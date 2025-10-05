from llm import openai
from engines import polly


def main():
    with open("samples/news-inputs/sample-news-short.txt", "r") as input_file:
        text = input_file.read()

    result = openai.transcript(text)
    with open("gen-result-short.txt", "w") as output_file:
        output_file.write(result)

    parts = result[:10000].split("\n\n")
    polly.PollyClient().synthesize(text_bits=parts).save_as("gen-result-short.mp3")
    print("Done")


if __name__ == "__main__":
    main()
