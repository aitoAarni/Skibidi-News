from engines import polly, gcp
import uuid


def main():
    with open("gen-result.txt", "r") as input_file:
        text = input_file.read()

    parts = text.split("\n\n")

    identifier = uuid.uuid4()
    for i, part in enumerate(parts):
        # text = "Hey everyone on TikTok, I'm GCP and I'm here to bring you Skibidi News."
        client = polly.PollyClient()
        filename = f"{i}-{identifier}.mp3"
        client.synthesize(part.strip()).save_as(filename)
        print(client.voices())


if __name__ == "__main__":
    main()
