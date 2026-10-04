from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List
import json
import yaml


@dataclass
class Scene:
    index: int
    title: str
    duration: int
    text: str
    visual: str
    script: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class VideoPlanner:
    def __init__(self, settings_path: str | Path | None = None):
        self.settings_path = Path(settings_path) if settings_path else Path("config/settings.yaml")
        self.settings = self._load_settings()

    def _load_settings(self) -> Dict[str, Any]:
        with self.settings_path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

    def plan_video(
        self,
        topic: str,
        style: str,
        tone: str,
        audience: str,
        duration_seconds: int | None = None,
    ) -> List[Scene]:
        total = duration_seconds or self.settings.get("defaults", {}).get("duration_seconds", 60)

        hook = self._hook_scene(topic, style, tone)
        intro = self._intro_scene(topic, style, tone)
        proof = self._proof_scene(topic, audience)
        value = self._value_scene(topic, audience)
        action = self._action_scene(topic, audience)
        closing = self._closing_scene(topic)

        scenes = [hook, intro, proof, value, action, closing]
        current_total = sum(scene.duration for scene in scenes)

        if current_total != total:
            delta = total - current_total
            scenes[-1] = Scene(
                index=scenes[-1].index,
                title=scenes[-1].title,
                duration=scenes[-1].duration + delta,
                text=scenes[-1].text,
                visual=scenes[-1].visual,
                script=scenes[-1].script,
            )

        return scenes

    def _hook_scene(self, topic: str, style: str, tone: str) -> Scene:
        return Scene(
            index=1,
            title="Hook",
            duration=8,
            text=f"{topic} is changing the way people work.",
            visual=f"{style.title()} opening shot with bold typography and motion arc",
            script=f"{topic} is changing the way {tone} teams create momentum.",
        )

    def _intro_scene(self, topic: str, style: str, tone: str) -> Scene:
        return Scene(
            index=2,
            title="Why it matters",
            duration=10,
            text=f"Most people are still doing {topic.lower()} the hard way.",
            visual=f"{style.title()} montage of friction, tasks, and pressure points",
            script=f"Most people are still handling {topic.lower()} the hard way, and it slows everything down.",
        )

    def _proof_scene(self, topic: str, audience: str) -> Scene:
        return Scene(
            index=3,
            title="The shift",
            duration=12,
            text=f"A smarter system turns complexity into clarity for {audience}.",
            visual="Comparison split screen showing before and after workflow",
            script=f"A smarter system turns complexity into clarity, especially for {audience} who need speed and focus.",
        )

    def _value_scene(self, topic: str, audience: str) -> Scene:
        return Scene(
            index=4,
            title="Value",
            duration=12,
            text=f"You gain better decisions, faster execution, and less operational drag.",
            visual="Product UI mockup, metrics, and workflow diagram animation",
            script=f"You gain better decisions, faster execution, and less operational drag without sacrificing quality.",
        )

    def _action_scene(self, topic: str, audience: str) -> Scene:
        return Scene(
            index=5,
            title="Next step",
            duration=10,
            text=f"Start today with a focused rollout and measurable outcomes.",
            visual="Call-to-action card with simple timeline and checklist",
            script=f"Start today with a focused rollout and measure the outcomes that matter most to {audience}.",
        )

    def _closing_scene(self, topic: str) -> Scene:
        return Scene(
            index=6,
            title="Close",
            duration=8,
            text=f"This is not a trend. It is a practical advantage.",
            visual="Final logo reveal and confident brand close-up",
            script=f"This is not a trend; it is a practical advantage for people ready to move faster.",
        )

    def export_plan(self, plan: List[Scene], path: str | Path) -> None:
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = {"scenes": [scene.to_dict() for scene in plan]}
        with output.open("w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2)
