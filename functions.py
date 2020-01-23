from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import time
import pyttsx3
import speech_recognition as sr
import pytz
import subprocess
import urllib.request
import urllib.parse
import re

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENSIOS = ["rd", "th", "st"]

# For check wheather an internet connection exists or not
def is_internet():
    try:
        urllib.request.urlopen('https://google.com', timeout=1)
        return True
    except urllib.request.URLError: 
        return False

# For audio from text input
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# For text from audio input
def get_audio(status_bar=None):
    r = sr.Recognizer()
    said = ""
    try:
        with sr.Microphone() as source:
            print("Please wait. Calibrating your microphone...")
            if status_bar:
                status_bar["text"] = "Please wait. Calibrating your microphone..."
            # listen for 1 seconds and create the ambient noise energy level  
            r.adjust_for_ambient_noise(source, duration=1)
            # Listen from audio source
            print("Listening...")
            if status_bar:
                status_bar["text"] = "Listening..."
            audio = r.listen(source)
            try:
                said = r.recognize_google(audio)
                print("You say: " + said)
                if status_bar:
                    status_bar["text"] = "You say: " + said
            except LookupError as err:
                print("Opps! could not understand audio: " + str(err))
                if status_bar:
                    status_bar["text"] = "Opps! could not understand audio: " + str(err)
    except:
        pass
    
    return said

# For google calendar authentication service
def authenticate_google_calender(message_box=None):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            speak("Calendar permission needed, for working with your, upcomming events, Would you like to, access your google calendar?")
            if message_box.askokcancel("Calendar permisson request", "Calendar permission needed for working with your upcomming events.\nWould like to access your google calendar?"):
                flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            else:
                return None
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    if not creds:
        return None
    else:
        service = build('calendar', 'v3', credentials=creds)
        return service

# For events from google calendar
def get_events(date, service, status_bar=None):
    # Call the Calendar API
    start_date = datetime.datetime.combine(date, datetime.datetime.min.time())  # Ex. 2019-11-07 00:00:00
    end_date = datetime.datetime.combine(date, datetime.datetime.max.time())  # Ex. 2019-11-07 23:59:59.999999

    events_result = service.events().list(calendarId='primary', timeMin=start_date.isoformat() + 'Z',
                                        timeMax=end_date.isoformat() + 'Z', singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak('Sorry, You have no upcoming events on this day.')
        if status_bar:
            status_bar["text"] = "Sorry, You have no upcoming events on this day."
            
    else:
        event_num = len(events)
        if event_num > 1:
            speak(f"You have {event_num} events, on this day.")
            print("Your events are:")
        else:
            speak(f"You have only {event_num} event, on this day.")
            print("Your event is:")

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("-")[0])

            if int(start_time.split(":")[0]) < 12:
                start_time = start_time.split(":")[0] + ":" + start_time.split(":")[1]
                start_time += "am"
                print(start_time)
            else:
                start_time = str(int(start_time.split(":")[0]) - 12) + ":" + start_time.split(":")[1]
                start_time += "pm"
                print(start_time)

            speak(event['summary'] + ", at " + start_time)

# For a date that contains in a string
def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENSIOS:
                found = word.find(ext)  # ex. 12th
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass
    
    if month < today.month and month != -1:
        year += 1
    if day < today.day and day != -1 and month == -1:
        month += month
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()  # 0-6
        diff = day_of_week - current_day_of_week
        
        if diff < 0:
            diff += 7
            if text.count("next") >= 1:
                diff += 7

        return today + datetime.timedelta(diff)  # Ex. 2019-11-07 + 7 days, 0:00:00
    
    if month == -1 or day == -1:
        return None

    return datetime.date(month=month, day=day, year=year)

# For make a note from text input
def make_note(text):
    date = datetime.datetime.now()
    if not os.path.exists('notes'):
        os.makedirs('notes')
    file_name = "notes/" + str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])

# For playing a song from online (Youtube)
def play_from_online(text, status_bar=None):
    os.add_dll_directory(r'C:\Program Files (x86)\VideoLAN\VLC')
    import vlc, pafy

    # song name from user
    song = urllib.parse.urlencode({"search_query" : text})
    print(song)

    # fetch the ?v=query_string
    result = urllib.request.urlopen("https://www.youtube.com/results?" + song)

    # make the url of the first result song
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', result.read().decode())  # 11 is the number of characters of each video
    print(search_results)

    # make the final url of song selects the very first result from youtube result
    url = "https://www.youtube.com/watch?v="+search_results[0]

    # Play the song using vlc and pafy (dependency youtube-dl module) 
    # modules which opens the video
    video = pafy.new(url)
    best = video.getbest()
    media = vlc.MediaPlayer(best.url)
    media.play()
    # Take time to open vlc
    while not media.is_playing():
        time.sleep(1)

# For query about a person
def query_from_online(query_text, status_bar=None):
    from apiclient.discovery import build
    from functions import speak
    import webbrowser
    # Custom module that stores private keys
    from private_keys import (
        # Create a google developer API key and enable custom search engine API 
        google_python_api_key,
        # Create a google custom search engine and get the search engine key 
        google_custom_search_engine_id
    )

    resource = build("customsearch", 'v1', developerKey=google_python_api_key).cse()
    result = resource.list(q=query_text, cx=google_custom_search_engine_id).execute()
    snippet = result['items'][0]["snippet"]
    formattedUrl = result['items'][0]["formattedUrl"]

    # Format the snipet strings by adding comma (,) between every
    # two words for better readabilty
    step = 2
    formatted_snippet = ", ".join([" ".join(snippet.split(" ")[i:i+step]) 
            for i in range(0, len(snippet.split(" ")), step)])
    print(formatted_snippet)
    speak(formatted_snippet)

    # If more query render into web browser.
    speak("Would you like to, know more?")
    if  get_audio(status_bar=status_bar).lower().count("yes") > 0:
        webbrowser.open(formattedUrl)
    