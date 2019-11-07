After installing python on windows pip is by default installed.
Install virtualenv using pip:
pip install virtualenv
Create a virtual environment in the name of 'venv'
virtualenv venv
Active the virtualenv:
"venv/Scripts/activate.bat"

Now install some libraries for our projects:

pip install SpeechRecognition
pip install pyttsx3
pyttsx3 is a Text to Speech (TTS) library for Python 2 and 3. Works without internet connection 
or delay. Supports multiple TTS engines, including Sapi5, nsss, and espeak.

There is no wheel (prebuilt package) for Python 3.7 or above on Windows:
We need to download pyaudio from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio 
After download, just type 
pip install <downloaded file name>

Also, we need to check on our microphone volume settings. If it is too 
sensitive, the microphone may be picking up a lot of ambient noise. If it 
is too insensitive, the microphone may be rejecting speech as just noise.


