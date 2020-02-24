''' Import Libraries '''
import pytz
import speech_recognition as sr
import os
import spacy
import nltk
from nltk import Tree
from spacy import displacy
from spacy.symbols import NOUN, NUM
from google.cloud import texttospeech
from gtts import gTTS
import pyttsx3 as pyt
import playsound

''' For Google Calendar '''
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

DAYS = ["monday", "tuesday", "wednesday","thursday","friday","saturday","sunday"]
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
DAY_EXTENTIONS = ["rd","th","st"]

''' See Versions '''
print(sr.__version__)
print(spacy.__version__)
print(nltk.__version__)

''' Next Steps '''

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def texttospeechwithpyttsx3():
    engine = pyt.init()
    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1.0)
    # voices = engine.setProperty("voices")
    # engine.setProperty("voice", voices[1].id)

    welcome = "Hello. How may I help you?"
    engine.say(welcome)
    engine.runAndWait()

texttospeechwithpyttsx3()

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
            print(said)
        except Exception as e:
            print("Exception: " + str(e))
            print("Sorry, I could not understand what you said.")

        return said

def check(sentence, words):
    res = [all([k in s for k in words]) for s in sentence]
    return [sentence[i] for i in range(0, len(res)) if res[i]]


def googleAuthentication():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'api/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service

def getEventsfromGoogle(day, service): #n is amount of events
    # Call the Calendar API

    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)
    events_result = service.events().list(calendarId ='primary', timeMin = date.isoformat(), timeMax = end_date.isoformat(),
                                        maxResults=10, singleEvents=True,
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
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass
    if month < today.month and month != -1:
        year = year + 1
    if day < today.day and month == -1 and day != -1:
        month = month + 1
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7
        return today + datetime.timedelta(dif)
    if month == -1 or day == -1:
        return None

    return datetime.date(month = month, day = day, year = year)

SERVICE = googleAuthentication()
text = get_audio()
getEventsfromGoogle(get_date(text), SERVICE)


# TALKTOHER = "hey"
# while True:
#     text = get_audio()
#
#     if text.count(TALKTOHER) > 0:
#         speak("Hello, how may I help you today?")
#         text = get_audio()
#
#         if "hello" in text.split():
#             speak("hello, how are you?")
#
#         if "name" in text.split():
#             speak("My name is Alice and I'm here to help you with booking.")
#
#
#         if "Malta" in text.split():
#             speak("Yes. She absolutely needs to sleep now. Nijat cares for her.")
#         os.remove('voice.mp3')