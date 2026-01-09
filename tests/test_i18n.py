import os
import sys

# ensure project root is on sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from i18n import t  # noqa: E402


def test_i18n_basic_keys():
    # verify that known keys return translations for supported langs
    assert isinstance(t("app_title", "zh-CN"), str)
    assert "HBR-AutoBeat" in t("app_title", "zh-CN")
    assert isinstance(t("app_title", "en-US"), str)
    assert "HBR-AutoBeat" in t("app_title", "en-US")
