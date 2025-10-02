from engines import main
import boto3
import os


class PollyClient(main.Engine):
    def __init__(self):
        # AWS credentials and configuration from environment variables
        aws_config = {}

        # Required AWS credentials
        if os.getenv("AWS_ACCESS_KEY_ID"):
            aws_config["aws_access_key_id"] = os.getenv("AWS_ACCESS_KEY_ID")
        if os.getenv("AWS_SECRET_ACCESS_KEY"):
            aws_config["aws_secret_access_key"] = os.getenv("AWS_SECRET_ACCESS_KEY")
        if os.getenv("AWS_SESSION_TOKEN"):
            aws_config["aws_session_token"] = os.getenv("AWS_SESSION_TOKEN")

        # AWS region (default to us-east-1 if not specified)
        aws_config["region_name"] = os.getenv("AWS_REGION", "us-east-1")

        self.polly_client = boto3.client("polly", **aws_config)
        super(PollyClient, self).__init__()

    def synthesize(
        self, text, sslm=True, engine="neural", voice="Matthew", lang_code=None
    ):
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
                "TextType": "ssml" if sslm else "text",
                "VoiceId": voice,
            }
            if lang_code is not None:
                kwargs["LanguageCode"] = lang_code
            response = self.polly_client.synthesize_speech(**kwargs)
            audio_stream = response["AudioStream"]

            self.synthesis = audio_stream.read()
            return self
        except Exception:
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
            raise
