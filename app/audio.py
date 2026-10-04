from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip

from app.planner import Scene


class VideoRenderer:
    def __init__(self, width: int = 1280, height: int = 720, fps: int = 24):
        self.width = width
        self.height = height
        self.fps = fps

    def render_scene(self, scene: Scene, accent: tuple[int, int, int] = (76, 160, 255)) -> np.ndarray:
        image = Image.new("RGB", (self.width, self.height), color=(15, 18, 30))
        draw = ImageDraw.Draw(image)

        draw.rounded_rectangle((80, 80, self.width - 80, self.height - 80), radius=28, fill=(28, 34, 52))
        draw.rounded_rectangle((100, 100, self.width - 100, 160), radius=18, fill=accent)

        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 54)
        body_font = ImageFont.truetype("DejaVuSans.ttf", 32)
        small_font = ImageFont.truetype("DejaVuSans.ttf", 20)

        draw.text((130, 115), scene.title.upper(), font=title_font, fill=(255, 255, 255))
        draw.text((120, 220), scene.text, font=body_font, fill=(240, 244, 255))

        visual_lines = scene.visual.split(" ")
        wrapped_visual = self._wrap_text(visual_lines, 32)
        y = 300
        for line in wrapped_visual[:4]:
            draw.text((120, y), line, font=small_font, fill=(150, 180, 255))
            y += 34

        script_lines = self._wrap_text(scene.script.split(" "), 33)
        y = 470
        for line in script_lines[:3]:
            draw.text((120, y), line, font=body_font, fill=(230, 230, 230))
            y += 40

        time_label = f"00:{scene.duration:02d}"
        draw.text((self.width - 180, self.height - 80), time_label, font=small_font, fill=(180, 200, 255))

        return np.array(image)

    def render_plan(self, scenes: List[Scene]) -> List[np.ndarray]:
        frames: List[np.ndarray] = []
        for index, scene in enumerate(scenes):
            accent = (76 + index * 25, 160 - index * 10, 255)
            for _ in range(self.fps * scene.duration):
                frames.append(self.render_scene(scene, accent=accent))
        return frames

    def write_video(self, scenes: List[Scene], output_path: str | Path) -> Path:
        frames = self.render_plan(scenes)
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        clip = ImageSequenceClip(frames, fps=self.fps)
        clip.write_videofile(str(path), codec="libx264", fps=self.fps)
        return path

    @staticmethod
    def _wrap_text(words: list[str], max_chars: int) -> list[str]:
        lines: list[str] = []
        current = ""
        for word in words:
            if len(current) + len(word) + 1 <= max_chars:
                current = f"{current} {word}".strip()
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines
