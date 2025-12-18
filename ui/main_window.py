import time
from typing import Tuple

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QFont
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
        self.in_play_mode = False
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
        self.setGeometry(self.client_left, self.client_top + 150, 10, 10)

    def exitApplication(self):
        import sys

        sys.exit()

    def toggleHelp(self):
        QMessageBox.information(
            self, t("help_button", self.language), t("help", self.language)
        )

    def initUI(self):
        global LOCAL_VERSION
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        QApplication.setFont(QFont("Microsoft YaHei", 14))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        lang_layout = QHBoxLayout()

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
        # 默认显示第一项（语言标签），但不改变内部语言设定
        self.lang_combo.setCurrentIndex(0)
        self.lang_combo.setStyleSheet(
            """
            QComboBox {
                background-color: rgba(0, 0, 0, 150);
                border-radius: 3px;
                padding: 3px;
                color: white;
            }
            QComboBox::drop-down {
                width: 20px; /* 下拉区域宽度 */
            }
        """
        )
        self.lang_combo.currentIndexChanged.connect(self.languageChanged)

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
        # intercept toggle clicks to switch views then start/stop engine
        self.toggle_button.clicked.connect(self.on_toggle_clicked)

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
        lang_layout.addWidget(self.reposition_button)
        lang_layout.addWidget(self.lang_combo)
        layout.addLayout(lang_layout)
        layout.addWidget(self.toggle_button)

        self.hold_th_input = QSpinBox()
        self.hold_th_input.setRange(0, 100)
        self.hold_th_input.setValue(10)
        self.hold_th = int(self.hold_th_input.value())
        self.hold_th_input.valueChanged.connect(self.setHoldTh)
        hold_th_label = QLabel(t("press_time_label", self.language))
        hold_th_label.setStyleSheet(
            "background-color: rgba(0, 0, 0, 150); color: white;"
        )

        hold_th_layout = QHBoxLayout()
        hold_th_layout.addWidget(hold_th_label)
        hold_th_layout.addWidget(self.hold_th_input)
        layout.addLayout(hold_th_layout)
        layout.addWidget(self.help_button)

        # collect control widgets so we can hide/show when entering play mode
        self._control_widgets = [
            self.reposition_button,
            self.lang_combo,
            self.hold_th_input,
            self.help_button,
        ]

        # 初始化语言显示为默认语言（不改变下拉显示）
        self.changeLanguage("zh-CN")

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
        # if we are in play mode but engine stopped, exit play mode
        if self.in_play_mode and not running:
            try:
                self.exit_play_mode()
            except Exception:
                pass

    def on_toggle_clicked(self):
        # when clicked in control mode, enter play view first
        if not self.in_play_mode:
            self.enter_play_mode()

        # call engine toggle if attached, else fallback to old behavior
        if hasattr(self, "engine") and self.engine is not None:
            try:
                self.engine.toggle_running()
                running = getattr(self.engine, "running", False)
            except Exception:
                running = False
        else:
            # fallback to legacy toggle
            self.toggleRunning()
            running = globals().get("running", False)

        # if toggled off, return to control view
        if not running:
            self.exit_play_mode()

    def enter_play_mode(self):
        self.in_play_mode = True
        for w in getattr(self, "_control_widgets", []):
            try:
                w.hide()
            except Exception:
                pass
        # adjust title to indicate play mode
        try:
            self.title_label.setText(
                t("app_title", self.language).format(version=self.local_version)
                + " - "
                + t("btn_auto_song", self.language)
            )
        except Exception:
            pass

    def exit_play_mode(self):
        self.in_play_mode = False
        for w in getattr(self, "_control_widgets", []):
            try:
                w.show()
            except Exception:
                pass
        # restore title
        try:
            self.title_label.setText(
                t("app_title", self.language).format(version=self.local_version)
            )
        except Exception:
            pass

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
    app = QApplication([])
    window = TransparentWindow(points, local_version=local_version)
    window.show()
    return app, window
