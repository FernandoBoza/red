import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import wikipedia
from pyowm import OWM
from urllib.request import urlopen
from bs4 import BeautifulSoup
import wolframalpha
import requests
import ssl
from nltk import tokenize
from config import keys


ssl._create_default_https_context = ssl._create_unverified_context
chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
engine = pyttsx3.init()
engine.setProperty('voice', "com.apple.speech.synthesis.voice.karen")
rate = engine.getProperty('rate')
engine.setProperty('rate', rate+50)
r = sr.Recognizer()
client = wolframalpha.Client(keys.wolframalpha_api_key)

closeDownCommands = ['no','nope','close down', 'shut down','nevermind']
searchCommands = ['look up', 'who is', 'find me the', 'what is the', 'what\'s the','show me the']
mathCommands = ['what is', 'get me the']

def openChrome(url):
   webbrowser.get(chrome_path).open(url)

def speak(content):
   engine.say(content)
   engine.runAndWait()

def listen(phrase):
   speak(phrase)
   with sr.Microphone() as source:
      audio = r.listen(source)
   print('Proccessing')
   WIT_AI_KEY = keys.wit_api_key
   try:
      runCommand(r.recognize_wit(audio, key=WIT_AI_KEY))
   except sr.UnknownValueError:
      print("Wit.ai could not understand audio")
   except sr.RequestError as e:
      print("Could not request results from Wit.ai service; {0}".format(e))


def runCommand(command):
   print(command)
   try:
      commandQuery(command)
   except:
      print('Error')

def commandQuery(command):
   if 'who are you' in command:
      speak('I am RED, version 1.0')
   elif any(word in command for word in mathCommands):
      speak("Running the numbers")
      calculate(command)
   elif any(word in command for word in searchCommands):
      speak('One second, let me get that')
      search_wiki(command)
   elif any(word in command for word in closeDownCommands):
      speak('Got it, let me know if you need anything else sir')
      return
   listen('Anything else sir')


def search_wiki(command):
   searchResults = wikipedia.search(command)
   if not searchResults:
      print("No result from Wikipedia")
      return
   try:
      page = wikipedia.page(searchResults[0])
   except wikipedia.DisambiguationError as err:
      page = wikipedia.page(err.options[0])
   wikiTitle = str(page.title.encode('utf-8'))
   wikiSummary = str(page.summary.encode('utf-8'))
   openChrome(page.url)
   text = tokenize.sent_tokenize(wikiSummary)
   print(text[0])
   speak(text[0])
   speak('should i continue?')
   with sr.Microphone() as source:
      audio = r.listen(source)
   print('Proccessing')
   if r.recognize_google(audio).lower() == "yes":
      for sent in text[1:]:
         print(sent)
         speak(sent)

      


def calculate(command):
   for i in mathCommands:
      if i in command:
         s = command.replace(i, '')
         try:
            speak( s + ' is '+  str(eval(s)))
         except:
            search_wolfram(command)
  


def search_wolfram(command):
   res = client.query(command)
   if res['@success'] == 'false':
      print('Question cannot be resolved')
   else:
      result = ''
      pod = res['pod'][2]
      print(pod)
      if (('definition' in pod['@title'].lower()) or ('result' in  pod['@title'].lower()) or (pod.get('@primary','false') == 'true')):
         result = resolveListOrDict(pod['subpod'])
         convertedFloat = float(result.replace('...',''))
         final = str(round(convertedFloat, 2))
         speak(final)

def resolveListOrDict(variable):
  if isinstance(variable, list):
    return variable[0]['plaintext']
  else:
    return variable['plaintext']

# search_wiki("look up a red black tree")
listen('How can I help you?')