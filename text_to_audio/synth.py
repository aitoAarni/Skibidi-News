from engines import polly, gcp
import uuid


def main():
    text = "Hey everyone on TikTok, I'm GCP and I'm here to bring you Skibidi News."
    client = polly.PollyClient()
    filename = f"{uuid.uuid4()}.mp3"
    client.synthesize(text).save_as(filename)
    # print(client.voices())


if __name__ == "__main__":
    main()
