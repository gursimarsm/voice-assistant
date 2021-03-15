import pyttsx3
import datetime
import speech_recognition as sr 
import wikipedia
import smtplib
import webbrowser as wb
import psutil
import pyjokes
import os
import pyautogui
import random
import json
import requests
from urllib.request import urlopen
import wolframalpha
import time 

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
wolframalpha_app_id='GUJ9EV-76PEG4XPU3'

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time_():
    Time=datetime.datetime.now().strftime("%I:%M:%S") #24 hour clock
    speak("The current time is")
    speak(Time)

def date_():
    year = datetime.datetime.now().year
    month =  datetime.datetime.now().month
    date =  datetime.datetime.now().day
    speak("The current date is")
    speak(date)
    speak(month)
    speak(year)

def wishme():
    
    #Greetings
    hour = datetime.datetime.now().hour
    if hour>=6 and hour<12:
        speak("Good Morning Sir! Welcome Back")
    elif hour>=12 and hour<16:
        speak("Good Afternoon Sir! Welcome Back")
    elif hour>=16 and hour<24:
        speak("Good evening Sir! Welcome Back")
    else:
        speak("Good Evening Sir! Welcome Back")
    
    speak("Your personal assistant at your service. How can I help you?")


def TakeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening..")
        r.pause_threshold=1
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-IN')
        print(query)
    
    except Exception as e:
        print(e)
        print("Sorry I couldn't recognize that. Can you repeat that please?")
        speak("Sorry I couldn't recognize that. Can you repeat that please?")
        return "None"
    return query

def cpu():
    usage = str(psutil.cpu_percent())
    speak("CPU is at" +usage)
    battery = psutil.sensors_battery()
    speak('battery is at')
    speak(battery)
 
def joke():
    speak(pyjokes.get_joke())
 
def screenshot():
    img = pyautogui.screenshot()
    img.save('C:/Users/Waheguru/Downloads/screenshot.png')

def sendEmail(to,content):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()

    server.login('username@gmail.com','password')
    server.sendmail('username@gmail.com',to,content)
    server.close()


#if __name__=="__main__":
def MainClass():

    wishme()

    while True:
        query = TakeCommand().lower()

        #All commands will be storred in lower case in query
        #for easy recognition

        if 'time' in query:
            time_()

        elif 'date' in query:
            date_()

        elif 'wikipedia' in query:
            speak('Searching...')
            query=query.replace('wikipedia','')
            result=wikipedia.summary(query,sentences=3)
            speak("According to wikipedia")
            print(result)
            speak(result)

        elif 'send email' in query:
            try:
                speak("What should I say?")
                content=TakeCommand()

                speak("Who is the reciever?")
                reciever=input("Enter reciever's Email: ")
                to=reciever
                sendEmail(to,content)
                speak(content)
                speak('Email has been sent.')

            except Exception as e:
                print(e)
                speak("Unable to send the Email.")

        elif 'search in browser' in query:
            speak("What do you want me to search for?")
            search = TakeCommand().lower()
            wb.open_new_tab(search+'.com')

        elif 'search youtube' in query:
            speak("What should I search?")
            search_Term=TakeCommand().lower()
            speak("Here we go to youtube")
            wb.open('https://www.youtube.com/results?search_query='+search_Term)

        elif 'search google' in query:
            speak('What do you want to search')
            search_term=TakeCommand().lower()
            speak("Giving best results")
            wb.open('https://www.google.com/search?q=' +search_term)

        elif 'cpu' in query:
            cpu()
 
        elif 'joke' in query:
            joke()

        elif 'whatsapp' in query:
            os.system("WhatsappBOT.py")
 
        elif 'go offline' in query:
            speak('Going to sleep, Good Night sir!')
            quit()

        elif 'explorer' in query:
            speak("Opening explorer")
            explorer = r'C:\Windows\SysWOW64\explorer.exe'
            os.startfile(explorer)


        elif 'write a note' in query:
            speak("what do you want to write?")
            notes = TakeCommand()
            file = open('notes.txt','w')
            speak("Should I include the date and time?")
            ans = TakeCommand()
            if 'yes' in ans or 'sure' in ans:
                strTime = datetime.datetime.now().strftime("%H:%M:%S %p")
                file.write(strTime)
                file.write(':-')
                file.write(notes)
                speak("Done taking notes, Sir!")
            else:
                file.write(notes)

        elif 'show notes' in query:
            speak('showing notes')
            file = open('notes.txt', 'r')
            print(file.read())
            speak(file.read())
 
        elif 'screenshot' in query:
            screenshot()
            speak('Screenshot saved')
            
        elif 'songs' in query or 'song' in query:
            os.system("capture.py")


        elif 'remember that' in query:
            speak('What do you want me to remember?')
            memory=TakeCommand()
            speak("You asked me to remember "+memory)
            remember=open('memory.txt','w')
            remember.write(memory)
            remember.close()

        elif 'do you remember anything' in query:
            remember=open('memory.txt','r')
            speak("You asked me to remember "+remember.read())

        elif 'where is' in query:
            query = query.replace('Where is','')
            location = query
            speak("User askedd to locate: "+location)
            wb.open_new_tab("https://www.google.com/maps/place/"+location)

        elif 'news' in query:
            try:
                jsonObj=urlopen("http://newsapi.org/v2/everything?domains=wsj.com&apiKey=223eae49743f41428541dd10f4665c99")
                data=json.load(jsonObj)
                i=1

                speak("Here are some top head lines")
                print("=====TOP HEADLINES====="+'\n')
                for item in data['articles']:
                    print(str(i)+'. '+item['title']+'\n')
                    print(item['description']+'\n')
                    speak(item['description']+'\n')
                    speak(item['title'])
                    i += 1
            except Exception as e:
                        print(str(e))

        elif 'calculate' in query:
            client= wolframalpha.Client(wolframalpha_app_id)
            indx=query.lower().split().index('calculate')
            query=query.split()[indx+1:]
            res=client.query(''.join(query))
            answer=next(res.results).text
            print('The answer is '+answer)
            speak("The answer is"+answer)

        elif 'what is' in query or 'who is' in query:
            client=wolframalpha.Client(wolframalpha_app_id)
            res=client.query(query)

            try:
                print(next(res.results).text)
                speak(next(res.results).text)

            except StopIteration:
                print("No results")
                speak("No results")
            
        elif 'translate' in query:
            os.system("translator.py")

        elif "change voice" in query:
            randomVoice = Voiceflag;
            while randomVoice == Voiceflag:
                randomVoice = random.randint(0, len(voices)-1)
            engine.setProperty('voice', voices[randomVoice].id)
            wishme()
            Voiceflag = randomVoice

        elif "play punjabi music" in query:
            wb.open("https://wynk.in/music/package/punjabi-top-50/bb_1512370496100")

        elif "play rock music" in query:
            wb.open("https://wynk.in/music/playlist/feel-good-classic-rock/bb_1522918663585")

        elif "toss" in query:
            os.system("toss.py")


        elif 'stop listening' in query:
            speak("For how many seconds?")
            ans=int(TakeCommand())
            time.sleep(ans)
            print(ans)

        elif 'logout' in query:
            os.system("shutdown -l")
        elif 'restart' in query:
            os.system("shutdown /r /t 1")
        elif 'shutdown' in query:
            os.system("shutdown /s /t 1")
 
