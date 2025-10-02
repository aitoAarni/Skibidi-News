from llm import openai


def main():
    with open("sample-news.txt", "r") as input_file:
        text = input_file.read()

    result = openai.transcript(text)
    with open("gen-result.txt", "w") as output_file:
        output_file.write(result)
    print(result)


if __name__ == "__main__":
    main()
