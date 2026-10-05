from __future__ import annotations

from manim import *
from components import *

config.background_color = BG


class Base(Scene):
    def construct(self):
        self.camera.background_color = BG

    def hold(self, seconds: float):
        self.wait(seconds)


class Episode01(Base):
    def construct(self):
        super().construct()
        self.play(FadeIn(title_card("Voice Agents from First Principles", "01 · Anatomy of one call")))
        self.wait(4)
        self.clear()
        boxes = VGroup(*[PipelineBox(x, c) for x, c in [("audio", CYAN), ("VAD", GOLD), ("STT", BLUE), ("LLM", BLUE), ("tool", GREEN), ("TTS", BLUE), ("playout", CYAN)]])
        boxes.arrange(RIGHT, buff=0.12).scale(0.68)
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in boxes], lag_ratio=0.12), run_time=2.2)
        self.play(Create(Waveform(width=10, height=0.85).next_to(boxes, DOWN, buff=0.65)), run_time=1.2)
        self.wait(8)
        self.play(FadeOut(boxes), FadeOut(self.mobjects[-1]))
        waterfall = VGroup(*[LatencyBar(label, value, width, color) for label, value, width, color in [
            ("endpointing", "120 ms", 1.0, GOLD), ("first model sound", "280 ms", 2.3, BLUE),
            ("tool round trip", "640 ms", 3.5, GREEN), ("response + playout", "210 ms", 1.5, CYAN)]])
        waterfall.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(ORIGIN)
        self.play(LaggedStart(*[GrowFromCenter(x) for x in waterfall], lag_ratio=0.15), run_time=2)
        self.play(FadeIn(Text("perceived dead air = the sum", font_size=25, color=INK).to_edge(UP, buff=0.7)))
        self.wait(12)
        self.play(FadeOut(*self.mobjects))
        caller = CallCard("Caller", "my AC stopped working", CYAN).shift(LEFT * 3.4)
        model = CallCard("Model", "propose: find open slots", BLUE)
        app = CallCard("Application", "validate → commit", GREEN).shift(RIGHT * 3.4)
        arrow1 = ToolArrow(caller, model, "interpret")
        arrow2 = ToolArrow(model, app, "proposal", GREEN)
        self.play(FadeIn(caller), FadeIn(model), FadeIn(app), GrowArrow(arrow1[0]), FadeIn(arrow1[1]), GrowArrow(arrow2[0]), FadeIn(arrow2[1]), run_time=2)
        self.play(FadeIn(GuardBadge().next_to(app, DOWN, buff=0.35)))
        self.wait(18)
        self.play(FadeOut(*self.mobjects))
        recap = title_card("Measure every boundary", "What adds the most latency in your pipeline? → lab 08")
        self.play(FadeIn(recap), run_time=1.3)
        self.wait(13)


class Episode02(Base):
    def construct(self):
        super().construct()
        self.play(FadeIn(title_card("Voice Agents from First Principles", "02 · Turn-taking")))
        self.wait(4)
        self.clear()
        wave = Waveform(width=10, height=1.3)
        self.play(Create(wave), run_time=2)
        self.play(FadeIn(Text("8 1 7   5 5 5", font_size=34, color=INK).next_to(wave, UP, buff=0.35)))
        self.wait(11)
        self.play(FadeOut(*self.mobjects))
        p = Axes(x_range=[0, 10, 1], y_range=[0, 1, 0.2], x_length=9, y_length=3.2, axis_config={"color": EDGE})
        line = VMobject(color=CYAN).set_points_smoothly([p.c2p(x, 0.15 + (0.75 if int(x) % 3 else 0.1), 0) for x in [0,1,2,3,4,5,6,7,8,9,10]])
        self.play(Create(p), Create(line), run_time=2)
        self.play(FadeIn(Text("speech probability", font_size=23, color=CYAN).to_edge(UP, buff=0.7)))
        self.wait(13)
        self.play(FadeOut(*self.mobjects))
        cards = VGroup(CallCard("silence timer", "pause = done?", GOLD), CallCard("semantic", "thought = complete?", GREEN)).arrange(RIGHT, buff=0.55)
        self.play(FadeIn(cards), run_time=1.2)
        self.wait(14)
        self.play(FadeOut(*self.mobjects))
        self.play(FadeIn(title_card("Heard ≠ generated", "cancel, stop playout, truncate at the audio boundary")), run_time=1.2)
        self.wait(19)
        self.play(FadeOut(*self.mobjects))
        self.play(FadeIn(title_card("Two questions", "How should uncertainty change behavior?\nWhich false interruption costs the caller most?")), run_time=1.2)
        self.wait(14)


class Episode03(Base):
    def construct(self):
        super().construct()
        self.play(FadeIn(title_card("Voice Agents from First Principles", "03 · Choosing an architecture")))
        self.wait(4)
        self.clear()
        groups = VGroup(*[VGroup(Text(name, font_size=25, color=c), Timeline(labels, cols, width=3.2).scale(0.7)).arrange(DOWN, buff=0.25) for name, c, labels, cols in [
            ("cascaded", BLUE, ["STT","LLM","TTS"], [CYAN,BLUE,CYAN]),
            ("speech-to-speech", GREEN, ["audio ↔ audio"], [GREEN]),
            ("full duplex", GOLD, ["live","delegate","commit"], [CYAN,GOLD,GREEN])]])
        groups.arrange(RIGHT, buff=0.5)
        self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.2) for g in groups], lag_ratio=0.2), run_time=2)
        self.wait(18)
        self.play(FadeOut(*self.mobjects))
        rows = VGroup(*[VGroup(Text(label, font_size=19, color=INK).set_width(2.4), *[Text(v, font_size=18, color=c).set_width(1.55) for v, c in zip(values, [BLUE,GREEN,GOLD])]).arrange(RIGHT, buff=0.25) for label, values in [
            ("latency", ["higher","lower","overlap"]), ("naturalness", ["tunable","strong","strong"]),
            ("inspectability", ["high","lower","backend"]), ("modularity", ["high","lower","medium"]),
            ("cost", ["varies","audio","voice + backend"]), ("debuggability", ["high","harder","trace"])]])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16).scale(0.8)
        self.play(FadeIn(rows), run_time=1.4)
        self.wait(25)
        self.play(FadeOut(*self.mobjects))
        self.play(FadeIn(title_card("Choose for the call", "Keep the control plane in every architecture")), run_time=1.2)
        self.wait(20)


class Episode04(Base):
    def construct(self):
        super().construct()
        self.play(FadeIn(title_card("Voice Agents from First Principles", "04 · The control plane")))
        self.wait(4)
        self.clear()
        left = CallCard("Model", "propose: book Thursday", BLUE).shift(LEFT * 3.3)
        right = CallCard("Application", "validate → commit → say", GREEN).shift(RIGHT * 3.3)
        self.play(FadeIn(left), FadeIn(right), GrowArrow(ToolArrow(left, right, "proposal")[0]), run_time=1.5)
        self.play(FadeIn(GuardBadge().next_to(right, DOWN, buff=0.35)))
        self.wait(16)
        self.play(FadeOut(*self.mobjects))
        checks = VGroup(*[VGroup(Text("✓", font_size=25, color=GREEN), Text(x, font_size=22, color=INK)).arrange(RIGHT, buff=0.2) for x in ["identity", "ownership", "offered slot", "grounded address", "idempotency"]])
        checks.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.2) for x in checks], lag_ratio=0.12), run_time=1.8)
        self.wait(22)
        self.play(FadeOut(*self.mobjects))
        self.play(FadeIn(title_card("Never say booked before committed", "emergency → escalate · OOD → route · every claim → evaluate")), run_time=1.2)
        self.wait(22)
        self.play(FadeOut(*self.mobjects))
        self.play(FadeIn(title_card("The model proposes. The application decides.", "Start with labs 02 and 07")), run_time=1.2)
        self.wait(15)
