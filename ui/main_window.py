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
    def __init__(self, points):
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
        self.language = "zh_CN"
        self.btnPosition = [None, None]
        self.language_texts = {}
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
            self, t("help_button", "Help"), self.language_texts[self.language]["help"]
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
            t("app_title", "HBR-AutoBeat {version}").format(version=LOCAL_VERSION)
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

        self.close_button = QPushButton(t("close_button", "X"))
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

        self.reposition_button = QPushButton(
            t("btn_recognize_window", "Recognize Window")
        )
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
                t("language_label", "(Language)"),
                t("language_zh_cn", "简体中文"),
                t("language_zh_tw", "繁体中文"),
                t("language_ja_jp", "日本語"),
                t("language_en_us", "English"),
            ]
        )
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

        self.toggle_button = QPushButton(t("btn_auto_song", "Auto Song Play"))
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

        self.help_button = QPushButton(t("help_button", "Help"))
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

        hold_th_input = QSpinBox()
        hold_th_input.setRange(0, 100)
        hold_th_input.setValue(10)
        hold_th_input.valueChanged.connect(self.setHoldTh)
        hold_th_label = QLabel(t("press_time_label", "Press Time: "))
        hold_th_label.setStyleSheet(
            "background-color: rgba(0, 0, 0, 150); color: white;"
        )

        hold_th_layout = QHBoxLayout()
        hold_th_layout.addWidget(hold_th_label)
        hold_th_layout.addWidget(hold_th_input)
        layout.addLayout(hold_th_layout)
        layout.addWidget(self.help_button)

        self.initLanguageTexts()
        self.languageChanged(0)

    def setHoldTh(self):
        global hold_th
        hold_th = int(self.sender().text())

    def initLanguageTexts(self):
        self.language_texts = {
            "zh_CN": {
                "reposition": "重新识别游戏窗口",
                "help": "'o' 激活，'p' 取消激活并暂停，直接点击上方按钮也能切换激活状态。\n\n激活后聚焦游戏内，按钮变绿，打歌开始。\n\n游戏窗口移动后先点击'重新识别游戏窗口'。\n\n使用前请先初始化设置，关闭按压线,再将按键大小设置为80%。\n\n若出现长按过早/过晚结束，请调整'Press Time'。\n\n若显示'Low Performance'，说明设备性能较差，打歌时会出现来不及反应的情况。",
                "key_status": "按键状态",
                "note_running_not_focus": "未激活，未聚焦",
                "running_not_focus": "已激活，未聚焦",
                "not_running_focus": "未激活，已聚焦",
                "running_focus": "已激活，已聚焦",
            },
            "zh_TW": {
                "reposition": "重新識別遊戲窗口",
                "help": "'o' 鍵啟用，'p' 鍵取消啟用並暫停，直接點擊上方按鈕也能切換激活狀態。\n\n啟用後聚焦遊戲內，按鈕變綠，打歌開始。\n\n移動遊戲窗口後請先點擊'重新識別遊戲窗口'。\n\n使用前請先初始化設置，關閉按壓線，再將按鍵大小設置為80%。若發生長按過早或過晚結束的情況，\n\n請調整'Press Time'。\n\n若显示「Low Performance」，代表装置效能较低，游玩节奏游戏时可能会反应不及。",
                "key_status": "按鍵狀態",
                "note_running_not_focus": "未啟用，未聚焦",
                "running_not_focus": "已啟用，未聚焦",
                "not_running_focus": "未啟用，已聚焦",
                "running_focus": "已啟用，已聚焦",
            },
            "ja_JP": {
                "reposition": "ゲームウィンドウを再認識",
                "help": "'o'キーで有効化、'p'キーで無効化、そして一時停止します。上のボタンで状態を切り替えられます。\n\n有効化後、ゲーム内にフォーカスを合わせ、ボタンが緑色になったら開始します。\n\nウィンドウ移動後は「ゲームウィンドウを再認識」をクリックしてください。\n\n使用前に初期設定を行い、プレスラインを閉じる、ボタンサイズを80％に設定してください。\n\n長押しの終了が早すぎ・遅すぎなら「Press Time」調整してください。\n\n「Low Performance」と表示された場合、デバイスの性能が低く、リズムゲームの反応が遅れる可能性があります。",
                "key_status": "キーの状態",
                "note_running_not_focus": "無効、フォーカスなし",
                "running_not_focus": "有効、フォーカスなし",
                "not_running_focus": "無効、フォーカスあり",
                "running_focus": "有効、フォーカスあり",
            },
            "en_US": {
                "reposition": "Re-recognize game window",
                "help": "Press 'o' to activate, press 'p' to deactivate and pause the game. Clicking the button above can also toggle the state. \n\nFocus on the game window after activation. Button turns green to start.\n\nIf the game window moves, click 'Re-recognize game window' first.\n\nPlease initialize settings first, then close the press line and set the button size to 80%.\n\nIf long press ends too early/late, adjust 'Press Time'.\n\n'Low Performance' indicates low device performance, which may cause delayed responses in rhythm games.",
                "key_status": "Key Status",
                "note_running_not_focus": "Not running, not focused",
                "running_not_focus": "running, not focused",
                "not_running_focus": "Not running, focused",
                "running_focus": "running, focused",
            },
        }

    def changeLanguage(self, language):
        self.language = language
        texts = self.language_texts.get(language, self.language_texts["en_US"])
        self.reposition_button.setText(texts["reposition"])
        self.update()
        self.repositionWindow()

    def languageChanged(self, index):
        language_map = {0: "", 1: "zh_CN", 2: "zh_TW", 3: "ja_JP", 4: "en_US"}
        if index == 0:
            self.changeLanguage("zh_CN")
        else:
            self.changeLanguage(language_map.get(index, "en_US"))

    def changeToggleButton(self):
        global running
        global focus
        global low_performance_state
        if self.btnPosition[0] == running and self.btnPosition[1] == focus:
            return
        texts = self.language_texts.get(self.language, self.language_texts["en_US"])

        if running and focus:
            button_text = texts["running_focus"]
        elif running and not focus:
            button_text = texts["running_not_focus"]
        elif not running and focus:
            button_text = texts["not_running_focus"]
        else:
            button_text = texts["note_running_not_focus"]
        if low_performance_state:
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


def create_overlay(points):
    app = QApplication([])
    window = TransparentWindow(points)
    window.show()
    return app, window
