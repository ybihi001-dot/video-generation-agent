from __future__ import annotations

from pathlib import Path
from typing import List

from moviepy.editor import AudioFileClip, concatenate_videoclips

from app.planner import Scene
from app.render import VideoRenderer


class VideoExporter:
    def __init__(self, renderer: VideoRenderer | None = None):
        self.renderer = renderer or VideoRenderer()

    def export(self, scenes: List[Scene], output_path: str | Path, audio_path: str | Path | None = None) -> Path:
        render_path = Path(output_path)
        render_path.parent.mkdir(parents=True, exist_ok=True)

        video_path = render_path.with_suffix(".tmp.mp4")
        self.renderer.write_video(scenes, video_path)

        if audio_path is not None and Path(audio_path).exists():
            final_path = render_path
            video = concatenate_videoclips(
                [self.renderer.render_scene(scene) for scene in scenes],
                method="compose",
            )
            audio = AudioFileClip(str(audio_path))
            video = video.set_audio(audio)
            video.write_videofile(str(final_path), codec="libx264", fps=self.renderer.fps, audio_codec="aac")
            if video_path.exists():
                video_path.unlink()
            return final_path

        return render_path if render_path.exists() else video_path
