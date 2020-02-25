import speech_recognition as sr
import pyttsx3
import playsound
import subprocess
import datetime
import spacy 
import sqlite3
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

nlp = spacy.load('en_core_web_sm')

#McDonald's MENUS
hamburger = ['Hamburger','Cheeseburger', 'Big Mac','Big And Tasty', '']
chicken = ['Chicken','Nuggets','Snack Wrap']
fish = ['Fish','Bites']
pork = ['Mc rib', '']
salad = ['']
side = ['French fries','Garlic fries']
breakfast = ['Mc muffins', 'Sandwiches', 'Bagels', 'Wraps']
beverage = ['Soft drink', 'Coffee', 'Tea','Shake']

how_many = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
allitems = hamburger + chicken + fish + pork + salad + side + breakfast + beverage


doc = []
list_of_words = []

#INITIALIZING THE DATABASE
conn = sqlite3.connect('mcd.db')

c = conn.cursor()

c.execute("SELECT * FROM foods")
#print(c.fetchall())
conn.commit()
conn.close()


def initDatabase(database_file, nameoffood):
    query = "SELECT * FROM foods WHERE name=?;"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    cursor.execute(query, [nameoffood])
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results


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
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            speak("Sorry, I could not understand what you said.")

        return said.lower()

specific_words = ['do', 'have', 'which', 'what']
no_interest = ['no', 'nothing','none','do not']


def takingOrders():
    user_speech = get_audio()

    if "hamburger" in user_speech:
        speak("For today we serve these hamburgers.")
        print("For today we serve these hamburgers.")
        for meal in hamburger:
            speak(meal)
            print(meal)
        speak("Which one would you love to have?")
        print("Which one would you love to have?")
        return "hamburger"
    elif "chicken" in user_speech:
        speak("For today we have these chicken burgers.")
        for meal in chicken:
            speak(f"We have {meal}")
        speak("Which one would you like to prefer?")
        return "chicken"
    elif "fish" in user_speech:
        speak("For today we have these kind of fish.")
        for meal in fish:
            #speak(f"Let me see.")
            speak(f"We have {meal}")
        speak("Which one would you like to prefer?")
        return "fish"
    elif "pork" in user_speech:
        speak("For today we have these kind of pork burgers.")
        for meal in pork:
            #speak(f"Let me see.")
            speak(f"We have {meal}")
        speak("Which one would you like to prefer?")
        return "pork"
    elif "salad" in user_speech:
        speak("For today we have these kind of salads.")
        for meal in salad:
            #speak(f"Let me see.")
            speak(f"We have {meal}")
        speak("Which one would you like to prefer?")
        return "salad"
    elif "side" in user_speech:
        speak("For today we have these side.")
        for meal in side:
            speak(f"{meal}")
        speak("Which one would you like to prefer?")
        return "side"  
    elif "breakfast" in user_speech:
        speak("For today we serve breakfast.")
        for meal in breakfast:
            speak(f"{meal}")
        speak("Which one would you like to prefer?")
        return "breakfast"
    elif "beverage" in user_speech:
        speak("For today we have these kind of beverages")
        for meal in beverage:
            speak(f"{meal}")
        speak("Which one would you like to prefer?")
        return "beverage"
    elif any(word in user_speech for word in no_interest):
        speak("Thank you for your response. We hope to see you soon.")

def repeat_menu():
    speak("Here is what we have for hamburgers.")
    for meal in hamburger:
        speak(meal)
    speak("Here is what we have for chicken.")
    for meal in chicken:
        speak(meal)
    speak("Here is what we have for fish.")
    for meal in fish:
        speak(meal)
    speak("Here is what we have for side menu.")
    for meal in side:
        speak(meal)

    speak("Here is what we have for beverages.")
    for meal in beverage:
        speak(meal)

    ### SO ON ###

    speak("What would you like to have?")

list_of_numbers = []
def take_customer_order(user_speech):
    global list_of_words
    list_of_words = []
    global list_of_numbers

    doc = nlp(user_speech)

    for possible_subject in doc:
        print("doc --", possible_subject.pos_)
        if((possible_subject.pos_ == 'NOUN' or possible_subject.pos_ == 'PROPN') and possible_subject.text.title() in allitems):
            list_of_words.append(possible_subject.text.title())

        #checking numbers
        if((possible_subject.pos_ == 'NUM')):
            list_of_numbers.append(possible_subject.text.title())

    if(len(list_of_words) == 0):
        for word in doc:
            if(word.text.title() in specific_words):
                list_of_words.append(word.text.title())
                break
    if(len(list_of_words) == 0):
        for word in doc:
            list_of_words.append(word.text.title())
            break
    list_of_words = list(set(list_of_words))
    print("Menus ", list_of_words)

    return doc

def confirm_customer_order():
    global list_of_words

    orders = []

    for meal in list_of_words:
        if(order_preference == 'hamburger' and meal in hamburger) \
                or (order_preference == 'chicken' and meal in chicken) \
                or (order_preference == 'fish' and meal in fish) \
                or (order_preference == 'side' and meal in side) \
                or (order_preference == 'breakfast' and meal in breakfast) \
                or (order_preference == 'beverage' and meal in beverage):
            orders.append(meal)
        
    if len(orders) > 1:
        speechoutput = " and ".join(str(x) for x in orders)
        #there will be several items
        #so maybe need to split the list
        #speechoutputsplitted = speechoutput.split()
        #print(speechoutput)

        speak('Your ' + speechoutput + ' are being served.')
        speak("Thank you for choosing Mc Donald's")
        print('Your ' + speechoutput + ' are being served.')
        print("Thank you for choosing Mc Donald's")

        query = "UPDATE foods SET available = available - 1;"
        connection = sqlite3.connect('mcd.db')
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return True

    for meal in list_of_words:
        #If the meal the customer ordered is available
        if meal in allitems:
            print('You have ordered ', meal)
            speak('Your '+ meal + ' are being served.')
            speak("Bon appetito and thanks for choosing Mc Donald's")
            print('Your ' + meal + ' are being served.')
            print("Bon appetito and thank you for choosing Mc Donald's")

            query = "UPDATE foods SET available = available - 1;"
            connection = sqlite3.connect('mcd.db')
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            connection.close()

            break

        #If customer asks about the meals again or not sure of what to have
        elif meal in specific_words:
            repeat_menu()
            list_of_words = []
            order = get_audio()
            take_customer_order(order)
            confirm_customer_order()
            break

        #If customer doesn't want the available meals
        elif meal in no_interest:
            list_of_words = []
            print('Thanks for stopping by. We hope to see you again soon.')
            speak('Thanks for stopping by. We hope to see you again soon.')
            break

        #If customer request for something that is not available in the menu list
        elif meal not in allitems and specific_words:
            print('I\'m sorry but we don\'t have '+meal)
            speak('I\'m sorry We don\'t have '+meal)
            repeat_menu()
            list_of_words = []
            order = get_audio()
            take_customer_order(order)
            confirm_customer_order()
            break


print("Hey. It is good to see you in McDonald's Rome branch. What would you like to have today?")
speak("Hey. It is good to see you in McDonald's Rome branch. What would you like to have today?")


while True:
    order_preference = takingOrders()
    print("You have ordered ", order_preference)

    user_speech = get_audio()
    customer_order = take_customer_order(user_speech)

    print(customer_order)
    print(list_of_words)

    confirm_customer_order()

    speak("Would you like to have something else as well?")



