from engines import main
import boto3


class PollyClient(main.Engine):
    def __init__(self):
        self.polly_client = boto3.client("polly")
        super(PollyClient, self).__init__()

    def synthesize(self, text, engine="neural", voice="Matthew", lang_code=None):
        """
        Synthesizes speech or speech marks from text, using the specified voice.

        :param text: The text to synthesize.
        :param engine: The kind of engine used: 'standard'|'neural'|'long-form'|'generative'.
        :param voice: The ID of the voice to use.
        :param audio_format: The audio format to return for synthesized speech: 'json'|'mp3'|'ogg_opus'|'ogg_vorbis'|'pcm'.
        :param lang_code: The language code of the voice to use. This has an effect
                          only when a bilingual voice is selected.
        :return: The audio stream that contains the synthesized speech and a list
                 of visemes that are associated with the speech audio.
        """
        try:
            kwargs = {
                "Engine": engine,
                "OutputFormat": "mp3",
                "Text": text,
                "VoiceId": voice,
            }
            if lang_code is not None:
                kwargs["LanguageCode"] = lang_code
            response = self.polly_client.synthesize_speech(**kwargs)
            audio_stream = response["AudioStream"]

            self.synthesis = audio_stream.read()
            return self
        except Exception:
            print("Something went wrong.")
            raise

    def voices(self):
        """
        Gets metadata about available voices.

        :return: The list of voice metadata.
        """
        try:
            response = self.polly_client.describe_voices()
            return response["Voices"]
        except Exception:
            print("Couldn't get voice metadata.")
            raise
