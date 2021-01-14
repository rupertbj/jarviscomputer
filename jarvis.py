#!/usr/bin/env python3
#Porcupine wakeword includes
import struct
import pyaudio
import pvporcupine
#speech recognition includes
import speech_recognition as sr
#information includes
import wolframalpha
import wikipedia
import pyjokes
#system includes
import webbrowser
import os
import time
import datetime
import subprocess
import json
import requests
import random
from subprocess import call

def speak(text):
    call(['espeak', '-v', 'mb-us1', text])

def wishMe():
    hour=datetime.datetime.now().hour
    morning=['Good morning handsome', 'Whats up dog', 'top of the morning to you', 'Good morning sir']
    afternoon=['Good afternoon, Rupert', 'Good afternoon sir', 'isnt it time for a drink yet?']
    evening=['Good evening sir', 'Good evening', 'Good evening Rupert']

    if hour>=0 and hour<12:
        rand_item = random.choice(morning)
        speak(rand_item)
        print(rand_item)

    elif hour>=12 and hour<18:
        rand_item = random.choice(afternoon)
        speak(rand_item)
        print(rand_item)

    else:
        rand_item = random.choice(evening)
        speak(rand_item)
        print(rand_item)

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio=r.listen(source)

        try:
            statement=r.recognize_google(audio,language='en-in')
            print(f"user said: {statement}\n")

        except Exception as _:
            speak("Sorry, please say that again")
            return "None"
        return statement

porcupine = None
pa = None
audio_stream = None

try:
    porcupine = pvporcupine.create(keywords=["computer", "jarvis"])

    pa = pyaudio.PyAudio()

    audio_stream = pa.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length)

    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:
            print("Hotword Detected")
            speak("Computer online")
            wishMe()

            if __name__=='__main__':

                while True:
                    help=['How can I help you?', 'What can I do for you today?', 'May I be of service?', 'How might I assist you, sir']
                    rand_help = random.choice(help)
                    speak(rand_help)
                    print(rand_help)
                    statement = takeCommand().lower()
                    if statement==0:
                        continue
                    time.sleep(5)

                    if "thank you" in statement or "ok bye" in statement or "stop" in statement:
                        speak('Computer offline')
                        print('Computer offline')
                        break

                    if 'wikipedia' in statement or 'look up' in statement:
                        statement =statement.replace("wikipedia", "")
                        results = wikipedia.summary(statement, sentences=5)
                        speak("According to Wikipedia")
                        print(results)
                        speak(results)
                        break

                    elif 'open youtube' in statement:
                        webbrowser.open_new_tab("https://www.youtube.com")
                        speak("youtube is open now")
                        time.sleep(5)
                        break

                    elif 'open google' in statement:
                        webbrowser.open_new_tab("https://www.google.com")
                        speak("Google chrome is open now")
                        time.sleep(5)
                        break

                    elif 'open gmail' in statement:
                        webbrowser.open_new_tab("gmail.com")
                        speak("Google Mail open now")
                        time.sleep(5)
                        break

                    elif "weather" in statement:

                        api_key="98a7ac3b9c8c7a9f3762a0419e49345c"
                        base_url="https://api.openweathermap.org/data/2.5/weather?"
                        #lat=
                        #lon=
                        complete_url=base_url+"appid="+api_key+"&q=London,uk""&units=metric"
                        response = requests.get(complete_url)
                        x=response.json()
                        if x["cod"]!="404":
                            y=x["main"]
                            current_temperature = y["temp"]
                            current_humidiy = y["humidity"]
                            z = x["weather"]
                            weather_description = z[0]["description"]
                            speak(" The temperature is " +
                                str(current_temperature) + "degrees centigrade"
                                "\n humidity in percentage is " +
                                str(current_humidiy) +
                                "\n description  " +
                                str(weather_description))
                            print(" Temperature = " +
                                str(current_temperature) + "°C"
                                "\n humidity = " +
                                str(current_humidiy) +  "%"
                                "\n description = " +
                                str(weather_description))
                            break

                        else:
                            speak(" City Not Found ")
                            break

                    elif 'date' in statement:
                        strTime=datetime.datetime.now().strftime(f"%A %d %B %Y")
                        speak(f"it is {strTime}")
                        print(f"it is {strTime}")
                        break

                    elif 'time' in statement:
                        strTime=datetime.datetime.now().strftime("%H:%M")
                        speak(f"the time is {strTime}")
                        print(f"the time is {strTime}")
                        break

                    elif 'who are you' in statement or 'what can you do' in statement:
                        speak('I am a personal voice assistant called Computer. I am programmed to undertake tasks like'
                            'opening youtube, google, and stackoverflow, tell the date and time, search wikipedia, and tell you the weather,' 
                            'bring you the news from the Telegraph. You can also ask me computational and geographical questions')
                        break

                    elif "who made you" in statement or "who created you" in statement or "what are you" in statement:
                        speak("I was developed by Rupstar Technologies, building a better future through AI")
                        print("I was developed by Rupstar Technologies, building a better future through AI")
                        break

                    elif "open stack overflow" in statement:
                        webbrowser.open_new_tab("https://stackoverflow.com/login")
                        speak("Here is stackoverflow")
                        break

                    elif 'news' in statement:
                        news = webbrowser.open_new_tab("https://www.telegraph.co.uk/news/uk/")
                        speak('Here are some headlines from the Telegraph, happy reading')
                        #time.sleep(6)
                        break

                    elif 'joke' in statement:
                        result = pyjokes.get_joke()
                        print(result)
                        speak(result)
                        break

                    elif 'search' in statement:
                        search = statement.replace("search", "")
                        search = webbrowser.open_new_tab("https://duckduckgo.com/?q=" + search + "&t=h_&ia=web")
                        time.sleep(5)
                        break

                    elif 'ask' in statement:
                        speak('I can answer computational and geographical questions, what can I tell you?')
                        question=takeCommand()
                        app_id="4GG3K3-KYVUVKRWL7"
                        client = wolframalpha.Client('4GG3K3-KYVUVKRWL7')
                        res = client.query(question)
                        answer = next(res.results).text
                        speak(answer)
                        print(answer)
                        break

                    elif "shutdown" in statement:
                        speak("Ok , your pc will log off in 10 sec make sure you exit from all applications")
                        if porcupine is not None:
                            porcupine.delete()
                        if audio_stream is not None:
                            audio_stream.close()
                        if pa is not None:
                            pa.terminate()
                        subprocess.call(["shutdown", "/l"])
                    
                    elif "exit program" in statement:
                        speak("exiting program. I will not be available until you reanimate me")
                        if porcupine is not None:
                            porcupine.delete()
                        if audio_stream is not None:
                            audio_stream.close()
                        if pa is not None:
                            pa.terminate()
                        break

            time.sleep(3)






finally:
    if porcupine is not None:
        porcupine.delete()

    if audio_stream is not None:
        audio_stream.close()

    if pa is not None:
            pa.terminate()