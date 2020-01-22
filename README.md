# Installation

### Install Python 3
#### For Windows
Download Python 3 [here](https://www.python.org/ftp/python/3.8.1/python-3.8.1.exe) then install it in your computer.
#### For Linux and MacOS
No need to install python3 separetly. 
To see which version of Python 3 you have already installed, open a command prompt and run 
```python3 --version```

### Install ```pip``` 
```pip``` is a package-management system used to install and manage software packages written in Python.
#### For windows user
No need to install ```pip``` separetly after installing python 3.
#### For linux user
Open terminal (press Ctrl+Alt+T in Ubuntu) then write the command and press enter ```sudo apt install pip```

### Install virtualenv using ```pip```:
```
pip install virtualenv
```
In the project root directory
### Create a virtual environment using ```virtualenv```:
```
virtualenv venv
```
```venv``` can be any name.

### Active virtual environment ```venv```:
In the project root directory type:
#### For Windows:
```"venv/Scripts/activate.bat"``` and hit enter
#### For Linux:
```source/venv/bin/activate``` and hit enter

#### Now install some required libraries for our project:
Install python timezone
```
pip install pytz
```
Install python image library
```
pip install Pillow
```
Install python SpeechRecognition library
```
pip install SpeechRecognition
```
Install python ```PyAudio``` library (Required to work with ```SpeechRecognition```):

There is no wheel (prebuilt package) for Python 3.7 or above on Windows.
We need to download pyaudio from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio).

After download, just type
```
pip install <downloaded file name>
```
Install python text-to-speech library:
```
pip install pyttsx3
```
pyttsx3 is a Text to Speech (TTS) library for Python 2 and 3. Works without internet connection 
or delay. Supports multiple TTS engines, including Sapi5, nsss, and espeak.

Install python vlc library to work with VLC media player:
```
pip install python-vlc 
```
This module provides ctypes-based bindings for the native libvlc API of the VLC video player. Note that it relies on an already present install of VLC.

Install python pafy library:
```
pip install pafy
```
Retrieve YouTube content and metadata. Retrieve the URL to stream the video in a vlc player.
 
Install ```youtube-dl``` (Required to work with ```pafy```)
```
pip install --upgrade youtube_dl
```

#### Install the Google client library:
``` 
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

#### For Google calendar events:
Turn on the Google Calendar API from [here](https://developers.google.com/calendar/quickstart/python) and download the credentials.json file and place it to root directory.

#### Caution
We may need to check on our microphone volume settings. 
If it's too sensitive, the microphone may be picking up a lot of ambient noise. 
If it is too insensitive, the microphone may be rejecting speech as just noise.

### Watch output on YouTube:
[![Virtual Assistant Image](https://github.com/almasud/Virtual_Voice_Assistant/blob/master/screenshot.jpg)](https://youtu.be/yjxzA8449qs)

##### Thank you all and happy codding... 
[Abdullah Almasud](https://facebook.com/almasud.arm)
