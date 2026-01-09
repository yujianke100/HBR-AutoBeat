import os
from typing import Any, Dict

import yaml  # type: ignore

_LANG_CACHE: Dict[str, Any] = {}


class I18nLoader:
    def __init__(self, lang="zh-CN", i18n_dir=None):
        self.lang = lang
        self.i18n_dir = i18n_dir or os.path.join(os.path.dirname(__file__))
        self._strings = self._load_yaml(lang)

    def _load_yaml(self, lang):
        if lang in _LANG_CACHE:
            return _LANG_CACHE[lang]
        fname = (
            f"{lang}.yml"
            if os.path.exists(os.path.join(self.i18n_dir, f"{lang}.yml"))
            else f"{lang.replace('-', '_')}.yml"
        )
        path = os.path.join(self.i18n_dir, fname)
        if not os.path.exists(path):
            path = os.path.join(self.i18n_dir, "zh-CN.yml")
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        _LANG_CACHE[lang] = data
        return data

    def t(self, key, default=None):
        return self._strings.get(key, default or key)


# 用法示例：
# loader = I18nLoader(lang="zh-CN")
# loader.t("app_title")


def get_loader(lang="zh-CN"):
    return I18nLoader(lang)


def t(key, lang="zh-CN"):
    return get_loader(lang).t(key)
