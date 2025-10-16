from socials.youtube import upload_shorts


def main():
    # Regular YouTube video upload
    # upload(
    #     file_path="./bbb.mp4",
    #     video_title="Test Video Title",
    #     video_description="This is a test video description.",
    #     keywords="test,video,upload",
    #     video_category="22",
    #     privacy_status="unlisted",
    # )

    # YouTube Shorts upload example
    upload_shorts(
        file_path="./bbb.mp4",  # Make sure this is ≤60s and vertical/square format
        video_title="My YouTube Short",
        video_description="This is a test YouTube Short! 🎬",
        keywords="shorts,test,vertical,video",
        privacy_status="unlisted",
    )


if __name__ == "__main__":
    main()
