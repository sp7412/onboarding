import { url } from "../url";
export interface Explainer {
  id: string;
  title: string;
  description: string;
  videoUrl: string;
  audioUrl: string;
  posterUrl: string;
  captionsUrl: string;
  releaseUrl: string;
  length: string;
  questions: [string, string];
}

const RELEASE = "https://github.com/sp7412/onboarding/releases/download/explainer-series";
const MEDIA = url("/explainers").replace(/\/$/, "");

export const EXPLAINERS: Explainer[] = [
  {
    id: "voice-agents-01-anatomy",
    title: "Anatomy of one call",
    description: "Trace “my AC stopped working” through audio, models, tools, and playout.",
    videoUrl: `${RELEASE}/voice-agents-01-anatomy-1080p.mp4`,
    audioUrl: `${RELEASE}/voice-agents-01-anatomy.mp3`,
    posterUrl: `${MEDIA}/voice-agents-01-anatomy.png`,
    captionsUrl: `${MEDIA}/voice-agents-01-anatomy.vtt`,
    releaseUrl: RELEASE,
    length: "3:03",
    questions: ["What adds the most latency in your pipeline?", "Which boundary would you instrument first?"],
  },
  {
    id: "voice-agents-02-turn-taking",
    title: "Turn-taking",
    description: "See why pauses inside a phone number are not the end of a caller’s turn.",
    videoUrl: `${RELEASE}/voice-agents-02-turn-taking-1080p.mp4`,
    audioUrl: `${RELEASE}/voice-agents-02-turn-taking.mp3`,
    posterUrl: `${MEDIA}/voice-agents-02-turn-taking.png`,
    captionsUrl: `${MEDIA}/voice-agents-02-turn-taking.vtt`,
    releaseUrl: RELEASE,
    length: "2:46",
    questions: ["How should uncertainty about turn completion change behavior?", "Which false interruption costs the caller most?"],
  },
  {
    id: "voice-agents-03-architecture",
    title: "Choosing an architecture",
    description: "Compare cascaded, speech-to-speech, and full-duplex delegation for a booking call.",
    videoUrl: `${RELEASE}/voice-agents-03-architecture-1080p.mp4`,
    audioUrl: `${RELEASE}/voice-agents-03-architecture.mp3`,
    posterUrl: `${MEDIA}/voice-agents-03-architecture.png`,
    captionsUrl: `${MEDIA}/voice-agents-03-architecture.vtt`,
    releaseUrl: RELEASE,
    length: "3:21",
    questions: ["Which trade-off dominates this specific use case?", "What must stay inspectable before speech is played?"],
  },
  {
    id: "voice-agents-04-control-plane",
    title: "The control plane",
    description: "The model proposes; the application owns identity, policy, state, and claims.",
    videoUrl: `${RELEASE}/voice-agents-04-control-plane-1080p.mp4`,
    audioUrl: `${RELEASE}/voice-agents-04-control-plane.mp3`,
    posterUrl: `${MEDIA}/voice-agents-04-control-plane.png`,
    captionsUrl: `${MEDIA}/voice-agents-04-control-plane.vtt`,
    releaseUrl: RELEASE,
    length: "3:16",
    questions: ["Which checks must remain outside the model?", "How will repeat trials prove the workflow stayed legal?"],
  },
];

export function validateExplainers(items: Explainer[] = EXPLAINERS): void {
  if (new Set(items.map((item) => item.id)).size !== items.length) throw new Error("Explainer IDs must be unique");
  for (const item of items) {
    if (!item.videoUrl.endsWith("-1080p.mp4") || !item.audioUrl.endsWith(".mp3") || !item.posterUrl.endsWith(".png") || !item.captionsUrl.endsWith(".vtt")) {
      throw new Error(`Invalid explainer asset paths for ${item.id}`);
    }
    if (item.questions.length !== 2) throw new Error(`Explainer ${item.id} needs two questions`);
  }
}

validateExplainers();
