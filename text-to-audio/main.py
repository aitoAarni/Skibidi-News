from gcp import synthesize, voices_available


def main():
    # with open("ssml.xml", "r") as content:
    #    ssml = content.read()

    text = "Hey everyone on TikTok, I'm GCP and I'm here to bring you Skibidi News."
    synthesize(text, None)
    # voices_available()


if __name__ == "__main__":
    main()
