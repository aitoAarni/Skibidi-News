from llm import openai
from tts import polly, gcp
from video import tools


def main():
    with open("samples/news-inputs/demo-sample.txt", "r") as input_file:
        text = input_file.read()

    result = openai.transcript(text)
    with open("demo-transcript-text.txt", "w") as output_file:
        output_file.write(result)

    # with open("demo-transcript-text.txt", "r") as input_file:
    #    result = input_file.read()

    # client = gcp.GoogleTextToSpeechClient().synthesize(text=result)
    client = polly.PollyClient().synthesize(text=result)
    tools.combine_audio_and_video(client)


if __name__ == "__main__":
    main()
