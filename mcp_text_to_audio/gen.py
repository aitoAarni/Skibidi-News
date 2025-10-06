from llm import openai
from engines import polly


def main():
    # with open("samples/news-inputs/demo-sample.txt", "r") as input_file:
    #    text = input_file.read()

    # result = openai.transcript(text)
    with open("demo-transcript.txt", "r") as input_file:
        result = input_file.read()

    parts = result[:10000].split("\n\n")
    polly.PollyClient().synthesize(text_bits=parts).save_as("demo.mp3")
    print("Done")


if __name__ == "__main__":
    main()
