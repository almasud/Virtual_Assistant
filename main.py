import os
import time
import speech_recognition as sr
import playsound
from gtts import gTTS

def speak(text):
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)

speak("Hello Al masud")

