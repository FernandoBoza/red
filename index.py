import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha
import ssl
from nltk import tokenize
from config import keys

ssl._create_default_https_context = ssl._create_unverified_context
chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
engine = pyttsx3.init()
engine.setProperty('voice', "com.apple.speech.synthesis.voice.karen")
rate = engine.getProperty('rate')
engine.setProperty('rate', rate + 50)
r = sr.Recognizer()
client = wolframalpha.Client(keys.wolframalpha_api_key)

closeDownCommands = ['no', 'nope', 'close down', 'shut down', 'nevermind']
searchCommands = ['look up', 'who is', 'find me the', 'what is the', 'what\'s the', 'show me the']
mathCommands = ['what is', 'get me the']


def open_chrome(url):
    webbrowser.get(chrome_path).open(url)


def speak(content):
    engine.say(content)
    engine.runAndWait()
    print("done speaking")


def listen(phrase):
    speak(phrase)
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
    search_results = wikipedia.search(command)
    if not search_results:
        print("No result from Wikipedia")
        return
    try:
        page = wikipedia.page(search_results[0])
    except wikipedia.DisambiguationError as err:
        page = wikipedia.page(err.options[0])
    wiki_title = str(page.title.encode('utf-8'))
    wiki_summary = str(page.summary.encode('utf-8'))
    open_chrome(page.url)
    text = tokenize.sent_tokenize(wiki_summary)
    print(text[0])
    speak(text[0])
    speak('should i continue?')
    with sr.Microphone() as source:
        audio = r.listen(source)
    print('Processing')
    if r.recognize_google(audio).lower() == "yes":
        for sent in text[1:]:
            print(sent)
            speak(sent)


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
    if res['@success'] == 'false':
        print('Question cannot be resolved')
    else:
        result = ''
        pod = res['pod'][2]
        print(pod)
        if (('definition' in pod['@title'].lower()) or ('result' in pod['@title'].lower()) or (
                pod.get('@primary', 'false') == 'true')):
            result = resolve_list_or_dict(pod['subpod'])
            convertedFloat = float(result.replace('...', ''))
            final = str(round(convertedFloat, 2))
            speak(final)


def resolve_list_or_dict(variable):
    if isinstance(variable, list):
        return variable[0]['plaintext']
    else:
        return variable['plaintext']


listen('How can I help you?')
