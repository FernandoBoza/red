import pyttsx3

voiceId = [
"com.apple.speech.synthesis.voice.karen", -
"com.apple.speech.synthesis.voice.samantha", -
]

engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voiceId:
   engine.setProperty('voice', voice)
   engine.say('The quick brown fox jumped over the lazy dog.')
engine.runAndWait()
