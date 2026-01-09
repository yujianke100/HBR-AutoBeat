"""简化的自动打歌模块 - 仅支持单曲单次模式"""

from typing import Any


def attach(engine: Any, overlay_window: Any):
    """Attach engine controls to the overlay window widgets."""
    overlay_window.engine = engine

    try:
        overlay_window.toggle_button.clicked.connect(engine.toggle_running)
    except Exception:
        pass

    # sync hold time from UI to engine if control exists
    try:
        if hasattr(overlay_window, "hold_th_input"):
            engine.hold_th = int(overlay_window.hold_th_input.value())
            overlay_window.hold_th_input.valueChanged.connect(
                lambda v: setattr(engine, "hold_th", int(v))
            )
    except Exception:
        pass

    engine.start()


__all__ = ["attach"]
