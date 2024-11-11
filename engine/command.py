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

# Initialize the error counter
error_counter = 0
max_errors = 3  # Maximum number of allowed errors

def speak(text):
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    engine.setProperty('rate', 150)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("Welcome Sir. How can I Help you?")

# This function restarts the microphone listening process
def restartListening():
    global error_counter
    if error_counter < max_errors:
        error_counter += 1
        eel.DisplayMessage(f"Error occurred {error_counter} times. Restarting mic...")
        takeCommand()  # Restart the process
    else:
        eel.DisplayMessage("Too many errors. Showing failure message...")
        eel.ShowHood()  # Call the JavaScript function to show the hood UI
        error_counter = 0  # Reset the counter after showing the error message

def takeCommand():
    global error_counter
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening....")
        eel.DisplayMessage("Listening....")
        r.adjust_for_ambient_noise(source)
        r.dynamic_energy_threshold = True
        r.energy_threshold = 300

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            eel.DisplayMessage("Listening timeout, restarting mic...")
            restartListening()
            return ""

    try:
        print("recognizing")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
    
        # Reset error counter after a successful recognition
        error_counter = 0

    except sr.UnknownValueError:
        eel.DisplayMessage("Sorry, I could not understand the audio.")
        restartListening()
        return ""

    except sr.RequestError:
        eel.DisplayMessage("Network error. Please check your connection.")
        restartListening()
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
                    message = ""
                    if "send message" in query:
                        message = 'message'
                        speak("What message to send?")
                        query = takeCommand()
                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                    whatsApp(contact_no, query, message, name)
        else:
            # Additional commands integrated here
            if 'wikipedia' in query:
                speak('Searching Wikipedia...')
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
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
