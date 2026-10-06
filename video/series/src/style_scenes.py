from __future__ import annotations

# ruff: noqa: F403, F405
from manim import *
from components import *

config.background_color = BG
config.frame_rate = 60


class StyleFrame(MovingCameraScene):
    def construct(self):
        self.add(design_background())
        chapter = text("CHAPTER 2 · THE LATENCY WATERFALL", size=LABEL, color=GOLD).to_edge(UP, buff=0.55)
        self.play(FadeIn(chapter), run_time=0.6)
        caller = CallCard("CALLER", "my AC stopped working", CYAN).shift(LEFT * 4.2 + UP * 1.2)
        vad = PipelineBox("VAD", GOLD, width=1.65).shift(LEFT * 1.8 + UP * 1.2)
        stt = PipelineBox("STT", BLUE, width=1.65).shift(RIGHT * 0.2 + UP * 1.2)
        tool = PipelineBox("TOOL", GREEN, width=1.65).shift(RIGHT * 2.2 + UP * 1.2)
        self.play(FadeIn(caller, shift=UP * 0.2), FadeIn(vad, shift=UP * 0.2), FadeIn(stt, shift=UP * 0.2), FadeIn(tool, shift=UP * 0.2), run_time=0.7)
        for start, end, label, color in [(caller, vad, "audio", CYAN), (vad, stt, "turn", GOLD), (stt, tool, "proposal", BLUE)]:
            packet = Dot(start.get_right(), color=color, radius=0.07)
            arrow = Arrow(start.get_right(), end.get_left(), buff=0.1, stroke_color=EDGE, stroke_width=2)
            self.add(arrow)
            self.play(MoveAlongPath(packet, arrow), run_time=0.65, rate_func=smooth)
            self.remove(packet)
        waterfall = VGroup(*[LatencyBar(a, b, w, c) for a, b, w, c in [("endpointing", "120 ms", 1.3, GOLD), ("first sound", "280 ms", 2.4, BLUE), ("tool", "640 ms", 4.0, GREEN)]])
        waterfall.arrange(DOWN, aligned_edge=LEFT, buff=0.22).shift(DOWN * 1.0)
        self.play(LaggedStart(*[GrowFromCenter(x) for x in waterfall], lag_ratio=0.1), run_time=1.4)
        playhead = Line(ORIGIN, UP * 1.8, stroke_color=CYAN, stroke_width=3).move_to(waterfall[0].get_left() + LEFT * 0.15)
        self.play(Create(playhead), run_time=0.5)
        self.play(playhead.animate.shift(RIGHT * 5.0), run_time=8, rate_func=linear)
        self.play(Indicate(tool, color=GREEN), run_time=0.7)
        self.play(FadeOut(*self.mobjects), run_time=0.8)
        self.play(FadeIn(text("The caller experiences the sum.", size=HEADING, color=INK)), run_time=0.6)
        self.wait(2)


class ComponentSheet(Scene):
    def construct(self):
        self.add(design_background())
        title = text("COMPONENT LIBRARY", size=TITLE, color=INK).to_edge(UP, buff=0.45)
        items = VGroup(PipelineBox("PIPELINE", BLUE), Waveform(width=2.2, height=0.6), LatencyBar("LATENCY", "640 ms", 1.8, GOLD), CallCard("CALL", "AC stopped", CYAN), GuardBadge("APPROVED", GREEN))
        items.arrange(DOWN, buff=0.25).scale(0.7).move_to(ORIGIN)
        self.play(FadeIn(title), LaggedStart(*[FadeIn(x, shift=RIGHT * 0.2) for x in items], lag_ratio=0.1), run_time=2)
        self.wait(2)
