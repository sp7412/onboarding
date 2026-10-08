import os
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

import nbformat

LABS = Path(__file__).resolve().parents[1] / "labs"
sys.path.insert(0, str(LABS))

import build_nb  # noqa: E402


class ColabCellTests(unittest.TestCase):
    def test_every_notebook_has_title_badge_and_current_setup_cell(self):
        for src in sorted((LABS / "src").glob("*.py")):
            nb = nbformat.read(LABS / f"{src.stem}.ipynb", as_version=4)
            title, badge, setup = nb.cells[0], nb.cells[1], nb.cells[2]
            self.assertTrue(title.source.startswith(f"# {src.stem[:2]} · "), src.stem)
            self.assertIn(f"blob/main/labs/{src.stem}.ipynb", badge.source, src.stem)
            self.assertEqual(setup.source, build_nb.colab_setup_cell(src.stem).source,
                             f"{src.stem}: rebuild notebooks with `cd labs && python build_nb.py`")
            self.assertNotIn("Colab setup", src.read_text(), "sources must stay free of generated cells")

    def test_package_map_keys_are_real_labs(self):
        prefixes = {p.stem[:2] for p in (LABS / "src").glob("*.py")}
        self.assertLessEqual(set(build_nb.COLAB_PACKAGES), prefixes)

    def test_setup_cell_is_a_no_op_outside_colab(self):
        code = build_nb.colab_setup_cell("15_llm_judge").source
        with tempfile.TemporaryDirectory() as d, mock.patch("subprocess.run") as run:
            cwd = os.getcwd()
            os.chdir(d)
            try:
                with mock.patch.dict(sys.modules, {}):
                    sys.modules.pop("google.colab", None)
                    exec(code, {})
                self.assertEqual(os.getcwd(), os.path.realpath(d))
            finally:
                os.chdir(cwd)
            run.assert_not_called()

    def test_setup_cell_in_colab_clones_installs_and_loads_secrets(self):
        code = build_nb.colab_setup_cell("15_llm_judge").source
        secrets = {"OPENAI_API_KEY": "sk-test-not-real"}

        def get(key):
            if key not in secrets:
                raise RuntimeError("SecretNotFoundError")
            return secrets[key]

        userdata = types.SimpleNamespace(get=get)
        colab = types.ModuleType("google.colab")
        colab.userdata = userdata
        google = types.ModuleType("google")
        google.colab = colab
        with tempfile.TemporaryDirectory() as d:
            repo = Path(d) / "onboarding"
            (repo / "labs").mkdir(parents=True)
            code = code.replace('"/content/onboarding"', repr(str(repo)))
            cwd, path = os.getcwd(), list(sys.path)
            env = {k: v for k, v in os.environ.items() if k not in ("OPENAI_API_KEY", "LANGSMITH_API_KEY")}
            try:
                with mock.patch.dict(sys.modules, {"google": google, "google.colab": colab}), \
                        mock.patch.dict(os.environ, env, clear=True), \
                        mock.patch("subprocess.run") as run:
                    exec(code, {})
                    self.assertEqual(os.getcwd(), os.path.realpath(repo / "labs"))
                    self.assertEqual(os.environ.get("OPENAI_API_KEY"), "sk-test-not-real")
                    self.assertNotIn("LANGSMITH_API_KEY", os.environ)
                    calls = [c.args[0] for c in run.call_args_list]
                    self.assertFalse(any("clone" in c for c in calls))   # repo already present
                    self.assertTrue(any(c[-1] == "openai" and "pip" in c for c in calls))
            finally:
                os.chdir(cwd)
                sys.path[:] = path


if __name__ == "__main__":
    unittest.main()
