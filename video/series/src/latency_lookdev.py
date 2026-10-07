# ruff: noqa: E701, E702
from __future__ import annotations

from manim import *
from components import *  # noqa: F403, F405
from manim import config

config.background_color = BLACK
config.frame_rate = 60
config.tex_template.tex_compiler = "latex"


def axes(title: str):
    ax = Axes(x_range=[0, 10, 2], y_range=[0, 1, .25], x_length=9, y_length=3.8, axis_config={"color": GREY_B, "stroke_width": 2})
    label = MathTex(title, color=WHITE, font_size=34).next_to(ax, UP, buff=.25)
    return VGroup(ax, label)


class OpeningPuzzle(Scene):
    def construct(self):
        ax = axes(r"\text{latency of one stage}")
        curve = FunctionGraph(lambda x: np.exp(-((x - 4.2) ** 2) / 2.4), x_range=[0, 9], color=BLUE_C, stroke_width=5).move_to(ax[0].c2p(4.5, .2))
        p50 = DashedLine(ax[0].c2p(4.2, 0), ax[0].c2p(4.2, .72), color=YELLOW)
        p95 = DashedLine(ax[0].c2p(7.3, 0), ax[0].c2p(7.3, .2), color=YELLOW)
        self.play(Create(ax), Create(curve), run_time=1.0)
        self.play(Create(p50), Write(MathTex(r"p50", color=YELLOW).next_to(p50, DOWN)), run_time=.6)
        self.play(Create(p95), Write(MathTex(r"p95", color=YELLOW).next_to(p95, DOWN)), run_time=.6)
        self.wait(1)


class ConvolutionMoment(Scene):
    def construct(self):
        first = axes(r"X = \text{endpointing}")
        second = axes(r"Y = \text{tool round trip}")
        total = axes(r"X + Y")
        first.shift(LEFT * 4); second.shift(RIGHT * 4)
        f1 = FunctionGraph(lambda x: np.exp(-((x - 4.0) ** 2) / 1.5), x_range=[0, 9], color=BLUE_C, stroke_width=5).move_to(first[0].c2p(4.5, .2))
        f2 = FunctionGraph(lambda x: np.exp(-((x - 5.0) ** 2) / 1.9), x_range=[0, 9], color=TEAL, stroke_width=5).move_to(second[0].c2p(4.5, .2))
        self.play(Create(first), Create(f1), Create(second), Create(f2), run_time=1.2)
        arrow = Arrow(LEFT * .7, RIGHT * .7, color=YELLOW)
        self.play(Create(arrow), run_time=.4)
        self.play(FadeOut(first, f1, second, f2, arrow), FadeIn(total), run_time=.8)
        broad = FunctionGraph(lambda x: .85 * np.exp(-((x - 5.0) ** 2) / 4.2), x_range=[0, 9], color=YELLOW, stroke_width=5).move_to(total[0].c2p(4.5, .2))
        self.play(Create(broad), run_time=1.0)
        self.play(Write(MathTex(r"X+Y", color=YELLOW).to_edge(DOWN, buff=.5)), run_time=.5)
        self.wait(1)


class P95Brace(Scene):
    def construct(self):
        bars = VGroup(*[Rectangle(width=.75, height=h, fill_color=BLUE_C, fill_opacity=.8, stroke_width=0) for h in [.5, .9, 1.4, 1.9, 2.3, 2.0, 1.3, .8, .35]])
        bars.arrange(RIGHT, buff=.08).move_to(ORIGIN)
        brace = Brace(VGroup(*bars[6:]), direction=UP, color=YELLOW)
        label = MathTex(r"p95\text{ tail}", color=YELLOW, font_size=34).next_to(brace, UP)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=.08), run_time=1.2)
        self.play(GrowFromCenter(brace), Write(label), run_time=.7)
        self.play(Indicate(VGroup(*bars[6:]), color=YELLOW), run_time=.6)
        self.wait(1)
