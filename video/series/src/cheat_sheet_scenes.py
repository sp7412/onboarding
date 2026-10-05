from __future__ import annotations

from manim import *
from components import *

config.background_color = BG


class CallFlow(Scene):
    def construct(self):
        boxes = VGroup(*[PipelineBox(x, c, width=1.7, height=0.62) for x, c in [("audio", CYAN), ("turn", GOLD), ("model", BLUE), ("tool", GREEN), ("speak", CYAN)]])
        boxes.arrange(RIGHT, buff=0.18).scale(0.85)
        self.add(Text("ONE CALL", font_size=28, color=INK).to_edge(UP, buff=0.3), boxes)
        self.wait(1)


class TurnFlow(Scene):
    def construct(self):
        self.add(Text("TURN-TAKING", font_size=28, color=INK).to_edge(UP, buff=0.3))
        self.add(Waveform(width=10, height=1.5))
        self.add(Text("speech probability", font_size=20, color=CYAN).to_edge(DOWN, buff=0.4))
        self.wait(1)


class ArchitectureTable(Scene):
    def construct(self):
        self.add(Text("ARCHITECTURE CHOICE", font_size=28, color=INK).to_edge(UP, buff=0.3))
        headers = VGroup(*[Text(x, font_size=20, color=c) for x, c in [("cascaded", BLUE), ("speech-to-speech", GREEN), ("full duplex", GOLD)]])
        headers.arrange(RIGHT, buff=0.55).shift(DOWN * 0.3)
        self.add(headers)
        self.add(Timeline(["STT", "LLM", "TTS"], [CYAN, BLUE, CYAN], width=3).scale(0.7).shift(LEFT * 3.2 + DOWN * 1.0))
        self.add(Timeline(["audio ↔ audio"], [GREEN], width=3).scale(0.7).shift(DOWN * 1.0))
        self.add(Timeline(["live", "delegate", "commit"], [CYAN, GOLD, GREEN], width=3).scale(0.7).shift(RIGHT * 3.2 + DOWN * 1.0))
        self.wait(1)


class ControlPlane(Scene):
    def construct(self):
        self.add(Text("CONTROL PLANE", font_size=28, color=INK).to_edge(UP, buff=0.3))
        checks = VGroup(*[VGroup(Text("✓", font_size=23, color=GREEN), Text(x, font_size=21, color=INK)).arrange(RIGHT, buff=0.16) for x in ["identity", "grounding", "idempotency", "escalation", "evaluation"]])
        checks.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.add(checks)
        self.wait(1)
