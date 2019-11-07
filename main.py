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

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENSIOS = ["rd", "th", "st"]

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print("You say: " + said)
        except LookupError as err:
            print("Opps! could not understand audio: " + str(err))
    return said

# Code for google calender
def authenticate_google_calender():
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
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

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
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

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


""" 
Say for testing:
What's going on Wednessday? or
What's going on next Wednessday?
"""
service = authenticate_google_calender()
text = get_audio()
print("Your result:")
get_events(get_date(text), service)


