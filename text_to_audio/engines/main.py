from typing import Self


class Engine:
    def __init__(self):
        self.synthesis: bytes = None

    def synthesize(self) -> Self:
        return self

    def voices(self) -> str:
        pass

    def save_as(self, filename: str):
        with open(filename, "wb") as out:
            out.write(self.synthesis)

    def get_bytes(self) -> bytes:
        return self.synthesis
