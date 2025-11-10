from tts.main import Engine
from moviepy import (
    VideoFileClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
)
from uuid import uuid4
import os
import re


videos = {
    "subway-surfers": "video/ss.mp4",
    "big-buck-bunny": "video/bbb.mp4",
}


def combine_audio_and_video(audio_client: Engine, background_video: str) -> str:
    audio_text_clips = []
    total_duration = 0
    for audio_synthesis in audio_client.syntheses:
        audio_id = f"{uuid4()}.mp3"
        audio_synthesis.save_as(audio_id)
        audio_clip = AudioFileClip(audio_id)

        # Make all chars in captions UPPER CASE
        # Remove all special characters
        all_text = audio_synthesis.text.upper()
        re.sub("[^A-Z0-9 ]+", "", all_text)

        # Cut off 25ms from the end of audio clips to reduce breaks.
        end_cutoff = 0.025

        clip = (
            TextClip(
                font="./fonts/Super_Joyful.ttf",
                text=all_text,
                font_size=35,
                color="orange",
                size=(550, None),  # Width constraint for text wrapping
                margin=(10, 10),
                method="caption",  # Enable text wrapping
                stroke_color="black",  # Add black outline for better readability
                stroke_width=5,
            )
            .with_duration(audio_synthesis.duration_s - end_cutoff)
            .with_position("center")
            .with_audio(audio_clip[:-end_cutoff])
        )

        os.remove(audio_id)

        total_duration += clip.duration
        if total_duration < 60:
            audio_text_clips.append(clip)
        else:
            break

    # Concatenate audio
    audio_text = concatenate_videoclips(audio_text_clips).with_position(
        ("center", "center")
    )

    print(f"The duration of the output is {audio_text.duration}s")

    background_video_path = videos.get(background_video, videos["subway-surfers"])
    video_clip = VideoFileClip(background_video_path).with_audio(None)

    final_video = CompositeVideoClip([video_clip[0 : audio_text.duration], audio_text])
    final_id = uuid4()

    if not os.path.exists("results"):
        os.makedirs("results")

    final_video.write_videofile(f"results/{final_id}.mp4")
    return final_id
