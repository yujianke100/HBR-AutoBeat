from typing import Any, Optional

from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget

from i18n import t


class ContinuousPlayButton(QPushButton):
    """Custom button for continuous play with enabled/disabled state management."""

    def __init__(self, language: str = "zh-CN"):
        super().__init__(t("btn_continuous_play", language))
        self.language = language
        self.is_enabled_state = False
        self.game_window_recognized = False
        self.in_song_selection = False
        self._setup_styles()
        self._update_state()

    def _setup_styles(self):
        """Setup button styling for enabled and disabled states."""
        self.enabled_style = """
            QPushButton {
                background-color: rgba(100, 149, 237, 200);
                color: white;
                border: none;
                padding: 8px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(100, 149, 237, 255);
            }
            QPushButton:pressed {
                background-color: rgba(70, 130, 180, 255);
            }
        """

        self.disabled_style = """
            QPushButton {
                background-color: rgba(169, 169, 169, 100);
                color: rgba(255, 255, 255, 150);
                border: none;
                padding: 8px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(169, 169, 169, 100);
            }
        """

    def set_preconditions(self, game_window_recognized: bool, in_song_selection: bool):
        """Update preconditions for enabling the button.

        Args:
            game_window_recognized: Whether the game window has been recognized
            in_song_selection: Whether the UI is in the song selection screen
        """
        self.game_window_recognized = game_window_recognized
        self.in_song_selection = in_song_selection
        self._update_state()

    def _update_state(self):
        """Update button enabled state based on preconditions."""
        should_enable = self.game_window_recognized and self.in_song_selection
        self.is_enabled_state = should_enable

        self.setEnabled(should_enable)
        self.setStyleSheet(self.enabled_style if should_enable else self.disabled_style)

        # Set tooltip
        if not should_enable:
            self.setToolTip(t("continuous_play_disabled", self.language))
        else:
            self.setToolTip("")

    def set_language(self, language: str):
        """Update button text and tooltip when language changes."""
        self.language = language
        self.setText(t("btn_continuous_play", language))
        self._update_state()


def attach(engine: Any, overlay_window: Any):
    """Attach engine controls to the overlay window widgets.

    - Connects the overlay toggle button to engine.toggle_running
    - Adds continuous play button (disabled by default)
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

    # Create and attach continuous play button if it doesn't exist
    if not hasattr(overlay_window, "continuous_play_button"):
        try:
            language = getattr(overlay_window, "language", "zh-CN")
            overlay_window.continuous_play_button = ContinuousPlayButton(language)

            # Find the layout and insert the button
            # Typically, the button should be inserted before the return button or at the end
            if hasattr(overlay_window, "layout") and overlay_window.layout():
                layout = overlay_window.layout()
            else:
                # Try to find the main layout
                central_widget = overlay_window.centralWidget()
                if central_widget and central_widget.layout():
                    layout = central_widget.layout()
                else:
                    layout = None

            if layout:
                # Insert continuous play button before the return button if it exists
                if hasattr(overlay_window, "return_button"):
                    index = layout.indexOf(overlay_window.return_button)
                    if index >= 0:
                        layout.insertWidget(
                            index, overlay_window.continuous_play_button
                        )
                    else:
                        layout.addWidget(overlay_window.continuous_play_button)
                else:
                    layout.addWidget(overlay_window.continuous_play_button)

            # Initialize the button state (disabled by default)
            overlay_window.continuous_play_button.set_preconditions(False, False)
        except Exception:
            pass

    engine.start()


def create_auto_song_view_widget(language: str = "zh-CN") -> Optional[QWidget]:
    """Create the auto song view widget for Phase 5+.

    This function creates a container widget with the continuous play button
    and other controls needed for advanced auto song functionality.

    Args:
        language: The current language code (default: "zh-CN")

    Returns:
        A QWidget containing the auto song controls, or None if creation fails
    """
    try:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Add continuous play button
        continuous_play_button = ContinuousPlayButton(language)
        layout.addWidget(continuous_play_button)

        return widget
    except Exception:
        return None


__all__ = ["attach", "ContinuousPlayButton", "create_auto_song_view_widget"]
