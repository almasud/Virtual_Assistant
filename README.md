# Installation
To create a virtual environment
### Install virtualenv using ```pip```:
```
pip install virtualenv
```

Now, In the project root directory
### Create a virtual environment using ```virtualenv```:
```
virtualenv venv
```
```venv``` can be any name.

Now it's time to active the vrtual environment
### Active virtual environment ```venv```:
In the project root directory type:
#### For Windows:
```"venv/Scripts/activate.bat"``` and hit enter
#### For Linux:
```source/venv/bin/activate``` and hit enter

#### Now install some required libraries for our project:
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
