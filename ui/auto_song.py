from typing import Any, Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from i18n import t
from src.config import get, set


class ContinuousPlaySettingsDialog(QDialog):
    """Settings dialog for continuous play mode (Phase 6)."""

    def __init__(self, language: str = "zh-CN", parent=None):
        super().__init__(parent)
        self.language = language
        self.play_new_songs = False
        self.continuous_play = False
        self.selected_difficulty = get("continuous_play_difficulty", "EASY")
        self.repeat_count = get("continuous_play_repeat_count", 1)
        self.setWindowTitle(t("continuous_play_settings_title", language))
        self.setWindowFlags(
            Qt.Window | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedWidth(400)
        self.initUI()

    def initUI(self):
        """Initialize the settings dialog UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(12)

        # Title/Hint
        hint_label = QLabel(t("continuous_play_hint", self.language))
        hint_label.setStyleSheet(
            "color: white; font-weight: bold; background-color: rgba(0, 0, 0, 150);"
            "padding: 8px; border-radius: 3px;"
        )
        main_layout.addWidget(hint_label)

        # Toggle A: Play new songs
        self.toggle_a = self._create_toggle_button(
            t("continuous_play_toggle_a", self.language)
        )
        self.toggle_a.clicked.connect(self._on_toggle_a_clicked)
        main_layout.addWidget(self.toggle_a)

        # Toggle B: Continuous play
        self.toggle_b = self._create_toggle_button(
            t("continuous_play_toggle_b", self.language)
        )
        self.toggle_b.clicked.connect(self._on_toggle_b_clicked)
        main_layout.addWidget(self.toggle_b)

        # Divider
        divider = QWidget()
        divider.setFixedHeight(2)
        divider.setStyleSheet("background-color: rgba(100, 149, 237, 100);")
        main_layout.addWidget(divider)

        # Difficulty selector
        difficulty_layout = QHBoxLayout()
        difficulty_label = QLabel(t("difficulty_label", self.language))
        difficulty_label.setStyleSheet("color: white;")
        difficulty_label.setFixedWidth(80)
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(
            [
                t("difficulty_easy", self.language),
                t("difficulty_normal", self.language),
                t("difficulty_hard", self.language),
                t("difficulty_expert", self.language),
            ]
        )
        self.difficulty_combo.setStyleSheet(self._get_combo_style())
        # Set current difficulty
        difficulties = ["EASY", "NORMAL", "HARD", "EXPERT"]
        try:
            index = difficulties.index(self.selected_difficulty)
            self.difficulty_combo.setCurrentIndex(index)
        except ValueError:
            self.difficulty_combo.setCurrentIndex(0)

        difficulty_layout.addWidget(difficulty_label)
        difficulty_layout.addWidget(self.difficulty_combo, 1)
        main_layout.addLayout(difficulty_layout)

        # Repeat count
        repeat_layout = QHBoxLayout()
        repeat_label = QLabel(t("repeat_count_label", self.language))
        repeat_label.setStyleSheet("color: white;")
        repeat_label.setFixedWidth(80)
        self.repeat_spinbox = QSpinBox()
        self.repeat_spinbox.setMinimum(1)
        self.repeat_spinbox.setMaximum(999)
        self.repeat_spinbox.setValue(self.repeat_count)
        self.repeat_spinbox.setStyleSheet(self._get_spinbox_style())

        repeat_layout.addWidget(repeat_label)
        repeat_layout.addWidget(self.repeat_spinbox, 1)
        main_layout.addLayout(repeat_layout)

        # Buttons
        button_layout = QHBoxLayout()
        ok_button = QPushButton(t("btn_ok", self.language))
        ok_button.setStyleSheet(self._get_button_style("ok"))
        ok_button.clicked.connect(self._on_ok_clicked)

        cancel_button = QPushButton(t("btn_cancel", self.language))
        cancel_button.setStyleSheet(self._get_button_style("cancel"))
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        main_layout.addLayout(button_layout)

        # Initially disable settings when no toggle is selected
        self._update_settings_enabled()

    def _create_toggle_button(self, text: str) -> QPushButton:
        """Create a styled toggle button."""
        button = QPushButton(text)
        button.setCheckable(True)
        button.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(100, 149, 237, 100);
                color: white;
                border: 2px solid rgba(100, 149, 237, 100);
                padding: 10px;
                border-radius: 5px;
                text-align: left;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(100, 149, 237, 150);
            }
            QPushButton:checked {
                background-color: rgba(100, 149, 237, 200);
                border: 2px solid rgba(70, 130, 180, 200);
            }
        """
        )
        button.setMinimumHeight(45)
        return button

    def _get_combo_style(self) -> str:
        """Get stylesheet for combo box."""
        return """
            QComboBox {
                background-color: rgba(40, 40, 40, 200);
                color: white;
                border: 1px solid rgba(100, 149, 237, 150);
                padding: 5px;
                border-radius: 3px;
            }
            QComboBox::drop-down {
                background-color: rgba(100, 149, 237, 150);
            }
            QComboBox QAbstractItemView {
                background-color: rgba(40, 40, 40, 200);
                color: white;
                selection-background-color: rgba(100, 149, 237, 150);
            }
        """

    def _get_spinbox_style(self) -> str:
        """Get stylesheet for spinbox."""
        return """
            QSpinBox {
                background-color: rgba(40, 40, 40, 200);
                color: white;
                border: 1px solid rgba(100, 149, 237, 150);
                padding: 5px;
                border-radius: 3px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: rgba(100, 149, 237, 150);
            }
        """

    def _get_button_style(self, btn_type: str) -> str:
        """Get stylesheet for OK/Cancel buttons."""
        if btn_type == "ok":
            return """
                QPushButton {
                    background-color: rgba(0, 100, 0, 150);
                    color: white;
                    border: none;
                    padding: 8px;
                    border-radius: 3px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: rgba(0, 150, 0, 200);
                }
            """
        else:  # cancel
            return """
                QPushButton {
                    background-color: rgba(100, 0, 0, 150);
                    color: white;
                    border: none;
                    padding: 8px;
                    border-radius: 3px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: rgba(150, 0, 0, 200);
                }
            """

    def _on_toggle_a_clicked(self):
        """Handle Toggle A (Play new songs) clicked."""
        if self.toggle_a.isChecked():
            self.toggle_b.setChecked(False)
            self.play_new_songs = True
            self.continuous_play = False
        else:
            self.play_new_songs = False
        self._update_settings_enabled()

    def _on_toggle_b_clicked(self):
        """Handle Toggle B (Continuous play) clicked."""
        if self.toggle_b.isChecked():
            self.toggle_a.setChecked(False)
            self.continuous_play = True
            self.play_new_songs = False
        else:
            self.continuous_play = False
        self._update_settings_enabled()

    def _update_settings_enabled(self):
        """Update whether detailed settings are enabled."""
        enabled = self.play_new_songs or self.continuous_play
        self.difficulty_combo.setEnabled(enabled)
        self.repeat_spinbox.setEnabled(enabled)

    def _on_ok_clicked(self):
        """Handle OK button clicked."""
        # Validate inputs
        if not self.play_new_songs and not self.continuous_play:
            QMessageBox.warning(
                self,
                t("validation_error_title", self.language),
                "请选择至少一个模式",
            )
            return

        repeat_count = self.repeat_spinbox.value()
        if repeat_count < 1:
            QMessageBox.warning(
                self,
                t("validation_error_title", self.language),
                t("validation_error_repeat", self.language),
            )
            return

        # Save settings to config
        difficulties = ["EASY", "NORMAL", "HARD", "EXPERT"]
        selected_difficulty = difficulties[self.difficulty_combo.currentIndex()]
        set("continuous_play_difficulty", selected_difficulty)
        set("continuous_play_repeat_count", repeat_count)
        set("continuous_play_new_songs", self.play_new_songs)
        set("continuous_play_continuous", self.continuous_play)

        self.accept()

    def get_settings(self) -> dict:
        """Get the configured settings."""
        difficulties = ["EASY", "NORMAL", "HARD", "EXPERT"]
        return {
            "play_new_songs": self.play_new_songs,
            "continuous_play": self.continuous_play,
            "difficulty": difficulties[self.difficulty_combo.currentIndex()],
            "repeat_count": self.repeat_spinbox.value(),
        }


class ContinuousPlayButton(QPushButton):
    """Custom button for continuous play with enabled/disabled state management."""

    def __init__(self, language: str = "zh-CN", parent=None):
        super().__init__(t("btn_continuous_play", language), parent)
        self.language = language
        self.is_enabled_state = False
        self.game_window_recognized = False
        self.in_song_selection = False
        self._setup_styles()
        self._update_state()
        # Connect clicked signal to show settings dialog
        self.clicked.connect(self._on_clicked)

    def _on_clicked(self):
        """Handle button click - show settings dialog."""
        if not self.isEnabled():
            return
        # Show continuous play settings dialog
        dialog = ContinuousPlaySettingsDialog(self.language, self.parent())
        if dialog.exec_() == QDialog.Accepted:
            # Settings were saved by the dialog
            pass

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


__all__ = [
    "attach",
    "ContinuousPlayButton",
    "create_auto_song_view_widget",
    "ContinuousPlaySettingsDialog",
]
