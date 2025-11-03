from tts.main import Engine
from google.cloud import texttospeech


class GoogleTextToSpeechClient(Engine):
    def __init__(self):
        self.gcp_tts_client = texttospeech.TextToSpeechClient()
        super(GoogleTextToSpeechClient, self).__init__()

    def synthesize(self, text, voice="en-US-Chirp3-HD-Charon", lang_code="en-US"):
        parts = text[:5000].split("\n")

        for part in parts:
            if len(part) == 0:
                continue
            try:
                input_text = texttospeech.SynthesisInput(text=part)
                voice_params = texttospeech.VoiceSelectionParams(
                    language_code=lang_code, name=voice
                )
                audio_config = texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.MP3
                )

                response = self.gcp_tts_client.synthesize_speech(
                    input=input_text, voice=voice_params, audio_config=audio_config
                )

                self.insert(part, response.audio_content)
            except Exception:
                raise
        return self

    def voices(self):
        try:
            return str(self.gcp_tts_client.list_voices())
        except Exception:
            raise
