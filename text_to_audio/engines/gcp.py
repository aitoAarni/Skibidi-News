from engines import main
from google.cloud import texttospeech


class GoogleTextToSpeechClient(main.Engine):
    def __init__(self):
        self.gcp_tts_client = texttospeech.TextToSpeechClient()
        super(GoogleTextToSpeechClient, self).__init__()

    def synthesize(self, text, voice="en-US-Chirp3-HD-Charon", lang_code="en-US"):
        try:
            input_text = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(
                language_code=lang_code, name=voice
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            response = self.gcp_tts_client.synthesize_speech(
                input=input_text, voice=voice, audio_config=audio_config
            )

            self.synthesis = response.audio_content
            return self
        except Exception:
            print("Something went wrong.")
            raise

    def voices(self):
        try:
            return str(self.gcp_tts_client.list_voices())
        except Exception:
            print("Something went wrong.")
            raise
