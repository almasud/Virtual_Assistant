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

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print("You say: " + said)
        except Exception as e:
            print("Exception: " + str(e))
    return said

text = get_audio()

if "hello" in text:
    speak("Hello, How are you")
if "what's your name" or "what is your name" in text:
    speak("My name is, Shikha")


