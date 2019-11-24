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
pip install pytz
pip install SpeechRecognition
```
Install PyAudio (Required to work with SpeechRecognition):

There is no wheel (prebuilt package) for Python 3.7 or above on Windows.
We need to download pyaudio from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio).

After download, just type
```
pip install <downloaded file name>
```
Install pyttsx3:
```
pip install pyttsx3
```
pyttsx3 is a Text to Speech (TTS) library for Python 2 and 3. Works without internet connection 
or delay. Supports multiple TTS engines, including Sapi5, nsss, and espeak.

#### Then install the Google client library:
``` 
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### For Google calendar events:
Turn on the Google Calendar API from [here](https://developers.google.com/calendar/quickstart/python) and download the credentials.json file and place it to root directory.


#### Caution
We may need to check on our microphone volume settings. 
If it's too sensitive, the microphone may be picking up a lot of ambient noise. 
If it is too insensitive, the microphone may be rejecting speech as just noise.

### Watch output on YouTube:
[![Virtual Voice Assistant Image](https://github.com/almasud/Virtual_Voice_Assistant/blob/master/screenshot.jpg)](https://youtu.be/D5ClCGMC0GU)


##### Thank you all and happy codding... 
[Abdullah Almasud](https://facebook.com/almasud.arm)
