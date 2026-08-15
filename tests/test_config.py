import importlib.util
import pathlib
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config.py"
SPEC = importlib.util.spec_from_file_location("config_module", CONFIG_PATH)
config = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(config)


class ValidateConfigTests(unittest.TestCase):
    def test_keeps_valid_cooldown(self):
        validated = config.validateConfig({"cooldownDistance": 42})
        self.assertEqual(validated["cooldownDistance"], 42)

    def test_rejects_out_of_range_cooldown(self):
        for value in (0, -1, 1000):
            with self.subTest(value=value):
                validated = config.validateConfig({"cooldownDistance": value})
                self.assertEqual(validated["cooldownDistance"], 15)

    def test_rejects_invalid_config_shapes(self):
        for value in ({"cooldownDistance": True}, [], "", None):
            with self.subTest(value=value):
                validated = config.validateConfig(value)
                self.assertEqual(validated, config.getDefaultConfig())

    def test_rejects_blank_shortcut(self):
        for value in ("", "   "):
            with self.subTest(value=value):
                validated = config.validateConfig({"shortcutKey": value})
                self.assertEqual(validated["shortcutKey"], "Ctrl+Shift+U")

    def test_load_user_config_falls_back_for_invalid_json(self):
        with tempfile.TemporaryDirectory() as tempDir:
            config_path = pathlib.Path(tempDir) / "user_config.json"
            config_path.write_text("{bad json", encoding="utf-8")
            original_path = config.configFile
            try:
                config.configFile = str(config_path)
                self.assertEqual(config.loadUserConfig(), config.getDefaultConfig())
            finally:
                config.configFile = original_path


if __name__ == "__main__":
    unittest.main()
