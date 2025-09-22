from google.cloud import texttospeech
import uuid


def synthesize(text, ssml):
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", name="en-US-Chirp3-HD-Charon"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    filename = f"{uuid.uuid4()}.mp3"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to file {filename}")


def voices_available():
    client = texttospeech.TextToSpeechClient()
    with open("gcp-voices.txt", "w") as out:
        out.write(str(client.list_voices()))
