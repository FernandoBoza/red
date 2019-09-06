import speech_recognition as sr
import ssl
from config import keys

ssl._create_default_https_context = ssl._create_unverified_context
r = sr.Recognizer()


def listen(phrase):
    print(phrase)
    with sr.Microphone() as source:
        audio = r.listen(source)
    print('Proccessing')
    WIT_AI_KEY = keys.wit_api_key
    try:
        print(r.recognize_wit(audio, key=WIT_AI_KEY))
    except sr.UnknownValueError:
        print("Wit.ai could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Wit.ai service; {0}".format(e))


listen("Say something")
