from __future__ import annotations

from manim import *  # noqa: F403

BG = "#0a1224"
PANEL = "#111c33"
EDGE = "#27385d"
INK = "#e8eefc"
DIM = "#a8b5d1"
CYAN = "#37e0ff"
BLUE = "#3e7bff"
GREEN = "#4ade80"
GOLD = "#f5c044"
RED = "#ff7a6b"


class PipelineBox(VGroup):
    def __init__(self, label: str, color: str = BLUE, width: float = 2.0, height: float = 0.72, **kwargs):
        super().__init__(**kwargs)
        self.box = RoundedRectangle(width=width, height=height, corner_radius=0.1, stroke_color=color, fill_color=PANEL, fill_opacity=1)
        self.label = Text(label, font_size=22, color=INK).scale_to_fit_width(width - 0.24)
        self.add(self.box, self.label)


class Waveform(VGroup):
    def __init__(self, width: float = 8, height: float = 1.1, color: str = CYAN, seed: int = 7, **kwargs):
        super().__init__(**kwargs)
        points = []
        for i in range(81):
            x = -width / 2 + width * i / 80
            y = (0.25 + 0.75 * abs(((i * 37 + seed * 13) % 23) - 11) / 11) * height / 2
            if i % 7 in (0, 1):
                y *= 0.28
            points.append([x, y if i % 2 else -y, 0])
        self.add(Polygon(*points, stroke_color=color, stroke_width=2, fill_opacity=0))


class Timeline(VGroup):
    def __init__(self, labels: list[str], colors: list[str] | None = None, width: float = 10, **kwargs):
        super().__init__(**kwargs)
        colors = colors or [BLUE] * len(labels)
        unit = width / len(labels)
        for i, label in enumerate(labels):
            bar = Rectangle(width=unit - 0.08, height=0.42, stroke_width=0, fill_color=colors[i], fill_opacity=0.9)
            bar.move_to([-width / 2 + unit * (i + 0.5), 0, 0])
            text = Text(label, font_size=16, color=INK).scale_to_fit_width(unit - 0.12)
            text.move_to(bar.get_center())
            self.add(VGroup(bar, text))


class LatencyBar(VGroup):
    def __init__(self, label: str, value: str, width: float = 4.2, color: str = GOLD, **kwargs):
        super().__init__(**kwargs)
        self.add(Text(label, font_size=19, color=DIM).set_width(2.55).align_to(ORIGIN, LEFT))
        bar = RoundedRectangle(width=width, height=0.24, corner_radius=0.12, stroke_width=0, fill_color=color, fill_opacity=0.9)
        bar.next_to(self[0], RIGHT, buff=0.18)
        value_text = Text(value, font_size=18, color=INK)
        value_text.next_to(bar, RIGHT, buff=0.15)
        self.add(bar, value_text)


class CallCard(VGroup):
    def __init__(self, title: str, detail: str, color: str = CYAN, **kwargs):
        super().__init__(**kwargs)
        card = RoundedRectangle(width=4.5, height=1.25, corner_radius=0.12, stroke_color=color, fill_color=PANEL, fill_opacity=1)
        heading = Text(title, font_size=22, color=color)
        body = Text(detail, font_size=18, color=INK).scale_to_fit_width(4.0)
        group = VGroup(heading, body).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        group.move_to(card.get_center())
        self.add(card, group)


class ToolArrow(VGroup):
    def __init__(self, start: Mobject, end: Mobject, label: str = "proposal", color: str = CYAN, **kwargs):
        super().__init__(**kwargs)
        arrow = Arrow(start.get_right(), end.get_left(), buff=0.1, stroke_color=color, stroke_width=3, max_tip_length_to_length_ratio=0.12)
        text = Text(label, font_size=16, color=color).next_to(arrow, UP, buff=0.08)
        self.add(arrow, text)


class GuardBadge(VGroup):
    def __init__(self, label: str = "CONTROL PLANE", color: str = GREEN, **kwargs):
        super().__init__(**kwargs)
        badge = RoundedRectangle(width=2.35, height=0.46, corner_radius=0.18, stroke_color=color, fill_color=color, fill_opacity=0.15)
        text = Text(label, font_size=16, color=color).scale_to_fit_width(2.1)
        self.add(badge, text)


def title_card(title: str, subtitle: str):
    return VGroup(Text(title, font_size=38, color=INK), Text(subtitle, font_size=22, color=CYAN)).arrange(DOWN, buff=0.22)


def footer(text: str):
    return Text(text, font_size=16, color=DIM).to_edge(DOWN, buff=0.28)
