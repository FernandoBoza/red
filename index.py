import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha
import ssl
from nltk import tokenize
from config import keys
import subprocess

ssl._create_default_https_context = ssl._create_unverified_context
chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate + 50)
r = sr.Recognizer()
client = wolframalpha.Client(keys.wolframalpha_api_key)
how_can_i_help_you = "./static_audio_lib/how_can_help_you.mp3"
let_me_get_that = "./static_audio_lib/let_me_get_that.mp3"

closeDownCommands = ['no', 'nope', 'close down', 'shut down', 'nevermind']
searchCommands = ['look up', 'who is', 'find me the', 'what is the', 'what\'s the', 'show me the']
mathCommands = ['what is', 'get me the']


def open_chrome(url):
    webbrowser.get(chrome_path).open(url)


def speak(content, mp3_file):
    if mp3_file is None:
        engine.say(content)
        engine.runAndWait()
    else:
        subprocess.call(["afplay", mp3_file])
    print('listening')


def listen(phrase, mp3_file):
    if mp3_file is None:
        speak(phrase)
    else:
        subprocess.call(["afplay", mp3_file])
        print('listening')
    with sr.Microphone() as source:
        audio = r.listen(source)
        print('Processing')
        try:
            run_command(r.recognize_wit(audio, key=keys.wit_api_key))
        except sr.UnknownValueError:
            print("Wit.ai could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Wit.ai service; {0}".format(e))


def run_command(command):
    print(command)
    try:
        command_query(command)
    except:
        print('Error')


def command_query(command):
    if 'who are you' in command:
        speak('I am RED, version 1.0', None)
    elif any(word in command for word in mathCommands):
        speak("Running the numbers")
        calculate(command)
    elif any(word in command for word in searchCommands):
        speak('One second, let me get that', let_me_get_that)
        search_wiki(command)
    elif any(word in command for word in closeDownCommands):
        speak('Got it, let me know if you need anything else')
        return
    listen('Anything else')


def search_wiki(command):
    search_results = wikipedia.search(command)
    if not search_results:
        print("No result from Wikipedia")
        return
    try:
        page = wikipedia.page(search_results[0])
        print(search_results)
    except wikipedia.DisambiguationError as err:
        page = wikipedia.page(err.options[0])
    wiki_summary = str(page.summary.encode('utf-8'))
    open_chrome(page.url)
    text = tokenize.sent_tokenize(wiki_summary)
    speak(text[0])
    speak('should i continue?')
    with sr.Microphone() as source:
        audio = r.listen(source)
    print('Processing')
    if r.recognize_google(audio).lower() == "yea" or "continue":
        for sentence in text[1:]:
            print(sentence)
            speak(sentence)


def calculate(command):
    for i in mathCommands:
        if i in command:
            s = command.replace(i, '')
            try:
                speak(s + ' is ' + str(eval(s)))
            except:
                search_wolfram(command)


def search_wolfram(command):
    res = client.query(command)
    output = next(res.results)
    pod = res['pod'][2]
    result = resolve_list_or_dict(pod['subpod'])
    try:
        convertedFloat = float(result.replace('...', ''))
        speak(str(round(convertedFloat, 2)))
    except:
        speak(result)
    

def resolve_list_or_dict(variable):
    if isinstance(variable, list):
        return variable[0]['plaintext']
    else:
        return variable['plaintext']


listen('How can I help you?', how_can_i_help_you)