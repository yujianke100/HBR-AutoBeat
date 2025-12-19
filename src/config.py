"""Simple config helper."""

import json
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[1]
_CONFIG_PATH = _ROOT / "config.json"


def load_config() -> dict:
    try:
        if _CONFIG_PATH.exists():
            with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def save_config(cfg: dict) -> None:
    try:
        with open(_CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def get(key: str, default: Any = None) -> Any:
    cfg = load_config()
    return cfg.get(key, default)


def set(key: str, value: Any) -> None:
    cfg = load_config()
    cfg[key] = value
    save_config(cfg)


__all__ = ["load_config", "save_config", "get", "set"]
