''' Import Libraries '''

## For Speech Recognition
import speech_recognition as sr
import pytz
from google.cloud import texttospeech
import os
from gtts import gTTS
import pyttsx3
import playsound
import subprocess

''' For NLTK Dependency Tree '''
import spacy
from spacy import displacy
from spacy.symbols import NOUN, NUM

import nltk
from nltk import word_tokenize, sent_tokenize

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

ALLDAYSANDMONTHS = DAYS + MONTHS

''' See Versions '''
print(sr.__version__)
print(spacy.__version__)
print(nltk.__version__)

''' Next Steps '''

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def speak(text):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 50)
    engine.setProperty("volume", 1.0)
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak:")
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            #print("Exception: " + str(e))
            speak("Sorry, I could not understand what you said.")

        return said.lower()

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
        speak('You can book on this date, do you want to proceed?')

        if text.lower() == "yes":
            speak("Your booking has successfully written.")

    else:
        speak(f"Sorry, we don't have room for that day, do you want something else?")

def writeEventsonGoogleCalendar():

    return

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

def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])


nlp = spacy.load('en_core_web_sm')
doc = []
list_of_words = []

words = ['Do','Have','Which','What', 'Do']
no_interest = ['nothing', 'none']

def welcome_menu():
    customer_speech = get_audio()

    if "single" in customer_speech:
        speak("Good decision. So for what days would you like to book a room?")
        return "single"
    elif "double" in customer_speech:
        speak("Let me have a look. For which days would you like to book a room?")
        return "double"
    elif any(word in customer_speech for word in no_interest):
        speak("Thank you contacting us. We hope to see you soon.")

order_preference = welcome_menu()

def TakeReservationfromUser():
    global list_of_words
    list_of_words = []
    doc = nlp(text)
    spacy.displacy.render(doc, style='dep', jupyter=True)

    for possible_subject in doc:
        print("doc --", possible_subject.pos_)
        if((possible_subject.pos_ == 'NOUN' or possible_subject.pos_ == 'PROPN') and possible_subject.text.title() in ALLDAYSANDMONTHS):
            list_of_words.append(possible_subject.text.title())

        if(len(list_of_words) == 0):
            for word in doc:
                if(word.text.title() in words):
                    list_of_words.append(word.text.title())
                    break
        if(len(list_of_words) == 0):
            for word in doc:
                list_of_words.append(word.text.title())
                break
        list_of_words = list(set(list_of_words))
        print("Days ", list_of_words)

        return doc

CALENDAR_STRS = ["do", "have", "which", "what"]
NOTE_STRS = ["book", "register"]

SERVICE = googleAuthentication()
print("START")

while True:
    text = get_audio()
    for phrase in CALENDAR_STRS:
        if phrase in text.lower():
            date = get_date(text)
            if date:
                getEventsfromGoogle(get_date(text), SERVICE)
            else:
                speak("Sorry, I didn't understand what you have said. Could you please repeat?")

    for phrase in NOTE_STRS:
        if phrase in NOTE_STRS:
            if phrase in text.lower():
                speak("What would you like me to write down?")
                note_text = get_audio().lower()
                note(note_text)
                speak("I have made a note of that.")

    if "name" in text.split():
        speak("My name is Alice and I'm here to help you with booking.")






