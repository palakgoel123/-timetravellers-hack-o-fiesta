import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

listener = sr.Recognizer()
alengine = pyttsx3.init()
voices = alengine.getProperty('voices')
alengine.setProperty('voice', voices[1].id)
alengine.say('I am your Alexa')
alengine.say('How can i help you')
alengine.runAndWait()
def talk(text):
    alengine.say(text)
    alengine.runAndWait()

def take_command():
     try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa','yes')
                print(command)
                talk(command)
            else:
                print(command)
     except:
        pass
     return command

def run_alexa():
    command = take_command()
    if 'play' in command:
        song = command.replace('play','')
        talk('playing'+song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time =datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        talk('Current time is' + time)
    elif 'who the heck is' in command:
        person = command.replace('who the heck is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)
    elif 'date' in command:
        talk('sorry, I have a Headache')
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    else:
       talk('please say again')

while True:
    run_alexa()
