from typing import Self
from pydub import AudioSegment
import io


class Engine:
    def __init__(self):
        # The combines synthesis of all parts.
        self.combined_synthesis: bytes = None

        # TTS engines support only a certain amount of chars,
        # so we split the input and store each mp3 bytes in a list.
        self.syntheses: [bytes] = []

    def synthesize(self) -> Self:
        return self

    def voices(self) -> str:
        pass

    def combine_syntheses(self) -> Self:
        self.combined_synthesis = b"".join(self.syntheses)

        combination = None
        for s in self.syntheses:
            sound = AudioSegment.from_mp3(io.BytesIO(s))
            if combination is None:
                combination = sound
            else:
                combination += AudioSegment.silent(duration=1000)
                combination += sound

        self.combined_synthesis = combination.export(format="mp3").read()
        self.syntheses = []
        return self

    def save_as(self, filename: str):
        if self.combined_synthesis is None and len(self.syntheses) > 0:
            self.combine_syntheses()

        with open(filename, "wb") as out:
            out.write(self.combined_synthesis)

    def get_bytes(self) -> bytes:
        if self.combined_synthesis is None and len(self.syntheses) > 0:
            self.combine_syntheses()

        return self.combined_synthesis
