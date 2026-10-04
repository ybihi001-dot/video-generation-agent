from __future__ import annotations

from pathlib import Path
from typing import List

from moviepy.editor import AudioFileClip, VideoFileClip

from app.planner import Scene
from app.render import VideoRenderer


class VideoExporter:
    def __init__(self, renderer: VideoRenderer | None = None):
        self.renderer = renderer or VideoRenderer()

    def export(self, scenes: List[Scene], output_path: str | Path, audio_path: str | Path | None = None) -> Path:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        temp_video = output.with_suffix(".tmp.mp4")
        self.renderer.write_video(scenes, temp_video)

        if audio_path is not None and Path(audio_path).exists():
            video = VideoFileClip(str(temp_video))
            audio = AudioFileClip(str(audio_path))
            final_video = video.set_audio(audio)
            final_video.write_videofile(str(output), codec="libx264", fps=self.renderer.fps, audio_codec="aac")
            video.close()
            audio.close()
            final_video.close()
            if temp_video.exists():
                temp_video.unlink()
            return output

        if temp_video.exists():
            temp_video.rename(output)
        return output
