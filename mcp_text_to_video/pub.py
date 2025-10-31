from socials.youtube import upload


def main(
    video_id: str,
    video_title: str,
    video_description: str,
    keywords: str,
    privacy_status: str,
) -> bool:
    """Publish a locally stored video with given ID to YouTube as YouTube Shorts.

    Args:
        video_id: Video ID which to publish.
        video_title: Title of the video.
        video_description: Description of the video.
        keywords: comma-separated string of keywords, e.g. "keyword1,keyword2,keyword3"
    """
    upload(
        f"results/{video_id}.mp4",  # Make sure this is ≤60s and vertical/square format
        video_title,
        video_description,
        keywords,
        privacy_status="unlisted",
    )


if __name__ == "__main__":
    main(
        "2a454f7d-0bb1-4e58-843a-39831c2ffdce",
        "Todays News",
        "This is the news description",
        "news,updates,headlines",
        "unlisted",
    )
