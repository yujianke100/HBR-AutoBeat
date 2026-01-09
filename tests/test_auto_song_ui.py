import os
import sys
from types import SimpleNamespace

# ensure project root is on sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ui.auto_song import attach  # noqa: E402


def test_attach_sets_engine_and_sync_hold():
    engine = SimpleNamespace()
    engine.hold_th = 5
    engine.start = lambda: None
    overlay = SimpleNamespace()

    # provide a mock spinbox-like object
    class MockSpin:
        def __init__(self, v=7):
            self._v = v
            self._callbacks = []

        def value(self):
            return self._v

        def valueChanged(self, cb=None):
            # mimic Qt signal connect
            if cb:
                self._callbacks.append(cb)

        def setValue(self, v):
            self._v = v
            for cb in self._callbacks:
                cb(v)

    overlay.hold_th_input = MockSpin(8)
    overlay.toggle_button = SimpleNamespace()
    # attach should set overlay.engine and update engine.hold_th
    attach(engine, overlay)
    assert hasattr(overlay, "engine")
    assert engine.hold_th == 8
