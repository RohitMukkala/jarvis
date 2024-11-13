from pyexpat import model
import pyttsx3
import speech_recognition as sr
import eel
import time
import datetime
import wikipedia
import webbrowser
import os
import random
import cv2
import pywhatkit as kit
import sys
import pyautogui
import operator
import requests
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import tensorflow as tf
import numpy as np
import joblib




def speak(text):
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


# Initialize speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def listen():
    with sr.Microphone() as source:
        print("Listening for your response...")
        audio = recognizer.listen(source)
    try:
        response = recognizer.recognize_google(audio)
        print("You said: " + response)
        return response.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that. Could you repeat?")
        return None
    except sr.RequestError:
        speak("Sorry, the speech service is unavailable.")
        return None


# def predict_heart_disease(data):
#     data = preprocess_input(data)
#     prediction = model.predict(data)

#     # Assuming binary classification (0 = no disease, 1 = disease)
#     if prediction[0] > 0.5:
#         speak("You are at risk for heart disease.")
#     else:
#         speak("You are not at risk for heart disease.")

# import tensorflow as tf

# # Load heart disease prediction model
# def load_heart_disease_model():
#     model = tf.keras.models.load_model("heart_disease_model.h5")  # Update path as needed
#     return model

# # Initialize the model
# heart_disease_model = load_heart_disease_model()

# # Function to predict heart disease
# def predict_heart_disease(features):
#     input_data = np.array(features).reshape(1, -1)  # Ensure data shape matches model input
#     prediction = heart_disease_model.predict(input_data)
#     if prediction[0] == 0:
#         print('The Person does not have Heart Disease')
#         print(prediction)
#     else:
#         print('The Person has Heart Disease')
#         print(prediction)

def load_heart_disease_model():
    model = tf.keras.models.load_model("heart_disease_model.h5")  # Update path as needed
    scaler = joblib.load("scaler.save")  # Load the scaler for input preprocessing
    return model, scaler

# Initialize the model and scaler
heart_disease_model, scaler = load_heart_disease_model()

# Preprocessing function
def preprocess_input(data):
    data = np.array(data).reshape(1, -1)  # Ensure data shape matches model input
    scaled_data = scaler.transform(data)  # Scale the data using the loaded scaler
    return scaled_data

# Function to predict heart disease
def predict_heart_disease(features):
    input_data = preprocess_input(features)
    prediction = heart_disease_model.predict(input_data)[0][0]  # Get the raw prediction score

    # Apply threshold to get binary output
    binary_output = 1 if prediction >= 0.5 else 0
    print(f'Raw model prediction: {prediction} | Binary output: {binary_output}')

    return prediction,binary_output


def suggest_health_improvements(metrics):
    suggestions = []
    # Extract individual metrics
    age, gender, chest_pain, bp, cholesterol, fasting_sugar, ecg, max_heart_rate, angina, old_peak, st_slope, vessels, thalassemia = metrics

    # Provide specific suggestions based on each metric
    if bp > 120:
        suggestions.append(f"Your blood pressure is {bp} mmHg, which is above the normal range. "
                           "Consider lifestyle changes like reducing salt intake, managing stress, "
                           "and regular exercise. Consult a healthcare provider if needed.")
    if cholesterol > 200:
        suggestions.append(f"Your cholesterol level is {cholesterol} mg/dL, which is high. "
                           "Adopt a low-cholesterol diet rich in fruits, vegetables, and whole grains, "
                           "and aim for regular physical activity to help lower it.")
    if max_heart_rate < 100:
        suggestions.append(f"Your maximum heart rate achieved is {max_heart_rate}, which is below the optimal range. "
                           "Incorporate more cardiovascular exercises like brisk walking, jogging, or cycling "
                           "to improve your heart rate capacity.")
    if fasting_sugar > 1:
        suggestions.append(f"Your fasting blood sugar level is elevated. Focus on a balanced diet with low sugar intake, "
                           "regular physical activity, and monitoring your glucose levels. If high levels persist, consult a doctor.")
    if angina == 1:
        suggestions.append("Exercise-induced angina was detected. Avoid strenuous activities without medical advice, "
                           "and consult a cardiologist for an exercise plan that suits your heart health needs.")

    return "\n".join(suggestions) if suggestions else "All metrics appear to be within normal ranges."

# Main function to handle the heart disease prediction process
def heart_disease_assessment():
    speak("Please provide the following health metrics for prediction. I will ask you each one by one.")

    # Example input metrics; replace these with real user input in a full implementation
    speak("What is your age?")
    age = int(listen())

    speak("What is your gender? Enter 1 for male and 0 for female.")
    gender = int(listen())

    speak("What is your chest pain type? Enter a number between 0 and 3.")
    chest_pain_type = int(listen())

    speak("What is your resting blood pressure in mm Hg?")
    resting_bp = int(listen())

    speak("What is your cholesterol level in mg/dl?")
    cholesterol = int(listen())

    speak("Is your fasting blood sugar greater than 120 mg/dl? Answer 1 for yes, 0 for no.")
    fasting_blood_sugar = int(listen())

    speak("What is your resting ECG? Answer 0, 1, or 2.")
    resting_ecg = int(listen())

    speak("What is your max heart rate achieved?")
    max_heart_rate = int(listen())

    speak("Do you have exercise-induced angina? Answer 1 for yes, 0 for no.")
    exercise_angina = int(listen())

    speak("What is your old peak value?")
    old_peak = float(listen())

    speak("What is the slope of the peak exercise ST segment? Enter 0, 1, or 2.")
    slope = int(listen())

    speak("How many major vessels are colored by fluoroscopy? Enter a number between 0 and 3.")
    vessels = int(listen())

    speak("What is your thalassemia status?")
    thalassemia = int(listen())

        # Collect all the inputs into a list
    features = [age, gender, chest_pain_type, resting_bp, cholesterol, fasting_blood_sugar, resting_ecg,
                    max_heart_rate, exercise_angina, old_peak, slope, vessels, thalassemia]
        
        # Predict heart disease based on the input features

    # features = [
    #     63,  # Age
    #     1,   # Gender
    #     3,   # Chest pain type
    #     145, # Resting blood pressure
    #     233, # Cholesterol
    #     1,   # Fasting blood sugar
    #     0,   # Resting ECG
    #     150, # Max heart rate achieved
    #     0,   # Exercise-induced angina
    #     2.3,   # Old peak
    #     0,   # Slope of the peak exercise ST segment
    #     0,   # Number of major vessels (0-3) colored by fluoroscopy
    #     1    # Thalassemia
    # ]
    # result = predict_heart_disease(features)


    # Predict heart disease
    prediction_score, binary_output = predict_heart_disease(features)

    # Provide feedback based on prediction score
    if prediction_score > 0.7:
        prediction_text = "The prediction indicates a high likelihood of heart disease. Please consult a doctor for further evaluation."
    elif 0.5 <= prediction_score <= 0.7:
        prediction_text = "The prediction indicates a moderate likelihood of heart disease. Consider lifestyle changes to lower risk."
    else:
        prediction_text = "The prediction indicates a low likelihood of heart disease. Maintain a healthy lifestyle."

    # Speak the prediction text
    print(prediction_text)
    speak(prediction_text)

    # Provide additional suggestions based on health metrics
    additional_suggestions = suggest_health_improvements(features)
    print("Additional health suggestions:")
    print(additional_suggestions)
    speak("Additional health suggestions are as follows.")
    speak(additional_suggestions)


# def heart_disease_command():
#     speak("Please provide the following health metrics for prediction.")
#     # Take user inputs interactively or use example values
#     features = [
#         44, # Age
#         1,  # Gender
#         0,  # Chest pain type
#         112, # Resting blood pressure
#         290, # Cholesterol
#         0,   # Fasting blood sugar
#         0,   # Resting ECG
#         153, # Max heart rate achieved
#         0,   # Exercise-induced angina
#         0, # Old peak
#         2,   # Slope of the peak exercise ST segment
#         1,   # Number of major vessels (0-3) colored by fluoroscopy
#         2    # Thalassemia
#     ]
#     result = predict_heart_disease(features)
#     if result == 1:
#         speak("The prediction indicates a high likelihood of heart disease.")
#     else:
#         speak("The prediction indicates a low likelihood of heart disease.")

# def suggest_improvements(metrics):
#     suggestions = []
#     # Extract individual metrics
#     age, gender, chest_pain, bp, cholesterol, fasting_sugar, ecg, max_heart_rate, angina, old_peak, st_slope, vessels, thalassemia = metrics

#     # Check each metric and provide specific suggestions
#     if bp > 120:
#         suggestions.append(f"Your blood pressure is {bp} mmHg, which is above the normal range. "
#                            "Consider lifestyle changes like reducing salt intake, managing stress, "
#                            "and regular exercise. Consult a healthcare provider if needed.")
#     if cholesterol > 200:
#         suggestions.append(f"Your cholesterol level is {cholesterol} mg/dL, which is high. "
#                            "Adopt a low-cholesterol diet rich in fruits, vegetables, and whole grains, "
#                            "and aim for regular physical activity to help lower it.")
#     if max_heart_rate < 100:
#         suggestions.append(f"Your maximum heart rate achieved is {max_heart_rate}, which is below the optimal range. "
#                            "Incorporate more cardiovascular exercises like brisk walking, jogging, or cycling "
#                            "to improve your heart rate capacity.")
#     if fasting_sugar > 1:
#         suggestions.append(f"Your fasting blood sugar level is elevated. Focus on a balanced diet with low sugar intake, "
#                            "regular physical activity, and monitoring your glucose levels. If high levels persist, consult a doctor.")
#     if angina == 1:
#         suggestions.append("Exercise-induced angina was detected. Avoid strenuous activities without medical advice, "
#                            "and consult a cardiologist for an exercise plan that suits your heart health needs.")
    
#     return "\n".join(suggestions) if suggestions else "All metrics appear to be within normal ranges."







# def heart_disease_command():
#     speak("Please provide the following health metrics for prediction. I will ask you each one by one.")
    
#     # Collecting health metrics interactively
#     try:
#         speak("What is your age?")
#         age = int(listen())

#         speak("What is your gender? Enter 1 for male and 0 for female.")
#         gender = int(listen())

#         speak("What is your chest pain type? Enter a number between 0 and 3.")
#         chest_pain_type = int(listen())

#         speak("What is your resting blood pressure in mm Hg?")
#         resting_bp = int(listen())

#         speak("What is your cholesterol level in mg/dl?")
#         cholesterol = int(listen())

#         speak("Is your fasting blood sugar greater than 120 mg/dl? Answer 1 for yes, 0 for no.")
#         fasting_blood_sugar = int(listen())

#         speak("What is your resting ECG? Answer 0, 1, or 2.")
#         resting_ecg = int(listen())

#         speak("What is your max heart rate achieved?")
#         max_heart_rate = int(listen())

#         speak("Do you have exercise-induced angina? Answer 1 for yes, 0 for no.")
#         exercise_angina = int(listen())

#         speak("What is your old peak value?")
#         old_peak = float(listen())

#         speak("What is the slope of the peak exercise ST segment? Enter 0, 1, or 2.")
#         slope = int(listen())

#         speak("How many major vessels are colored by fluoroscopy? Enter a number between 0 and 3.")
#         vessels = int(listen())

#         speak("What is your thalassemia status?")
#         thalassemia = int(listen())

#         # Collect all the inputs into a list
#         features = [age, gender, chest_pain_type, resting_bp, cholesterol, fasting_blood_sugar, resting_ecg,
#                     max_heart_rate, exercise_angina, old_peak, slope, vessels, thalassemia]
        
#         # Predict heart disease based on the input features
#         result = predict_heart_disease(features)
        
#         if result == 1:
#             speak("The prediction indicates a high likelihood of heart disease.")
#         else:
#             speak("The prediction indicates a low likelihood of heart disease.")
    
#     except ValueError:
#         speak("Invalid input detected. Please provide valid numerical values for each metric.")


# def convert_to_int(value, options_map):
#     """Converts a string response to corresponding integer values based on a map."""
#     value = value.lower().strip()
#     if value in options_map:
#         return options_map[value]
#     else:
#         return None  # If the value is not in the valid options map


# def get_valid_input(prompt, options_map=None, input_type=int):
#     """Generalized function to handle user input validation."""
#     while True:
#         speak(prompt)
#         response = listen()
        
#         if response:  # If Jarvis detects speech
#             response = response.strip().lower()
            
#             # If options_map is provided, convert the response to corresponding value
#             if options_map:
#                 converted_value = convert_to_int(response, options_map)
#                 if converted_value is not None:
#                     return converted_value
#                 else:
#                     speak(f"Invalid input. Please provide one of the following options: {', '.join(options_map.keys())}.")
#             else:
#                 try:
#                     # Convert the response to the required input type
#                     return input_type(response)
#                 except ValueError:
#                     speak("Invalid input. Please provide a valid number.")
#         else:
#             speak("I didn't understand that. Please speak clearly and try again.")

# def get_gender_input():
#     """Handles gender input, accepts male or female and converts to 1 or 0."""
#     while True:
#         speak("What is your gender? Please say male or female.")
#         response = listen().lower()
        
#         if response == "male":
#             return 1
#         elif response == "female":
#             return 0
#         else:
#             speak("I didn't understand that. Please say either male or female.")

# def get_fasting_blood_sugar_input():
#     """Handles fasting blood sugar input, accepts yes or no and converts to 1 or 0."""
#     while True:
#         speak("Is your fasting blood sugar greater than 120 mg/dl? Please say yes or no.")
#         response = listen().lower()
        
#         if response == "yes":
#             return 1
#         elif response == "no":
#             return 0
#         else:
#             speak("I didn't understand that. Please say either yes or no.")

# def heart_disease_command():
#     speak("Please provide the following health metrics for prediction. I will ask you each one by one.")
    
#     # Collecting health metrics interactively with validation
#     age = get_valid_input("What is your age?", input_type=int)
#     gender = get_gender_input()  # Get gender as 1 for male and 0 for female
#     chest_pain_type = get_valid_input("What is your chest pain type? Enter low, medium, or high.", 
#                                       options_map={'low': 0, 'medium': 1, 'high': 2}, input_type=int)
#     resting_bp = get_valid_input("What is your resting blood pressure in mm Hg?", input_type=int)
#     cholesterol = get_valid_input("What is your cholesterol level in mg/dl?", input_type=int)
#     fasting_blood_sugar = get_fasting_blood_sugar_input()  # Get fasting blood sugar as 1 for yes and 0 for no
#     resting_ecg = get_valid_input("What is your resting ECG? Enter low, medium, or high.", 
#                                   options_map={'low': 0, 'medium': 1, 'high': 2}, input_type=int)
#     max_heart_rate = get_valid_input("What is your max heart rate achieved?", input_type=int)
#     exercise_angina = get_valid_input("Do you have exercise-induced angina? Answer yes or no.", 
#                                       options_map={'yes': 1, 'no': 0}, input_type=int)
#     old_peak = get_valid_input("What is your old peak value?", input_type=float)
#     slope = get_valid_input("What is the slope of the peak exercise ST segment? Enter low, medium, or high.", 
#                             options_map={'low': 0, 'medium': 1, 'high': 2}, input_type=int)
#     vessels = get_valid_input("How many major vessels are colored by fluoroscopy? Enter low, medium, or high.", 
#                               options_map={'low': 0, 'medium': 1, 'high': 2}, input_type=int)
#     thalassemia = get_valid_input("What is your thalassemia status? Enter low, medium, or high.", 
#                                   options_map={'low': 0, 'medium': 1, 'high': 2}, input_type=int)
    
#     # Collect all the inputs into a list
#     features = [age, gender, chest_pain_type, resting_bp, cholesterol, fasting_blood_sugar, resting_ecg,
#                 max_heart_rate, exercise_angina, old_peak, slope, vessels, thalassemia]
    
#     # Predict heart disease based on the input features
#     result = predict_heart_disease(features)







def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("Welcome Sir. How can I Help you?")

def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source, 10, 6)

    try:
        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
       
    except Exception as e:
        return ""
    return query.lower()

@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takeCommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    try:
        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)
            if contact_no != 0:
                speak("Which mode you want to use: WhatsApp or mobile?")
                preference = takeCommand()
                print(preference)

                if "mobile" in preference:
                    if "send message" in query or "send sms" in query: 
                        speak("What message to send?")
                        message = takeCommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("Please try again.")
                elif "whatsapp" in preference:
                    if "send message" in query:
                        speak("What message to send?")
                        message = takeCommand()
                        whatsApp(contact_no, message, "message", name)
                    elif "phone call" in query:
                        whatsApp(contact_no, "", "call", name)
                    elif "video call" in query:
                        whatsApp(contact_no, "", "video call", name)
                    else:
                        speak("Please try again.")
                else:
                    speak("Invalid mode selected. Please try again.")
        else:
            # Additional commands integrated here
            if 'wikipedia' in query:
                speak('Searching Wikipedia...')
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            elif "predict heart disease" in query:
                 heart_disease_assessment()
            elif 'search in youtube' in query: 
                query = query.replace("search in youtube", "")
                webbrowser.open(f"www.youtube.com/results?search_query={query}")
            elif 'close chrome' in query:
                os.system("taskkill /f /im chrome.exe")
            elif 'close youtube' in query:
                os.system("taskkill /f /im msedge.exe")
            elif 'open google' in query:
                speak("What should I search?")
                qry = takeCommand().lower()
                webbrowser.open(f"{qry}")
            elif 'close google' in query:
                os.system("taskkill /f /im msedge.exe")
            elif 'shut down the system' in query:
                os.system("shutdown /s /t 5")
            elif 'restart the system' in query:
                os.system("shutdown /r /t 5")
            elif 'lock the system' in query:
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            elif 'close command prompt' in query:
                os.system("taskkill /f /im cmd.exe")
            elif 'open camera' in query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam', img)
                    k = cv2.waitKey(50)
                    if k == 27:
                        break
                cap.release()
                cv2.destroyAllWindows()
            elif 'go to sleep' in query:
                speak('Alright, I am switching off.')
                sys.exit()
            elif 'what is my ip address' in query:
                speak("Checking...")
                try:
                    ipAdd = requests.get('https://api.ipify.org').text
                    print(ipAdd)
                    speak("Your IP address is")
                    speak(ipAdd)
                except Exception as e:
                    speak("Network is weak, please try again later.")
            elif 'volume up' in query:
                for _ in range(5):
                    pyautogui.press("volumeup")
            elif 'volume down' in query:
                for _ in range(5):
                    pyautogui.press("volumedown")
            elif 'mute' in query:
                pyautogui.press("volumemute")
            elif 'refresh' in query:
                pyautogui.hotkey('ctrl', 'r')
            elif 'scroll down' in query:
                pyautogui.scroll(-1000)
            elif 'who are you' in query:
                speak('My name is Six. I am programmed to perform tasks based on my creator’s commands.')
            elif 'who created you' in query:
                speak("I am created with Python in Visual Studio Code.")
            elif 'take screenshot' in query:
                speak('Tell me a name for the file.')
                name = takeCommand().lower()
                time.sleep(3)
                img = pyautogui.screenshot()
                img.save(f"{name}.png")
                speak("Screenshot saved.")
            # elif 'jarvis' in query:
            #     speak("Yes Sir!")
            #     print("Yes Sir!")
            elif 'calculate' in query:
                speak("Ready")
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    audio = r.listen(source)
                my_string = r.recognize_google(audio)
                def get_operator_fn(op):
                    return {
                        '+': operator.add,
                        '-': operator.sub,
                        'x': operator.mul,
                        'divided': operator.__truediv__,
                    }[op]
                def eval_binary_expr(op1, oper, op2):
                    op1, op2 = int(op1), int(op2)
                    return get_operator_fn(oper)(op1, op2)
                speak("Your result is")
                speak(eval_binary_expr(*(my_string.split())))
            else:
                speak("I'm sorry, I couldn't find a suitable command.")
    except Exception as e:
        print("Error:", e)

    eel.ShowHood()
