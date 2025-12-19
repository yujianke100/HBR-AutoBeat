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


class PlayModeSettingsDialog(QDialog):
    """Settings dialog for play mode (Phase 6 - Redesigned)."""

    PLAY_MODES = {
        "single": t("play_mode_single", "zh-CN"),
        "new_songs": t("play_mode_new_songs", "zh-CN"),
        "continuous": t("play_mode_continuous", "zh-CN"),
    }

    def __init__(
        self, language: str = "zh-CN", initial_mode: str = "single", parent=None
    ):
        super().__init__(parent)
        # Set translucent background immediately to avoid white flash
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.Window | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint
        )

        self.language = language
        # Initialize with provided settings (allows showing current settings)
        self.selected_mode = initial_mode
        self.selected_difficulty = "EASY"
        self.repeat_count = 1
        self.setWindowTitle(t("play_mode_settings_title", language))
        self.setFixedWidth(450)
        self.initUI()

    def initUI(self):
        """Initialize the settings dialog UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        main_layout.setSizeConstraint(
            QVBoxLayout.SetFixedSize
        )  # Ensure dialog resizes to fit content

        # Background widget for styling
        bg_widget = QWidget()
        bg_widget.setStyleSheet(
            "background-color: rgba(40, 40, 40, 200); border-radius: 10px;"
        )
        bg_layout = QVBoxLayout(bg_widget)
        bg_layout.setContentsMargins(15, 15, 15, 15)
        bg_layout.setSpacing(15)

        # Play mode label and dropdown
        mode_layout = QHBoxLayout()
        mode_label = QLabel(t("play_mode_label", self.language))
        mode_label.setStyleSheet("color: white; font-weight: bold; font-size: 13px;")
        mode_label.setAlignment(Qt.AlignCenter)
        mode_label.setFixedWidth(100)

        self.mode_combo = QComboBox()
        modes_text = [
            t("play_mode_single", self.language),
            t("play_mode_new_songs", self.language),
            t("play_mode_continuous", self.language),
        ]
        self.mode_combo.addItems(modes_text)
        self.mode_combo.setStyleSheet(self._get_combo_style())
        # Don't connect signal yet - will connect after all widgets are created

        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_combo, 1)
        bg_layout.addLayout(mode_layout)

        # Tooltip for new_songs mode
        self.tooltip_label = QLabel(t("play_mode_new_songs_tooltip", self.language))
        self.tooltip_label.setStyleSheet(
            "color: rgba(200, 200, 150, 200); font-size: 10px;"
            "background-color: rgba(70, 70, 0, 100); padding: 8px; border-radius: 3px;"
        )
        self.tooltip_label.setWordWrap(True)
        self.tooltip_label.setVisible(False)
        bg_layout.addWidget(self.tooltip_label)

        # Divider
        divider = QWidget()
        divider.setFixedHeight(2)
        divider.setStyleSheet("background-color: rgba(100, 149, 237, 100);")
        bg_layout.addWidget(divider)

        # Difficulty selector (only for continuous mode)
        difficulty_layout = QHBoxLayout()
        difficulty_label = QLabel(t("difficulty_label", self.language))
        difficulty_label.setStyleSheet("color: white; font-size: 12px;")
        difficulty_label.setFixedWidth(100)
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
        difficulties = ["EASY", "NORMAL", "HARD", "EXPERT"]
        try:
            index = difficulties.index(self.selected_difficulty)
            self.difficulty_combo.setCurrentIndex(index)
        except ValueError:
            self.difficulty_combo.setCurrentIndex(0)

        difficulty_layout.addWidget(difficulty_label)
        difficulty_layout.addWidget(self.difficulty_combo, 1)
        self.difficulty_widget = QWidget()
        self.difficulty_widget.setLayout(difficulty_layout)
        bg_layout.addWidget(self.difficulty_widget)

        # Repeat count
        repeat_layout = QHBoxLayout()
        repeat_label = QLabel(t("repeat_count_label", self.language))
        repeat_label.setStyleSheet("color: white; font-size: 12px;")
        repeat_label.setFixedWidth(100)
        self.repeat_spinbox = QSpinBox()
        self.repeat_spinbox.setMinimum(1)
        self.repeat_spinbox.setMaximum(999)
        self.repeat_spinbox.setValue(self.repeat_count)
        self.repeat_spinbox.setStyleSheet(self._get_spinbox_style())

        repeat_layout.addWidget(repeat_label)
        repeat_layout.addWidget(self.repeat_spinbox, 1)
        self.repeat_widget = QWidget()
        self.repeat_widget.setLayout(repeat_layout)
        bg_layout.addWidget(self.repeat_widget)

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
        bg_layout.addLayout(button_layout)

        main_layout.addWidget(bg_widget)

        # Now connect signal and set initial index after all widgets are created
        self.mode_combo.currentIndexChanged.connect(self._on_mode_changed)
        mode_keys = ["single", "new_songs", "continuous"]
        try:
            index = mode_keys.index(self.selected_mode)
            self.mode_combo.setCurrentIndex(index)
        except ValueError:
            self.mode_combo.setCurrentIndex(0)

        # Explicitly update visibility to ensure difficulty/repeat are hidden initially
        self._update_settings_visibility()

    def _get_combo_style(self) -> str:
        """Get stylesheet for combo box."""
        return """
            QComboBox {
                background-color: rgba(60, 60, 60, 200);
                color: white;
                border: 1px solid rgba(100, 149, 237, 150);
                padding: 5px;
                border-radius: 3px;
                font-size: 12px;
            }
            QComboBox::drop-down {
                background-color: rgba(100, 149, 237, 150);
            }
            QComboBox QAbstractItemView {
                background-color: rgba(60, 60, 60, 200);
                color: white;
                selection-background-color: rgba(100, 149, 237, 150);
                font-size: 12px;
            }
        """

    def _get_spinbox_style(self) -> str:
        """Get stylesheet for spinbox."""
        return """
            QSpinBox {
                background-color: rgba(60, 60, 60, 200);
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
                    background-color: rgba(0, 120, 0, 180);
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 3px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: rgba(0, 180, 0, 220);
                }
            """
        else:  # cancel
            return """
                QPushButton {
                    background-color: rgba(120, 0, 0, 180);
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 3px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: rgba(180, 0, 0, 220);
                }
            """

    def _on_mode_changed(self):
        """Handle play mode selection change."""
        self._update_settings_visibility()
        # Show tooltip for new_songs mode
        if self.mode_combo.currentIndex() == 1:
            self.tooltip_label.setVisible(True)
        else:
            self.tooltip_label.setVisible(False)

        # Adjust dialog size after visibility changes
        self.adjustSize()

    def _update_settings_visibility(self):
        """Update visibility of difficulty and repeat count settings."""
        is_continuous = self.mode_combo.currentIndex() == 2
        self.difficulty_widget.setVisible(is_continuous)
        self.repeat_widget.setVisible(is_continuous)

    def _on_ok_clicked(self):
        """Handle OK button clicked."""
        repeat_count = self.repeat_spinbox.value()
        if repeat_count < 1:
            QMessageBox.warning(
                self,
                t("validation_error_title", self.language),
                t("validation_error_repeat", self.language),
            )
            return

        # Settings are not persisted, dialog just closes
        self.accept()

    def get_settings(self) -> dict:
        """Get the configured settings."""
        mode_keys = ["single", "new_songs", "continuous"]
        difficulties = ["EASY", "NORMAL", "HARD", "EXPERT"]
        return {
            "mode": mode_keys[self.mode_combo.currentIndex()],
            "difficulty": difficulties[self.difficulty_combo.currentIndex()],
            "repeat_count": self.repeat_spinbox.value(),
        }


class ContinuousPlayButton(QPushButton):
    """Button for play mode settings with current mode display."""

    def __init__(self, language: str = "zh-CN", parent=None):
        # Initialize with default mode
        self.language = language
        self.current_mode = "single"
        button_text = self._get_button_text()
        super().__init__(button_text, parent)

        self.is_enabled_state = False
        self.game_window_recognized = False
        self.in_song_selection = False
        self.overlay_window = (
            parent  # Store reference to overlay window for UI visibility management
        )
        self._setup_styles()
        self._update_state()
        # Connect clicked signal to show settings dialog
        self.clicked.connect(self._on_clicked)

    def _get_button_text(self) -> str:
        """Get the button text based on current mode."""
        mode_names = {
            "single": t("play_mode_single", self.language),
            "new_songs": t("play_mode_new_songs", self.language),
            "continuous": t("play_mode_continuous", self.language),
        }
        display_text = mode_names.get(
            self.current_mode, t("play_mode_single", self.language)
        )
        return t("play_mode_setting_display", self.language).format(mode=display_text)

    def _on_clicked(self):
        """Handle button click - show settings dialog."""
        if not self.isEnabled():
            return
        # Show play mode settings dialog with current mode
        dialog = PlayModeSettingsDialog(self.language, self.current_mode, self.parent())
        if dialog.exec_() == QDialog.Accepted:
            # Get the selected settings from dialog
            settings = dialog.get_settings()
            self.current_mode = settings["mode"]
            self.setText(self._get_button_text())

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
        """Update preconditions for enabling the button."""
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

    def _manage_ui_visibility(self, is_playing: bool):
        """Hide or show control buttons based on playing state."""
        # Use the stored overlay_window reference
        if not self.overlay_window:
            return

        # Hide these buttons when playing (is_playing=True), show them when not playing
        buttons_to_manage = [
            "continuous_play_button",  # Play mode settings button (self)
            "help_button",  # Help button
            "return_button",  # Return to main button
        ]

        for button_name in buttons_to_manage:
            if hasattr(self.overlay_window, button_name):
                button = getattr(self.overlay_window, button_name)
                button.setVisible(not is_playing)

        # Adjust window size after hiding/showing buttons
        if hasattr(self.overlay_window, "adjustSize"):
            self.overlay_window.adjustSize()

    def set_language(self, language: str):
        """Update button text and tooltip when language changes."""
        self.language = language
        self.setText(self._get_button_text())
        self._update_state()


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

    # Create and attach continuous play button if it doesn't exist
    if not hasattr(overlay_window, "continuous_play_button"):
        try:
            language = getattr(overlay_window, "language", "zh-CN")
            overlay_window.continuous_play_button = ContinuousPlayButton(
                language, overlay_window
            )

            # Find the layout and insert the button
            if hasattr(overlay_window, "layout") and overlay_window.layout():
                layout = overlay_window.layout()
            else:
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
    """Create the auto song view widget."""
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
    "PlayModeSettingsDialog",
]
