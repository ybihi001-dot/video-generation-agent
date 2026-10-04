from __future__ import annotations

from pathlib import Path

try:
    from gtts import gTTS
except ImportError:  # pragma: no cover
    gTTS = None


class AudioSynth:
    def __init__(self, language: str = "en"):
        self.language = language

    def generate_voiceover(self, script: str, output_path: str | Path) -> str | None:
        if gTTS is None:
            return None

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        tts = gTTS(text=script, lang=self.language, slow=False)
        tts.save(str(path))
        return str(path)
