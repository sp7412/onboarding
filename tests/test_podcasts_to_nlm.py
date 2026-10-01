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


class ListenLineTests(unittest.TestCase):
    DOC = ("## Episode 1: One\n- [ ] Generated · [ ] Listened · **When:** now\n\n```text\nx\n```\n"
           "## Episode 2: Two\n- [ ] Generated · [ ] Listened · **When:** later\n")

    def test_inserts_and_replaces_listen_line(self):
        once = p.update_listen_lines(self.DOC, {1: {"audio": "https://e.com/a.m4a"}})
        self.assertIn("- **Listen:** [Episode 1 audio (m4a)](https://e.com/a.m4a)", once)
        self.assertEqual(once.count("**Listen:**"), 1)
        twice = p.update_listen_lines(once, {1: {"audio": "https://e.com/b.m4a", "notebook": "https://n.com/x"}})
        self.assertEqual(twice.count("**Listen:**"), 1)
        self.assertIn("b.m4a", twice)
        self.assertIn("[NotebookLM notebook](https://n.com/x)", twice)
        self.assertNotIn("a.m4a", twice)

    def test_release_url(self):
        self.assertEqual(p.release_url("o/r", "episode-01.m4a"),
                         "https://github.com/o/r/releases/download/podcasts/episode-01.m4a")


class RunResumeTests(unittest.TestCase):
    def setUp(self):
        import json
        import os
        import stat
        import tempfile
        self.tmp = tempfile.mkdtemp()
        self.log = os.path.join(self.tmp, "calls.log")
        fake = os.path.join(self.tmp, "nlm")
        with open(fake, "w") as f:
            f.write("#!/bin/sh\n"
                    f"echo \"$*\" >> {self.log}\n"
                    "case \"$1 $2\" in\n"
                    "  \"notebook create\") echo '{\"notebook_id\":\"nb-1\"}';;\n"
                    "  \"audio create\") [ -f " + os.path.join(self.tmp, "quota") + " ] && echo 'RPC rate limit (RESOURCE_EXHAUSTED)' >&2 && exit 1; echo ok;;\n"
                    "esac\n")
        os.chmod(fake, os.stat(fake).st_mode | stat.S_IEXEC)
        self.fake = fake
        self.json = json
        self._state = p.STATE
        p.STATE = p.Path(self.tmp) / "state.json"

    def tearDown(self):
        p.STATE = self._state

    def _calls(self):
        with open(self.log) as f:
            return f.read().splitlines()

    def test_quota_then_resume_reuses_notebook(self):
        open(p.Path(self.tmp) / "quota", "w").close()
        rc = p.main(["--run", "--episodes", "1,2", "--nlm", self.fake, "--delay", "0"])
        self.assertEqual(rc, 1)
        calls = self._calls()
        self.assertEqual(sum(c.startswith("audio create") for c in calls), 1)  # stops after the limit
        (p.Path(self.tmp) / "quota").unlink()
        open(self.log, "w").close()
        rc = p.main(["--run", "--episodes", "1", "--nlm", self.fake, "--delay", "0"])
        self.assertEqual(rc, 0)
        calls = self._calls()
        self.assertFalse(any(c.startswith("notebook create") for c in calls))  # reused
        self.assertFalse(any(c.startswith("source add") for c in calls))       # no duplicate sources
        self.assertEqual(sum(c.startswith("audio create") for c in calls), 1)


if __name__ == "__main__":
    unittest.main()
