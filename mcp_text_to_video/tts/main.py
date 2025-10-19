from pydub import AudioSegment
import io
from typing import Self


class AudioSynthesisPart:
    def __init__(self, text: str, audio_synthesis: AudioSegment, duration_s: float):
        self.text = text
        self.audio_synthesis = audio_synthesis
        self.duration_s = duration_s

    def save_as(self, filename: str):
        with open(filename, "wb") as out:
            audio_bytes = self.audio_synthesis.export(format="wav").read()
            out.write(audio_bytes)


class Engine:
    def __init__(self):
        self.syntheses: [AudioSynthesisPart] = []

    def synthesize(self) -> Self:
        return self

    def voices(self) -> str:
        pass

    def insert(self, text, audio_bytes: bytes):
        segment = AudioSegment.from_mp3(io.BytesIO(audio_bytes))
        self.syntheses.append(
            AudioSynthesisPart(text, segment, segment.duration_seconds)
        )

    def save_as(self, filename: str):
        with open(filename, "wb") as out:
            audio_bytes = self.combined_synthesis.export(format="wav").read()
            out.write(audio_bytes)
