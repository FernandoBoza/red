import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './config/My Project-bd8af4dfa881.json'
from google.cloud import texttospeech
import base64


def create_google_sst(text):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.types.SynthesisInput(text=text)
    voice = texttospeech.types.VoiceSelectionParams(
            name="en-US-Wavenet-F",
            language_code='en-US', 
            ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE
        )
    audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3,
            pitch=2.0,
            speaking_rate=1.26
        )
    
    response = client.synthesize_speech(synthesis_input, voice, audio_config)
    
    with open('./static_audio_lib/how_can_help_you.mp3', 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file')

create_google_sst("how can I help you ?")