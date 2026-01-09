import time
from pathlib import Path
from typing import Tuple

import win32con
import win32gui
import win32ui
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
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
        # Defer expensive window detection (win32 calls) to async worker
        self.client_left = 0
        self.client_top = 0
        self.client_width = 1920
        self.client_height = 1080
        self.y_value = points[0][1] if points else 810
        self.min_x = min(p[0] for p in points) if points else 325
        self.max_x = max(p[0] for p in points) if points else 1575
        self._reposition_done = False
        self._pending_geometry = None
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
        # Mark that repositioning is done
        self._reposition_done = True

    def start_reposition_async(self, points=None):
        """Start background worker to detect game window and apply geometry when ready."""
        import threading

        def _worker():
            try:
                pts = points or [
                    (325, 810),
                    (575, 810),
                    (825, 810),
                    (1075, 810),
                    (1325, 810),
                    (1575, 810),
                ]
                (
                    client_left,
                    client_top,
                    client_width,
                    client_height,
                    y_value,
                    min_x,
                    max_x,
                ) = init("HeavenBurnsRed", pts, test_flag=True)
                scale = get_dpi_scale_factor()
                logical_left = int(client_left / scale)
                logical_top = int((client_top + 150) / scale)
                # store pending geometry for main thread to apply
                self._pending_geometry = (logical_left, logical_top, 10, 10)
                self._reposition_done = True
            except Exception:
                self._reposition_done = True

        threading.Thread(target=_worker, daemon=True).start()

        # poll for completion and apply geometry on main thread
        timer = QTimer(self)

        def _check():
            if getattr(self, "_reposition_done", False):
                if self._pending_geometry:
                    left, top, w, h = self._pending_geometry
                    self.setGeometry(left, top, w, h)
                timer.stop()

        timer.timeout.connect(_check)
        timer.start(50)

    def exitApplication(self):
        import sys

        sys.exit()

    def toggleHelp(self):
        QMessageBox.information(
            self, t("help_button", self.language), t("help", self.language)
        )

    def showOffsetDetection(self):
        """显示游戏窗口截图并标出识别点位置"""
        try:
            from PIL import Image, ImageDraw
            import pygetwindow as gw
            import pyautogui
            import os
            from PyQt5.QtGui import QPixmap, QImage
            from PyQt5.QtCore import Qt as QtCore
            from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout

            # 获取游戏窗口
            all_windows = gw.getAllTitles()
            browser_window_titles = [title for title in all_windows if "HeavenBurnsRed" in title]
            
            if not browser_window_titles:
                QMessageBox.warning(
                    self,
                    t("offset_detect", self.language),
                    t("hbr_not_found", self.language)
                )
                return
            
            chosen_browser_title = browser_window_titles[0]
            window = gw.getWindowsWithTitle(chosen_browser_title)[0]
            
            # 尝试激活并聚焦窗口，确保截图是最新的
            try:
                window.activate()
                time.sleep(0.1)
            except:
                pass
                
            hwnd = window._hWnd
            
            # 获取窗口客户区信息（屏幕坐标）
            client_rect = win32gui.GetClientRect(hwnd)
            left, top = win32gui.ClientToScreen(hwnd, (client_rect[0], client_rect[1]))
            right, bottom = win32gui.ClientToScreen(hwnd, (client_rect[2], client_rect[3]))
            width = right - left
            height = bottom - top
            
            # 使用 pyautogui 直接从屏幕抓取，比 BitBlt 抓取窗口 DC 更可靠且不会有缓存
            screenshot = pyautogui.screenshot(region=(left, top, width, height))
            
            # 在图像上标记识别点
            draw = ImageDraw.Draw(screenshot)
            points = [
                (325, 810), (575, 810), (825, 810),
                (1075, 810), (1325, 810), (1575, 810),
            ]
            
            for point in points:
                x, y = point
                radius = 8
                draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                           fill='red', outline='red', width=3)
                draw.line([x-radius*2, y, x+radius*2, y], fill='red', width=2)
                draw.line([x, y-radius*2, x, y+radius*2], fill='red', width=2)
            
            # 转换为 QPixmap (通过内存，完全不使用磁盘临时文件，彻底杜绝缓存)
            img_data = screenshot.tobytes("raw", "RGB")
            qimg = QImage(img_data, screenshot.size[0], screenshot.size[1], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
            
            # 创建对话框
            dialog = QDialog(self)
            dialog.setWindowTitle(t("offset_detect", self.language))
            dialog.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
            dialog.setStyleSheet("background-color: #000000;") # 使用黑色背景

            # 缩放以适应屏幕
            screen_geo = QApplication.primaryScreen().availableGeometry()
            max_disp_w = screen_geo.width() * 0.8
            max_disp_h = screen_geo.height() * 0.8
            
            scaled_pixmap = pixmap.scaled(
                int(max_disp_w), 
                int(max_disp_h), 
                QtCore.KeepAspectRatio, 
                QtCore.SmoothTransformation
            )
            
            layout = QVBoxLayout(dialog)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            
            label = QLabel()
            label.setPixmap(scaled_pixmap)
            label.setAlignment(Qt.AlignCenter)
            
            layout.addWidget(label)
            # 对话框大小紧贴缩放后的图片，消除多余边框
            dialog.setFixedSize(scaled_pixmap.size())
            dialog.exec_()
            
        except Exception as e:
            QMessageBox.warning(
                self,
                t("offset_detect", self.language),
                f"{t('error_occurred', self.language)}: {str(e)}"
            )
            
        except Exception as e:
            QMessageBox.warning(
                self,
                t("offset_detect", self.language),
                f"{t('error_occurred', self.language)}: {str(e)}"
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
        layout.setSizeConstraint(
            QVBoxLayout.SetFixedSize
        )  # Ensure window resizes to fit content

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

        # 第一行：识别游戏窗口按钮 + 语言选择器
        first_row = QWidget()
        first_row_layout = QHBoxLayout()
        first_row_layout.setContentsMargins(0, 0, 0, 0)

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

        # 语言选择下拉框
        self.lang_combo = QComboBox()
        self.lang_combo.addItems([
            t("language_zh_cn", "zh-CN"),
            t("language_ja_jp", "ja-JP"),
            t("language_en_us", "en-US"),
        ])
        self.lang_combo.setCurrentIndex(0)  # 默认中文
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
            QComboBox QAbstractItemView {
                background-color: rgba(0, 0, 0, 200);
                color: white;
                selection-background-color: rgba(0, 191, 255, 150);
            }
        """
        )
        self.lang_combo.currentIndexChanged.connect(self._on_language_changed)
        
        first_row_layout.addWidget(self.reposition_button)
        first_row_layout.addWidget(self.lang_combo)
        first_row.setLayout(first_row_layout)

        layout.addWidget(self.title_bar)
        layout.addWidget(first_row)

        # 开始/停止按钮
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
        layout.addWidget(self.toggle_button)

        # 长按时间设置
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

        # 帮助按钮和偏移检测按钮
        button_row = QWidget()
        button_row_layout = QHBoxLayout()
        button_row_layout.setContentsMargins(0, 0, 0, 0)

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

        self.offset_detect_button = QPushButton(t("offset_detect", self.language))
        self.offset_detect_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(100, 149, 237, 150);
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: rgba(100, 149, 237, 200);
            }
        """
        )
        self.offset_detect_button.clicked.connect(self.showOffsetDetection)

        button_row_layout.addWidget(self.help_button)
        button_row_layout.addWidget(self.offset_detect_button)
        button_row.setLayout(button_row_layout)
        layout.addWidget(button_row)

        # 初始化语言显示为默认语言（放在所有按钮创建之后）
        self.changeLanguage("zh-CN")

    def _on_language_changed(self, index):
        """处理语言切换"""
        languages = ["zh-CN", "ja-JP", "en-US"]
        if 0 <= index < len(languages):
            self.changeLanguage(languages[index])

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
        self.toggle_button.setText(t("btn_auto_song", self.language))
        self.help_button.setText(t("help_button", self.language))
        self.offset_detect_button.setText(t("offset_detect", self.language))
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
        language_map = {1: "zh-CN", 2: "ja-JP", 3: "en-US"}
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
                t("language_ja_jp", "ja-JP"),
                t("language_en_us", "en-US"),
            ]
        )
        # Always use default language (zh-CN)
        self.lang_combo.setCurrentIndex(1)
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
                else ("Select Feature" if self.language == "en-US" else "機能を選択")
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
        language_map = {1: "zh-CN", 2: "ja-JP", 3: "en-US"}
        self.language = language_map.get(index, "zh-CN")
        # Language selection is not persisted
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
