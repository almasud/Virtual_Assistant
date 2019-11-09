# Installation
Install virtualenv using pip:
```
pip install virtualenv
```

Create a virtual environment
```
virtualenv venv
```
```venv``` can be any name.

### Active virtualenv:
#### For Windows:
In the project directory type ```"venv/Scripts/activate.bat"``` and hit enter
#### For Linux:
In the project directory type ```source/venv/bin/activate``` and hit enter

#### Now install some required libraries for our projects:
```
pip install SpeechRecognition
pip install pyttsx3
```
pyttsx3 is a Text to Speech (TTS) library for Python 2 and 3. Works without internet connection 
or delay. Supports multiple TTS engines, including Sapi5, nsss, and espeak.

#### Caution
We may need to check on our microphone volume settings. 
If it's too sensitive, the microphone may be picking up a lot of ambient noise. 
If it is too insensitive, the microphone may be rejecting speech as just noise.

##### Thank you all and happy codding... 
[Abdullah Almasud](https://facebook.com/almasud.arm)
