from __future__ import annotations

from app.planner import Scene, VideoPlanner


def test_plan_total_duration_matches_60() -> None:
    planner = VideoPlanner("config/settings.yaml")
    scenes = planner.plan_video("AI automation", "cinematic", "confident", "Founders", 60)
    assert sum(scene.duration for scene in scenes) == 60
    assert len(scenes) == 6
    assert all(isinstance(scene, Scene) for scene in scenes)
