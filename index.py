import speech_recognition as sr
import pyttsx3
import os
import webbrowser

chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
engine = pyttsx3.init()
r = sr.Recognizer()

closeDownCommands = ['no','nope','close down','nevermind']
searchCommands = ['look up', 'get me the', 'find me the', 'what\'s is the', 'what\'s the','show me the']

def speak(content):
   engine.say(content)
   engine.runAndWait()

def listen(phrase):
   speak(phrase)
   with sr.Microphone() as source:
      audio = r.listen(source)
   print('Proccessing')
   command = r.recognize_google(audio).lower()
   runCommand(command)

def runCommand(command):
   try:
      print(command)
      commandQuery(command)
   except:
      print('Error')

def commandQuery(command):
   if 'who are you' in command:
      speak('I am RED, version 1.0')
      listen('Anything else sir')
   elif any(word in command for word in searchCommands):
      speak('One second, let me get that')
      searchOnInternet(command)
   elif any(word in command for word in closeDownCommands):
      speak('Got it, let me know if you need anything else sir')

def searchOnInternet(command):
   query = command.replace(" ", "+")
   webbrowser.get(chrome_path).open('https://www.google.com/search?q='+query)

listen('Hello Sir, how can I help you')




# commandLib = []
# commandLib.append({
#    "searchCommands": ['look up', 'get me the', 'find me the', 'what is the', 'whats the','show me the'],
#    "action": searchOnInternet(command)
# })

# commandLib.append({
#    "closeDownCommands": ['no','nope','close down','nevermind'],
#    "action": speak('Got it, let me know if you need anything else sir')
# })