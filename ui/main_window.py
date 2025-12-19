import time
from pathlib import Path
from typing import Tuple

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from core.window_helpers import init
from i18n import t
from src.config import get, set


def get_dpi_scale_factor():
    """Get the DPI scale factor using Qt's API to match Qt's coordinate system."""
    try:
        app = QApplication.instance()
        if app:
            screen = app.primaryScreen()
            if screen:
                return screen.devicePixelRatio()
        return 1.0
    except Exception:
        return 1.0


class TransparentWindow(QMainWindow):
    def __init__(self, points, local_version=None):
        super().__init__()
        (
            client_left,
            client_top,
            client_width,
            client_height,
            y_value,
            min_x,
            max_x,
        ) = init("HeavenBurnsRed", points, test_flag=False)
        self.client_left = client_left
        self.client_top = client_top
        self.client_width = client_width
        self.client_height = client_height
        self.y_value = y_value
        self.min_x = min_x
        self.max_x = max_x
        self.language = "zh-CN"
        self.btnPosition = [None, None]
        self.local_version = local_version or "v0.0.0"
        self.initUI()

    def getWindowInfo(self) -> Tuple[int, int, int, int, int, int, int]:
        return (
            self.client_left,
            self.client_top,
            self.client_width,
            self.client_height,
            self.y_value,
            self.min_x,
            self.max_x,
        )

    def repositionWindow(self):
        (
            self.client_left,
            self.client_top,
            self.client_width,
            self.client_height,
            self.y_value,
            self.min_x,
            self.max_x,
        ) = init(
            "HeavenBurnsRed",
            [(325, 810), (575, 810), (825, 810), (1075, 810), (1325, 810), (1575, 810)],
        )
        # Adjust for DPI scaling: win32gui returns physical pixels, Qt expects logical pixels
        scale = get_dpi_scale_factor()
        logical_left = int(self.client_left / scale)
        logical_top = int((self.client_top + 150) / scale)
        self.setGeometry(logical_left, logical_top, 10, 10)

    def exitApplication(self):
        import sys

        sys.exit()

    def toggleHelp(self):
        QMessageBox.information(
            self, t("help_button", self.language), t("help", self.language)
        )

    def initUI(self):
        # `LOCAL_VERSION` is provided by caller; no global needed here
        self.setWindowFlags(
            Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        QApplication.setFont(QFont("Microsoft YaHei", 11))
        # set window icon
        # try:
        #     icon_path = Path(__file__).resolve().parents[1] / "icon" / "favicon.ico"
        #     if icon_path.exists():
        #         self.setWindowIcon(QIcon(str(icon_path)))
        # except Exception:
        #     pass
        icon_path = Path(__file__).resolve().parents[1] / "icon" / "favicon.ico"
        self.setWindowIcon(QIcon(str(icon_path)))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.setMaximumWidth(300)
        layout = QVBoxLayout(central_widget)

        self.title_bar = QWidget()
        self.title_bar_layout = QHBoxLayout()
        self.title_bar_layout.setContentsMargins(0, 0, 0, 0)

        self.title_label = QLabel(
            t("app_title", self.language).format(version=self.local_version)
        )
        self.title_label.setStyleSheet(
            """
            background-color: rgba(0, 0, 0, 150);
            color: white;
            padding: 10px;
            border-radius: 3px;
        """
        )
        self.title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.close_button = QPushButton(t("close_button", self.language))
        self.close_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(255, 0, 0, 150);
                color: white;
                font-weight: bold;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 200);
            }
        """
        )
        self.close_button.setFixedSize(30, 30)
        self.close_button.clicked.connect(self.exitApplication)

        self.title_bar_layout.addWidget(self.title_label)
        self.title_bar_layout.addWidget(self.close_button)
        self.title_bar.setLayout(self.title_bar_layout)
        self.title_bar.setStyleSheet("background-color: rgba(0, 0, 0, 150);")

        self.reposition_button = QPushButton(t("btn_recognize_window", self.language))
        self.reposition_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(0, 191, 255, 150);
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: rgba(0,100,0, 150);
            }
        """
        )
        self.reposition_button.clicked.connect(self.repositionWindow)

        self.toggle_button = QPushButton(t("btn_auto_song", self.language))
        self.toggle_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(0,100,0, 150);
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: rgba(0, 255, 0, 200);
            }
        """
        )

        self.help_button = QPushButton(t("help_button", self.language))
        self.help_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(0,0,0, 150);
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: rgba(0, 255, 0, 200);
            }
        """
        )
        self.help_button.clicked.connect(self.toggleHelp)

        layout.addWidget(self.title_bar)
        layout.addWidget(self.reposition_button)
        layout.addWidget(self.toggle_button)

        # 初始化语言显示为默认语言（不改变下拉显示）
        self.changeLanguage("zh-CN")

        self.hold_th_input = QSpinBox()
        self.hold_th_input.setRange(0, 100)
        self.hold_th_input.setValue(10)
        self.hold_th = int(self.hold_th_input.value())
        self.hold_th_input.valueChanged.connect(self.setHoldTh)
        hold_th_label = QLabel(t("press_time_label", self.language))
        hold_th_label.setStyleSheet(
            "background-color: rgba(0, 0, 0, 150); color: white; text-align: center;"
        )
        hold_th_label.setAlignment(Qt.AlignCenter)

        hold_th_layout = QHBoxLayout()
        hold_th_layout.addWidget(hold_th_label)
        hold_th_layout.addWidget(self.hold_th_input)
        layout.addLayout(hold_th_layout)

        # return button shown on overlay to go back to main control window
        self.return_button = QPushButton(t("return_to_main", self.language))
        self.return_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(0, 191, 255, 150);
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }            QPushButton:hover {
                background-color: rgba(0, 191, 255, 200);
            }
            QPushButton:pressed {
                background-color: rgba(0, 150, 200, 200);
            }        """
        )
        self.return_button.clicked.connect(self._on_return_clicked)
        layout.addWidget(self.return_button)

        # callback set by caller to handle returning to main window
        self._return_callback = None

    def set_return_callback(self, cb):
        self._return_callback = cb

    def _on_return_clicked(self):
        # stop running and notify
        try:
            if hasattr(self, "engine") and self.engine is not None:
                try:
                    self.engine.running = False
                except Exception:
                    pass
        except Exception:
            pass
        if callable(self._return_callback):
            self._return_callback()

    def setHoldTh(self, value):
        # value is an int from QSpinBox
        try:
            self.hold_th = int(value)
        except Exception:
            self.hold_th = int(self.hold_th_input.value())
        # If engine is attached, update its parameter
        if hasattr(self, "engine") and self.engine is not None:
            try:
                self.engine.hold_th = self.hold_th
            except Exception:
                pass

    def initLanguageTexts(self):
        return

    def changeLanguage(self, language):
        self.language = language
        self.reposition_button.setText(t("btn_recognize_window", self.language))
        self.help_button.setText(t("help_button", self.language))
        self.close_button.setText(t("close_button", self.language))
        self.title_label.setText(
            t("app_title", self.language).format(version=self.local_version)
        )
        self.update()
        self.repositionWindow()

    def languageChanged(self, index):
        # index 0 is the label placeholder; do nothing if selected
        if index == 0:
            return
        language_map = {1: "zh-CN", 2: "zh-TW", 3: "ja-JP", 4: "en-US"}
        self.changeLanguage(language_map.get(index, "en-US"))

    def changeToggleButton(self):
        # Prefer engine state if attached, else fall back to module-level globals
        if hasattr(self, "engine") and self.engine is not None:
            running = getattr(self.engine, "running", False)
            focus = getattr(self.engine, "focus", False)
            low_performance = getattr(self.engine, "low_performance_state", False)
        else:
            try:
                running = globals().get("running", False)
                focus = globals().get("focus", False)
                low_performance = globals().get("low_performance_state", False)
            except Exception:
                running = False
                focus = False
                low_performance = False

        if self.btnPosition[0] == running and self.btnPosition[1] == focus:
            return
        if running and focus:
            button_text = t("running_focus", self.language)
        elif running and not focus:
            button_text = t("running_not_focus", self.language)
        elif not running and focus:
            button_text = t("not_running_focus", self.language)
        else:
            button_text = t("note_running_not_focus", self.language)
        if low_performance:
            button_text += " (Low Performance)"

        self.toggle_button.setText(button_text)
        if running and focus:
            self.toggle_button.setStyleSheet(
                """
                QPushButton {
                    background-color: rgba(0,100,0, 150);
                    color: white;
                    border: none;
                    padding: 5px;
                    border-radius: 3px;
                }
            """
            )
        else:
            self.toggle_button.setStyleSheet(
                """
                QPushButton {
                    background-color: rgba(255, 0, 0, 150);
                    color: white;
                    border: none;
                    padding: 5px;
                    border-radius: 3px;
                }
            """
            )
        time.sleep(0.1)
        self.btnPosition[0] = running
        self.btnPosition[1] = focus

    def toggleRunning(self):
        global running
        running = not running
        self.updateStatus()

    @pyqtSlot()
    def updateStatus(self):
        self.changeToggleButton()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if hasattr(self, "dragPosition"):
                self.move(event.globalPos() - self.dragPosition)
            event.accept()


def create_overlay(points, local_version=None):
    window = TransparentWindow(points, local_version=local_version)
    return window


class ControlWindow(QMainWindow):
    """Main control window shown at startup. Does not start engine directly.

    Use `set_start_callback(cb)` to provide start behavior. The start callback
    will be called when the user selects the feature and clicks Start.
    """

    def __init__(self, local_version=None):
        super().__init__()
        self.language = "zh-CN"
        self.local_version = local_version or "v0.0.0"
        self._start_callback = None
        self.initUI()

    def initUI(self):
        self.setWindowFlags(
            Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        QApplication.setFont(QFont("Microsoft YaHei", 10))
        # try:
        #     icon_path = Path(__file__).resolve().parents[1] / "icon" / "favicon.ico"
        #     if icon_path.exists():
        #         self.setWindowIcon(QIcon(str(icon_path)))
        # except Exception:
        #     pass
        icon_path = Path(__file__).resolve().parents[1] / "icon" / "favicon.ico"
        self.setWindowIcon(QIcon(str(icon_path)))
        central = QWidget()
        self.setCentralWidget(central)
        self.setMaximumWidth(280)
        layout = QVBoxLayout(central)

        # Title bar with close button
        title_bar = QWidget()
        title_bar_layout = QHBoxLayout()
        title_bar_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel(t("app_title", self.language).format(version=self.local_version))
        title.setStyleSheet(
            """
            background-color: rgba(0, 0, 0, 150);
            color: white;
            padding: 10px;
            border-radius: 3px;
        """
        )
        title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        close_button = QPushButton(t("close_button", self.language))
        close_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(255, 0, 0, 150);
                color: white;
                font-weight: bold;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 200);
            }
        """
        )
        close_button.setFixedSize(24, 24)
        close_button.clicked.connect(QApplication.quit)

        title_bar_layout.addWidget(title)
        title_bar_layout.addWidget(close_button)
        title_bar.setLayout(title_bar_layout)
        title_bar.setStyleSheet("background-color: rgba(0, 0, 0, 150);")
        layout.addWidget(title_bar)

        # First row: 识别游戏窗口 (reposition) + Language selector
        first_row = QWidget()
        first_row_layout = QHBoxLayout()
        first_row_layout.setContentsMargins(0, 0, 0, 0)

        self.reposition_button = QPushButton(t("btn_recognize_window", "zh-CN"))
        self.reposition_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(0, 191, 255, 150);
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
        """
        )
        self.reposition_button.setFixedHeight(28)
        self.reposition_button.clicked.connect(self.repositionWindow)

        self.lang_combo = QComboBox()
        self.lang_combo.addItems(
            [
                t("language_label", "en-US"),
                t("language_zh_cn", "zh-CN"),
                t("language_zh_tw", "zh-TW"),
                t("language_ja_jp", "ja-JP"),
                t("language_en_us", "en-US"),
            ]
        )
        # set language from persisted config if available
        current_lang = get("language", "zh-CN")
        lang_index_map = {"zh-CN": 1, "zh-TW": 2, "ja-JP": 3, "en-US": 4}
        self.lang_combo.setCurrentIndex(lang_index_map.get(current_lang, 1))
        self.lang_combo.setStyleSheet(
            """
            QComboBox {
                background-color: rgba(0, 0, 0, 150);
                border-radius: 3px;
                padding: 5px;
                color: white;
            }
            QComboBox::drop-down {
                width: 20px;
            }
        """
        )
        self.lang_combo.currentIndexChanged.connect(self._on_language_changed)

        first_row_layout.addWidget(self.reposition_button)
        first_row_layout.addWidget(self.lang_combo)
        first_row.setLayout(first_row_layout)
        layout.addWidget(first_row)

        # Separator with feature selection hint
        separator = QLabel(
            "↓ "
            + (
                "请选择功能"
                if self.language == "zh-CN"
                else (
                    "Select Feature"
                    if self.language == "en-US"
                    else "機能を選択" if self.language == "ja-JP" else "請選擇功能"
                )
            )
        )
        separator.setStyleSheet(
            """
            background-color: rgba(0, 0, 0, 100);
            color: rgba(255, 255, 255, 180);
            padding: 8px;
            border-radius: 3px;
            font-size: 9px;
        """
        )
        separator.setAlignment(Qt.AlignCenter)
        layout.addWidget(separator)
        self.separator_label = separator

        # Start button (Auto Song)
        self.start_button = QPushButton(t("btn_auto_song", self.language))
        self.start_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(0, 100, 0, 150);
                color: white;
                border: none;
                padding: 8px;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: rgba(0, 255, 0, 200);
            }
        """
        )
        self.start_button.clicked.connect(self._on_start_clicked)
        layout.addWidget(self.start_button)

        # Check updates button
        self.check_updates_button = QPushButton(
            t("close_button", self.language)
            if "check" not in t("close_button", self.language).lower()
            else "Check Updates"
        )
        self.check_updates_button.setText(
            "检查更新" if self.language == "zh-CN" else "Check Updates"
        )
        self.check_updates_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(0, 191, 255, 150);
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: rgba(0, 191, 255, 200);
            }
        """
        )
        self.check_updates_button.clicked.connect(self._on_check_updates)
        layout.addWidget(self.check_updates_button)

    def set_start_callback(self, cb):
        self._start_callback = cb

    def _on_start_clicked(self):
        if callable(self._start_callback):
            self._start_callback()

    def _on_help(self):
        QMessageBox.information(
            self, t("help_button", self.language), t("help", self.language)
        )

    def _on_check_updates(self):
        import webbrowser

        webbrowser.open("https://github.com/yujianke100/HBR-AutoBeat/releases")

    def _on_language_changed(self, index):
        if index == 0:
            return
        language_map = {1: "zh-CN", 2: "zh-TW", 3: "ja-JP", 4: "en-US"}
        self.language = language_map.get(index, "zh-CN")
        # persist language selection
        try:
            set("language", self.language)
        except Exception:
            pass
        self._update_ui_texts()

    def repositionWindow(self):
        # reuse helper used by overlay window; this will show messages if window not found
        points = [
            (325, 810),
            (575, 810),
            (825, 810),
            (1075, 810),
            (1325, 810),
            (1575, 810),
        ]
        try:
            init("HeavenBurnsRed", points)
        except Exception:
            pass

    def _update_ui_texts(self):
        # Update all UI texts based on current language
        self.start_button.setText(t("btn_auto_song", self.language))
        if self.language == "zh-CN":
            self.check_updates_button.setText("检查更新")
            self.separator_label.setText("↓ 请选择功能")
        elif self.language == "zh-TW":
            self.check_updates_button.setText("檢查更新")
            self.separator_label.setText("↓ 請選擇功能")
        elif self.language == "ja-JP":
            self.check_updates_button.setText("アップデートを確認")
            self.separator_label.setText("↓ 機能を選択")
        else:
            self.check_updates_button.setText("Check Updates")
            self.separator_label.setText("↓ Select Feature")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if hasattr(self, "dragPosition"):
                self.move(event.globalPos() - self.dragPosition)
            event.accept()
