import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import podcasts_to_nlm as p  # noqa: E402


class PodcastParserTests(unittest.TestCase):
    def test_parses_every_episode_in_repo(self):
        eps = p.parse_episodes(p.PROMPTS.read_text())
        self.assertEqual(len(eps), 13)
        self.assertEqual(len({e.number for e in eps}), 13)
        for e in eps:
            self.assertTrue(e.sources, e.number)
            self.assertTrue(all(s.startswith("http") for s in e.sources))
            self.assertIn(e.format, p.FORMATS.values())
            self.assertIn(e.length, p.LENGTHS.values())
            self.assertGreater(len(e.prompt), 100)

    def test_youtube_sources_use_youtube_flag(self):
        self.assertEqual(p.source_args("https://www.youtube.com/watch?v=abc")[0], "--youtube")
        self.assertEqual(p.source_args("https://example.com/a")[0], "--url")

    def test_malformed_block_fails_loudly(self):
        with self.assertRaises(ValueError):
            p.parse_episodes("```text\nEPISODE 1: X\nFormat: Deep Dive\n```")


if __name__ == "__main__":
    unittest.main()
