import pyttsx3
import speech_recognition as sr
import eel
import time

# Initialize the error counter
error_counter = 0
max_errors = 5  # Maximum number of allowed errors

def speak(text):
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()

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
def allCommands():
    try:
        query= takeCommand()
        print(query)

        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
            flag = ""
            contact_no, name = findContact(query)
            if(contact_no != 0):

                if "send message" in query:
                    flag = 'message'
                    speak("what message to send")
                    query = takeCommand()
                    
                elif "phone call" in query:
                    flag = 'call'
                else:
                    flag = 'video call'
                    
                whatsApp(contact_no, query, flag, name)
        else:
            print("Not run")
    except:
        print("error")

    eel.ShowHood()    

        