from typing import Any


def attach(engine: Any, overlay_window: Any):
    """Attach engine controls to the overlay window widgets.

    - Connects the overlay toggle button to engine.toggle_running
    - Starts the engine thread
    """
    # attach engine reference to window for two-way interaction
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
"""Placeholder for auto song UI and logic refactor.

This module will eventually contain the secondary view for the Auto Song feature
and any UI-specific orchestration code (e.g., settings dialog, continuous-play controls).
"""


def load_auto_song_view():
    # TODO: implement the actual UI and logic separation
    return None
