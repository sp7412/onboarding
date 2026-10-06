from __future__ import annotations

import json
from pathlib import Path

from manim import *
from components import *  # noqa: F403, F405

ROOT = Path(__file__).resolve().parents[3]
TIMING = json.loads((ROOT / "video/series/build/episode-01/timing.json").read_text())["sentences"]
config.background_color = BG
config.frame_rate = 60


class PolishedEpisode01(MovingCameraScene):
    def construct(self):
        self.add(design_background())
        stages = [PipelineBox(x, c, width=1.45, height=0.62) for x, c in [("AUDIO", CYAN), ("VAD", GOLD), ("STT", BLUE), ("LLM", BLUE), ("TOOL", GREEN), ("TTS", BLUE), ("PLAY", CYAN)]]
        pipeline = VGroup(*stages).arrange(RIGHT, buff=0.12).scale(0.72).to_edge(UP, buff=0.7)
        waveform = Waveform(width=10.5, height=0.8).shift(DOWN * 0.2)
        waveform_path = waveform[0]
        playhead = Line(ORIGIN, UP * 0.9, color=CYAN, stroke_width=3).move_to(waveform.get_left())
        self.add(pipeline, waveform, playhead)
        for index, cue in enumerate(TIMING):
            duration = cue["duration"] + (0.32 if index < len(TIMING) - 1 else 0)
            stage = stages[index % len(stages)]
            card = CallCard("NARRATION", cue["text"], CYAN).scale(0.72).to_edge(DOWN, buff=0.9)
            highlight = SurroundingRectangle(stage, color=GOLD if index % 3 == 0 else CYAN, buff=0.08, stroke_width=3)
            self.play(FadeIn(card, shift=UP * 0.18), Create(highlight), Indicate(stage, color=highlight.get_color()), run_time=min(0.7, max(0.25, duration * 0.25)))
            self.play(playhead.animate.move_to(waveform_path.point_from_proportion(min(1, (index + 1) / len(TIMING)))), run_time=max(0.25, duration * 0.75), rate_func=linear)
            self.play(FadeOut(card), FadeOut(highlight), run_time=0.25)
        self.play(FadeOut(*self.mobjects), run_time=0.8)
        self.play(FadeIn(text("WHAT ADDS THE MOST LATENCY?", size=HEADING, color=INK)), run_time=0.7)
        self.wait(2)
