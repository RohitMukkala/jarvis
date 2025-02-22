import os

import eel

from engine.features import *
from engine.auth import recoganize
from engine.command import *

def start():
    eel.init("www")

    playAssistantSound()

    @eel.expose
    def init():
        # subprocess.call([r'device.bat'])
        eel.hideLoader()
        speak("Ready for Face Authentication")
        flag = recoganize.AuthenticateFace()
        if flag == 1:
            eel.hideFaceAuth()
            speak("Face Authentication Successful")
            eel.hideFaceAuthSuccess()
            wishMe() 
            eel.hideStart()
            playAssistantSound()
        else:
            speak("Face Authentication Fail")

    os.system('start msedge.exe --app="http://localhost:8001/index.html"')

    #eel.start("index.html",mode=None,host="localhost",block=True)
    eel.start("index.html", mode=None, host="localhost", port=8001, block=True)