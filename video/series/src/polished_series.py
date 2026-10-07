from __future__ import annotations
import json
from pathlib import Path
from manim import *
from components import *  # noqa: F403, F405

ROOT = Path(__file__).resolve().parents[3]
config.background_color = BG; config.frame_rate = 60
EP = {"01":"anatomy", "02":"turn-taking", "03":"architecture", "04":"control-plane"}

class PolishedEpisode(MovingCameraScene):
    def construct(self):
        number = self.__class__.__name__[-2:]; base=f"voice-agents-{number}-{EP[number]}"
        cues=json.loads((ROOT/f"video/series/build/{base}/timing.json").read_text())["sentences"]
        self.add(design_background())
        stages = [PipelineBox(x,c,width=1.4,height=.6) for x,c in [("AUDIO",CYAN),("TURN",GOLD),("MODEL",BLUE),("TOOL",GREEN),("SPEAK",CYAN)]]
        pipeline=VGroup(*stages).arrange(RIGHT,buff=.15).scale(.72).to_edge(UP,buff=.65); self.add(pipeline)
        line=Line(LEFT*5,RIGHT*5,color=EDGE,stroke_width=2).shift(DOWN*.15); playhead=Line(ORIGIN,UP*.65,color=CYAN,stroke_width=3).move_to(line.get_left()); self.add(line,playhead)
        for i,cue in enumerate(cues):
            card=CallCard("NARRATION",cue["text"],CYAN).scale(.7).to_edge(DOWN,buff=.85)
            stage=stages[i%len(stages)]
            if number=="02": color=GOLD if i%2 else CYAN
            elif number=="03": color=[BLUE,GREEN,GOLD][i%3]
            elif number=="04": color=GREEN if i%3 else RED
            else: color=CYAN
            mark=SurroundingRectangle(stage,color=color,buff=.08,stroke_width=3)
            self.play(FadeIn(card,shift=UP*.15),Create(mark),run_time=.35)
            self.play(playhead.animate.move_to(line.point_from_proportion(min(1,(i+1)/len(cues)))),run_time=max(.25,cue["duration"]-.35),rate_func=linear)
            self.play(FadeOut(card),FadeOut(mark),run_time=.2)
        self.play(FadeOut(*self.mobjects),run_time=.5)
        self.play(FadeIn(text({"01":"WHAT ADDS THE MOST LATENCY?","02":"HEARD IS NOT THE SAME AS GENERATED","03":"CHOOSE FOR THE CALL","04":"THE MODEL PROPOSES. THE APPLICATION DECIDES."}[number],size=HEADING,color=INK)),run_time=.5)
        self.wait(1)

for n in EP:
    globals()[f"PolishedEpisode{n}"] = type(f"PolishedEpisode{n}",(PolishedEpisode,),{})
