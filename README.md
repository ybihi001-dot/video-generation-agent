# Video Generation Agent

An expert Python agent for creating polished 1-minute videos from a short brief.

What it does:
- Converts a subject, style, tone, and audience into a script and shot plan
- Builds a 60-second scene-by-scene storyboard
- Generates visual scene cards using image rendering
- Adds optional voice-over audio from text
- Exports a final MP4 video in 16:9

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.agent --topic "AI agents for small businesses" --tone persuasive --style cinematic --audience "founders" --output outputs/demo.mp4
```

## Project structure

- `app/` — agent logic, planning, rendering, and export
- `config/` — settings and defaults
- `prompts/` — reusable instruction templates
- `tests/` — smoke tests

## Example command

```bash
python -m app.agent \
  --topic "How to launch a micro SaaS in 30 days" \
  --tone confident \
  --style modern \
  --audience "startup founders" \
  --output outputs/launch.mp4
```

## Notes

- This project is designed as a solid expert starter for 1-minute video generation.
- It includes a local rendering pipeline and optional TTS via `gTTS`.
- If you want a production version later, this structure can be extended with image generation, stock footage, or voice synthesis APIs.
