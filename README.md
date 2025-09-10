# Jarvis AI Assistant

A sophisticated AI-powered personal assistant that combines voice recognition, face authentication, machine learning, and system automation to create an intelligent desktop companion.

## Introduction

Jarvis AI Assistant is a comprehensive desktop application that transforms your computer into an intelligent, voice-controlled environment. Built with Python and modern web technologies, it provides hands-free access to system functions, health monitoring, information retrieval, and entertainment through natural voice commands and biometric security.

The project demonstrates advanced integration of multiple AI technologies including computer vision for face recognition, machine learning for health predictions, and natural language processing for intuitive user interaction.

## Features

### 🎤 Voice Control & Communication

- **Wake Word Detection**: Responds to "Jarvis" or "Alexa" for hands-free activation
- **Speech Recognition**: Converts voice commands to text for processing
- **Text-to-Speech**: Provides natural-sounding voice responses
- **Conversational AI**: Custom chatbot with probabilistic response matching

### 🔐 Security & Access Control

- **Face Recognition**: Biometric authentication using OpenCV and LBPH
- **User Verification**: Trained facial models for authorized access
- **Secure Login**: Local processing ensures privacy and security

### 🏥 Health & Medical Assistance

- **Heart Disease Prediction**: Machine learning model using TensorFlow
- **Health Metrics Analysis**: Processes blood pressure, cholesterol, heart rate data
- **Personalized Recommendations**: AI-powered health improvement suggestions

### ⚙️ System Control & Automation

- **Application Launching**: Voice-controlled desktop app management
- **Web Navigation**: Opens browsers and navigates to specified sites
- **System Functions**: Controls settings and utilities through voice commands

### 🌐 Information & Entertainment

- **Weather Updates**: Real-time weather information via OpenWeatherMap API
- **News Headlines**: Current events via NewsAPI
- **YouTube Integration**: Video playback through voice search queries
- **Knowledge Base**: Time, date, and general information responses

### 📱 Contact & Communication

- **Contact Database**: SQLite-based contact management system
- **Voice Search**: Find contacts by name for phone/email access
- **Data Organization**: Structured contact storage with multiple fields

### 🎨 Modern User Experience

- **Animated Interface**: Particle effects and smooth transitions
- **Responsive Design**: Web-based UI accessible through desktop
- **Real-time Feedback**: System status and command confirmation display

## Tech Stack

### Core Technologies

- **Backend**: Python 3.9+ with multiprocessing architecture
- **Frontend**: HTML5, CSS3, JavaScript
- **Desktop Integration**: Eel framework for Python-Web bridge
- **Database**: SQLite3 with custom schema management

### AI & Machine Learning

- **Computer Vision**: OpenCV 4.11 (LBPH face recognition)
- **Deep Learning**: TensorFlow 2.18 with Keras
- **Machine Learning**: Scikit-learn 1.5.2
- **NLP**: Custom chatbot with probabilistic response matching

### Audio & Speech Processing

- **Speech Recognition**: SpeechRecognition library with PyAudio
- **Text-to-Speech**: pyttsx3 (SAPI5 engine)
- **Voice Activation**: Porcupine wake word detection
- **Audio Playback**: playsound library

### System Integration & Automation

- **Desktop Automation**: PyAutoGUI
- **Process Management**: Python multiprocessing
- **Device Management**: ADB integration for Android connectivity

### Web Technologies & APIs

- **Frontend Framework**: Bootstrap 5.0
- **JavaScript Libraries**: Modernizr, custom particle animations
- **External APIs**: OpenWeatherMap, NewsAPI, YouTube integration
- **Web Scraping**: BeautifulSoup4

### Data Processing & Analytics

- **Data Manipulation**: NumPy, Pandas
- **Model Persistence**: Joblib
- **Data Visualization**: Matplotlib
- **CSV Processing**: Built-in CSV handling

### Security & Authentication

- **Face Recognition**: Haar Cascade classifiers with LBPH models
- **Database Security**: SQLite with parameterized queries

### Development & Deployment

- **Version Control**: Git
- **Dependencies**: Comprehensive requirements.txt (100+ packages)
- **Platform**: Windows-focused with PowerShell integration
- **Architecture**: Modular design (engine, web interface, auth modules)

## Installation & Setup

### Prerequisites

- Python 3.9 or higher
- Windows 10/11 (primary platform)
- Microphone and webcam for voice/face features
- Internet connection for API services

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/jarvis-ai-assistant.git
cd jarvis-ai-assistant
```

### Step 2: Install Dependencies

```bash
pip install -r engine/requirements.txt
```

### Step 3: Set Up API Keys

Create API keys for external services:

1. **OpenWeatherMap API**:

   - Visit [OpenWeatherMap](https://openweathermap.org/api)
   - Sign up and get your free API key
   - Update `engine/long__responses.py` with your key

2. **NewsAPI**:
   - Visit [NewsAPI](https://newsapi.org/)
   - Sign up and obtain your API key
   - Update `engine/long__responses.py` with your key

### Step 4: Database Setup

Ensure the following files exist in your project root:

- `jarvis.db` (SQLite database)
- `contacts.csv` (contact data)
- `heart_disease_model.h5` (trained ML model)
- `scaler.save` (model preprocessing scaler)

### Step 5: Run the Application

```bash
pip install tensorflow
pip install eel
pip install pandas
pip install joblib
pip install scikit-learn
```

---

### Step 4: Add Required Files

#### Step 1: Ensure the Database File Exists

Verify that `jarvis.db` is present in the root directory of the project.

#### Step 2: Initialize the Database Tables

Use `db.py` or the following commands to create necessary tables:

- **System Commands Table**:
  ```sql
  CREATE TABLE IF NOT EXISTS sys_command(
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    path VARCHAR(1000)
  );
  ```
- **Web Commands Table**:
  ```sql
  CREATE TABLE IF NOT EXISTS web_command(
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    url VARCHAR(1000)
  );
  ```
- **Contacts Table**:
  ```sql
  CREATE TABLE IF NOT EXISTS contacts(
    id INTEGER PRIMARY KEY,
    name VARCHAR(200),
    mobile_no VARCHAR(255),
    email VARCHAR(255) NULL
  );
  ```

#### Step 3: Populate Tables

Add system and web commands using SQL queries or via `db.py`. For example:

- Add a system command:
  ```python
  query = "INSERT INTO sys_command VALUES (null, 'command prompt', 'c:\\Windows\\system32\\cmd.exe')"
  cursor.execute(query)
  con.commit()
  ```
- Add a web command:
  ```python
  query = "INSERT INTO web_command VALUES (null, 'google', 'https://www.google.com/')"
  cursor.execute(query)
  con.commit()
  ```

#### Step 4: Import Contacts

Place `contacts.csv` in the root directory with contact details formatted as:

```
Name,Mobile,Email
John Doe,1234567890,john@example.com
```

Modify and uncomment the `db.py` section for importing contacts:

```python
with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        cursor.execute('INSERT INTO contacts VALUES (null, ?, ?, ?)', (row[0], row[1], row[2]))
con.commit()
```

#### Step 5: Use Database Queries

Search Contacts: Use `db.py` or the following SQL to search:

```python
cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ?", ('%search_query%',))
results = cursor.fetchall()
print(results)
```

---

### Step 5: Configure API Keys in `long__response.py`

To enable weather and news functionalities, users need to add their own API keys.

#### **Step 1: Obtain API Keys**

1. **Weather API Key**:
   - Visit [OpenWeatherMap](https://openweathermap.org/api) to sign up and get a free API key.
2. **News API Key**:
   - Visit [NewsAPI](https://newsapi.org/) to sign up and obtain an API key.

#### **Step 2: Update `long__response.py`**

- Open the `longresponse.py` file in any text editor.
- Replace the placeholder values with your API keys:
  ```python
  WEATHER_API_KEY = "your_weather_api_key_here"
  NEWS_API_KEY = "your_news_api_key_here"
  ```

#### **Step 3: Save the File**

- Save the changes and close the editor.

#### **Step 4: Verify the Setup**

- Run the application (`python run.py`) and test weather or news commands to confirm that the APIs are functioning.

---

### Step 6: Heart Disease Model Setup

#### To train or test the heart disease prediction model:

1. Ensure the `heart_disease_model.h5` file is in the project root.
2. If training is required:
   - Use `savefile.py` with a dataset named `heart.csv`.
   - Run:
     ```bash
     python savefile.py
     ```

---

### Step 7: Launch NeuraLink

Start the application:

```bash
python run.py
```
