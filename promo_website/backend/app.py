import os
from flask import Flask, request, jsonify, g
from flask_cors import CORS
import mysql.connector
import bcrypt
import jwt
import datetime
from functools import wraps
import numpy as np
import joblib
from tensorflow.keras.models import load_model
import fitz  # PyMuPDF
import re
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Flask App ---
app = Flask(__name__)
frontend_url = "https://jarvis-one-teal.vercel.app"
CORS(app, origins=[
    frontend_url,
    "http://127.0.0.1:5500",
    "http://localhost:5500"
])

# --- Config from environment ---
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'super-secret-key')

# --- API Keys ---
OPENWEATHERMAP_API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY")
GNEWS_API_KEY = os.environ.get("GNEWS_API_KEY")

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_NAME = os.environ.get('DB_NAME', 'jarvis_db')

# --- Load AI Model and Scaler ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    model = load_model(os.path.join(BASE_DIR, 'heart_disease_model.h5'))
    scaler = joblib.load(os.path.join(BASE_DIR, 'scaler.save'))
except Exception as e:
    print(f"Error loading model/scaler: {e}")
    model, scaler = None, None

# --- Database Connection ---
def get_db_connection():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# --- Authentication Decorator ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, username, email FROM users WHERE id = %s", (data['user_id'],))
            current_user = cursor.fetchone()
            cursor.close()
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        if not current_user:
            return jsonify({'message': 'User not found!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

# --- Helper Functions for External APIs ---
def get_weather(city="Amaravati"):
    if not OPENWEATHERMAP_API_KEY or OPENWEATHERMAP_API_KEY == "YOUR_OPENWEATHERMAP_API_KEY":
        return {"error": "Weather API key not configured."}
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "temperature": round(data['main']['temp']),
            "description": data['weather'][0]['description'].title(),
            "icon": data['weather'][0]['icon']
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Could not fetch weather data: {e}"}

def get_news():
    if not GNEWS_API_KEY:
        return {"error": "GNews API key not configured."}
    try:
        url = f"https://gnews.io/api/v4/top-headlines?country=in&lang=en&token={GNEWS_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        articles = []
        for article in data.get("articles", [])[:5]:
            articles.append({
                "title": article.get("title"),
                "source": article.get("source", {}).get("name"),
                "url": article.get("url")
            })
        return {"articles": articles}
    except requests.exceptions.RequestException as e:
        return {"error": f"Could not fetch news data from GNews: {e}"}

# --- Routes ---
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'Missing data'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (%s,%s,%s)",
                       (username, email, hashed_password))
        conn.commit()
    except mysql.connector.IntegrityError:
        return jsonify({'message': 'Username or email already exists'}), 409
    finally:
        cursor.close()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Missing credentials'}), 401

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    cursor.close()

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = jwt.encode({
        'user_id': user['id'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({
        'token': token,
        'username': user['username'],
        'user_id': user['id']
    }), 200

@app.route('/api/dashboard', methods=['GET'])
@token_required
def dashboard(current_user):
    mock_activity = [
        {'timestamp': '2023-10-27 10:00:00', 'command': 'weather in London'},
        {'timestamp': '2023-10-27 10:02:15', 'command': 'open chrome'},
        {'timestamp': '2023-10-27 10:05:30', 'command': 'play music on youtube'}
    ]
    return jsonify({
        'username': current_user['username'],
        'user_id': current_user['id'],
        'activity': mock_activity
    })

@app.route('/api/predict_health', methods=['POST'])
@token_required
def predict_health(current_user):
    data = request.get_json()
    features = data.get('features')

    if not features or len(features) != 13:
        return jsonify({'message': '13 features required'}), 400

    if not model or not scaler:
        return jsonify({'message': 'Model not loaded'}), 503

    try:
        features_np = np.array(features).reshape(1, -1)
        scaled_features = scaler.transform(features_np)

        prediction = float(model.predict(scaled_features)[0][0])
        result = 'positive' if prediction > 0.5 else 'negative'

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO health_predictions (user_id, input_data, prediction_result) VALUES (%s,%s,%s)",
                       (current_user['id'], str(features), result))
        conn.commit()
        cursor.close()

        return jsonify({'prediction': result, 'probability': prediction}), 200
    except Exception as e:
        return jsonify({'message': f'Prediction error: {str(e)}'}), 500

@app.route('/api/predict_health_pdf', methods=['POST'])
@token_required
def predict_health_pdf(current_user):
    if 'file' not in request.files:
        return jsonify({'message': 'No file uploaded'}), 400
    file = request.files['file']
    if not file.filename.endswith('.pdf'):
        return jsonify({'message': 'Invalid file type'}), 400

    try:
        pdf_document = fitz.open(stream=file.read(), filetype="pdf")
        text = "".join([page.get_text() for page in pdf_document])

        feature_order = [
            "Age", "Sex", "CP", "Trestbps", "Chol", "FBS",
            "RestECG", "Thalach", "Exang", "Oldpeak", "Slope", "CA", "Thal"
        ]
        patterns = {
            "Age": r"Age[:\s]+(\d+)",
            "Sex": r"Sex[:\s]+(\d+)",
            "CP": r"CP[:\s]+(\d+)",
            "Trestbps": r"(?:Trestbps|Resting\s*BP)[:\s]+(\d+)",
            "Chol": r"(?:Chol|Cholesterol)[:\s]+(\d+)",
            "FBS": r"(?:FBS|Fasting\s*BS)[:\s]+(\d+)",
            "RestECG": r"(?:RestECG|Resting\s*ECG)[:\s]+(\d+)",
            "Thalach": r"(?:Thalach|Max\s*HR)[:\s]+(\d+)",
            "Exang": r"(?:Exang|Exercise\s*Angina)[:\s]+(\d+)",
            "Oldpeak": r"Oldpeak[:\s]+([\d.]+)",
            "Slope": r"Slope[:\s]+(\d+)",
            "CA": r"CA[:\s]+(\d+)",
            "Thal": r"Thal[:\s]+(\d+)"
        }

        features_dict = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            features_dict[key] = float(match.group(1)) if match else None

        if any(v is None for v in features_dict.values()):
            return jsonify({
                'message': 'Could not find all required values in PDF',
                'parsed': features_dict
            }), 400

        features = [features_dict[key] for key in feature_order]

        scaled_features = scaler.transform([features])
        prediction_val = float(model.predict(scaled_features)[0][0])
        result = 'positive' if prediction_val > 0.5 else 'negative'

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO health_predictions (user_id, input_data, prediction_result) VALUES (%s,%s,%s)",
            (current_user['id'], str(features), result)
        )
        conn.commit()
        cursor.close()

        return jsonify({
            'prediction': result,
            'probability': prediction_val,
            'features': features,
            'parsed': features_dict
        }), 200

    except Exception as e:
        return jsonify({'message': f'Error processing PDF: {str(e)}'}), 500

@app.route('/api/daily_briefing', methods=['GET'])
@token_required
def daily_briefing(current_user):
    weather_data = get_weather()
    news_data = get_news()
    return jsonify({
        "weather": weather_data,
        "news": news_data
    })

# --- Run App ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False') == 'True'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
