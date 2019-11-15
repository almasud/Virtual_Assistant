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

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENSIOS = ["rd", "th", "st"]

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_audio(status_bar=None):
    r = sr.Recognizer()
    said = ""
    try:
        with sr.Microphone() as source:
            print("Please wait. Calibrating your microphone...")  
            # listen for 1 seconds and create the ambient noise energy level  
            r.adjust_for_ambient_noise(source, duration=1)
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
    except Exception as e:
        print("Microphone Exception: ", e)
    
    return said


# Code for google calender
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
            if message_box.askokcancel("Calendar permisson request", "Calendar permission needed for working with your upcomming events.\nWould like to access your google calendar?"):
                flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    if not creds:
        return None
    else:
        service = build('calendar', 'v3', credentials=creds)
        return service


def get_events(date, service):
    # Call the Calendar API
    start_date = datetime.datetime.combine(date, datetime.datetime.min.time())  # Ex. 2019-11-07 00:00:00
    end_date = datetime.datetime.combine(date, datetime.datetime.max.time())  # Ex. 2019-11-07 23:59:59.999999

    events_result = service.events().list(calendarId='primary', timeMin=start_date.isoformat() + 'Z',
                                        timeMax=end_date.isoformat() + 'Z', singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak('Sorry, You have no upcoming events on this day.')
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
                found = word.find(ext)  # ex. 5th
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


def note(text):
    date = datetime.datetime.now()
    file_name = "notes/" + str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])
