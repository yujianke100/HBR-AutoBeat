from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget,
                           QComboBox, QPushButton, QHBoxLayout, QMessageBox, QSizePolicy)
from PyQt5.QtCore import Qt, QMetaObject, pyqtSlot
from PyQt5.QtGui import QFont
import sys
import time

import pyautogui  # 不能省，否则会让窗口识别失效  # noqa: F401
import pygetwindow as gw
import win32con
import win32gui
import win32ui
from PIL import Image, ImageDraw
from pynput import keyboard
from pynput.keyboard import Controller, Key, KeyCode, Listener  # noqa: F401


from threading import Thread

def safeChangeToggleButton():
    QMetaObject.invokeMethod(overlay_window, "updateStatus", Qt.QueuedConnection)

def init(window_title, test_flag=False):
    global window  # 声明为全局变量，以便在 on_press 中访问
    all_windows = gw.getAllTitles()
    browser_window_titles = [
        title for title in all_windows if window_title in title]
    if browser_window_titles == []:
        app = QApplication(sys.argv)
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Window Not Found")
        msg_box.setText("HBR was not found.")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setWindowFlags(msg_box.windowFlags() |
                               Qt.WindowStaysOnTopHint)
        msg_box.exec_()
        sys.exit()

    chosen_browser_title = browser_window_titles[0]
    window = gw.getWindowsWithTitle(chosen_browser_title)[0]
    window.restore()
    window.activate()
    time.sleep(0.5)

    hwnd = window._hWnd

    client_rect = win32gui.GetClientRect(hwnd)
    client_left, client_top = win32gui.ClientToScreen(
        hwnd, (client_rect[0], client_rect[1])
    )

    client_right, client_bottom = win32gui.ClientToScreen(
        hwnd, (client_rect[2], client_rect[3])
    )
    client_width = client_right - client_left
    client_height = client_bottom - client_top

    if test_flag:
        test(client_left, client_top, client_width, client_height)

    if (client_width != 1920 or client_height != 1080):
        app = QApplication(sys.argv)  # 创建 QApplication 实例
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)  # 设置图标为警告类型
        msg_box.setWindowTitle("Resolution Error")
        msg_box.setText(
            f"Window resolution does not match.\nIt needs to be set to 1920x1080, currently recognized as {client_width}x{client_height}.\nPlease reset the resolution in the game."
        )
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setWindowFlags(msg_box.windowFlags() |
                               Qt.WindowStaysOnTopHint)  # 设置置顶
        msg_box.exec_()  # 显示消息框
        sys.exit()  # 退出程序

    y_value = points[0][1]

    min_x = min(point[0] for point in points)
    max_x = max(point[0] for point in points)

    return client_left, client_top, client_width, client_height, y_value, min_x, max_x


class TransparentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        client_left, client_top, client_width, client_height, y_value, min_x, max_x = init(
            "HeavenBurnsRed", test_flag=False)
        self.client_left = client_left
        self.client_top = client_top
        self.client_width = client_width
        self.client_height = client_height
        self.y_value = y_value
        self.min_x = min_x
        self.max_x = max_x
        self.language = 'zh_CN'  # 默认语言为简体中文
        # 记录当前按键状态
        self.btnPosition = [None, None]
        self.language_texts = {}  # 存储多语言文本映射
        self.initUI()

    def getWindowInfo(self):
        return self.client_left, self.client_top, self.client_width, self.client_height, self.y_value, self.min_x, self.max_x

    def repositionWindow(self):
        # 重新识别窗口位置
        self.client_left, self.client_top, self.client_width, self.client_height, self.y_value, self.min_x, self.max_x = init(
            "HeavenBurnsRed", test_flag=False)
        # 重新设置窗口位置
        self.setGeometry(self.client_left + int(1920/3), self.client_top, 250, 250)
        
    def exitApplication(self):
        sys.exit()

    def initUI(self):
        # 设置窗口标志
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |  # 窗口置顶
            Qt.FramelessWindowHint |   # 无边框
            Qt.Tool                    # 工具窗口，不在任务栏显示
        )
        # 设置窗口透明度
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 设置GUI的默认字体大小
        QApplication.setFont(QFont("Microsoft YaHei", 14))

        # 创建主窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建垂直布局
        layout = QVBoxLayout(central_widget)

        # 创建一个水平布局用于语言选择
        lang_layout = QHBoxLayout()

        # 设置一个标题栏
        self.title_bar = QWidget()  # 用于容纳标题和关闭按钮的容器
        self.title_bar_layout = QHBoxLayout()
        self.title_bar_layout.setContentsMargins(0, 0, 0, 0)  # 去除布局的边距

        # 标题标签
        self.title_label = QLabel("HBR-AutoBeat")
        self.title_label.setStyleSheet("""
            background-color: rgba(0, 0, 0, 150);
            color: white;
            padding: 10px;
            border-radius: 3px;
        """)
        self.title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)  # 扩展标题占满剩余空间

        # "X" 按钮，用于退出程序
        self.close_button = QPushButton("X")
        self.close_button.setStyleSheet("""
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
        """)
        self.close_button.setFixedSize(30, 30)  # 设置固定大小
        self.close_button.clicked.connect(self.exitApplication)

        # 将标题和关闭按钮添加到标题栏布局
        self.title_bar_layout.addWidget(self.title_label)
        self.title_bar_layout.addWidget(self.close_button)

        # 设置标题栏布局
        self.title_bar.setLayout(self.title_bar_layout)
        self.title_bar.setStyleSheet("background-color: rgba(0, 0, 0, 150);")  # 设置标题栏背景颜色

        # 增加一个按钮，用于重新识别窗口位置
        self.reposition_button = QPushButton("")
        self.reposition_button.setStyleSheet("""
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
        """)
        self.reposition_button.clicked.connect(self.repositionWindow)

        self.lang_combo = QComboBox()
        self.lang_combo.addItems([" (Language)", " 简体中文", " 繁体中文", " 日本語", " English"])
        self.lang_combo.setStyleSheet("""
            QComboBox {
                background-color: rgba(0, 0, 0, 150);
                border-radius: 3px;
                padding: 3px;
                color: white;
            }
            QComboBox::drop-down {
                width: 20px; /* 下拉区域宽度 */
            }
        """)
        self.lang_combo.currentIndexChanged.connect(self.languageChanged)

        # 创建启动/停止按钮
        self.toggle_button = QPushButton("")
        self.toggle_button.setStyleSheet("""
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
        """)
        self.toggle_button.clicked.connect(self.toggleRunning)

        # 增加说明标签
        self.help_label = QLabel("")
        self.help_label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: rgba(0, 0, 0, 150);
                padding: 5px;
                border-radius: 5px;
            }
        """)

        # 添加所有组件到布局
        layout.addWidget(self.title_bar)  # 添加标题栏
        lang_layout.addWidget(self.reposition_button)
        lang_layout.addWidget(self.lang_combo)
        layout.addLayout(lang_layout)
        layout.addWidget(self.toggle_button)
        layout.addWidget(self.help_label)

        # 初始化语言文本
        self.initLanguageTexts()
        self.languageChanged(0)


    def initLanguageTexts(self):
        """初始化语言文本"""
        self.language_texts = {
            "zh_CN": {
                "title": "HBR-AutoBeat",
                "reposition": "重新识别游戏窗口",
                "help": "'o' 激活，'p' 取消激活，\n直接点击上方按钮也能切换激活状态。\n激活后聚焦游戏内，按钮变绿，打歌开始。\n游戏窗口移动后先点击'重新识别游戏窗口'。\n使用前请先初始化设置，再将按键大小设置为80%。",
                "key_status": "按键状态",
                "note_running_not_focus": "未激活，未聚焦",
                "running_not_focus": "已激活，未聚焦",
                "not_running_focus": "未激活，已聚焦",
                "running_focus": "已激活，已聚焦"
            },
            "zh_TW": {
                "title": "HBR-AutoBeat",
                "reposition": "重新識別遊戲窗口",
                "help": "'o' 鍵啟用，'p' 鍵取消啟用，\n直接點擊上方按鈕也能切換激活狀態。\n啟用後聚焦遊戲內，按鈕變綠，打歌開始。\n移動遊戲窗口後請先點擊'重新識別遊戲窗口'。\n使用前請先初始化設置，再將按鍵大小設置為80%。",
                "key_status": "按鍵狀態",
                "note_running_not_focus": "未啟用，未聚焦",
                "running_not_focus": "已啟用，未聚焦",
                "not_running_focus": "未啟用，已聚焦",
                "running_focus": "已啟用，已聚焦"
            },
            "ja_JP": {
                "title": "HBR-AutoBeat", 
                "reposition": "ゲームウィンドウを再認識",  
                "help": "'o'キーで有効化、'p'キーで無効化、\n上のボタンで状態を切り替えられます。\n有効化後、ゲーム内にフォーカスを合わせ、\nボタンが緑色になったら開始します。\nウィンドウ移動後は「ゲームウィンドウを再認識」をクリックしてください。\n使用前に初期設定を行い、ボタンサイズを80％に設定してください。",
                "key_status": "キーの状態",
                "note_running_not_focus": "無効、フォーカスなし", 
                "running_not_focus": "有効、フォーカスなし",  
                "not_running_focus": "無効、フォーカスあり", 
                "running_focus": "有効、フォーカスあり" 
            },
            "en_US": {
                "title": "HBR-AutoBeat",
                "reposition": "Re-recognize game window",
                "help": "Press 'o' to activate, press 'p' to deactivate, \nClicking the button above can also toggle the state.\nFocus on the game window after activation. \nButton turns green to start.\nIf the game window moves, click 'Re-recognize game window' first.\nPlease initialize settings first, then set the button size to 80%.",
                "key_status": "Key Status",
                "note_running_not_focus": "Not running, not focused",
                "running_not_focus": "running, not focused",
                "not_running_focus": "Not running, focused",
                "running_focus": "running, focused"
            }
        }

    def changeLanguage(self, language):
        self.language = language
        texts = self.language_texts.get(language, self.language_texts["en_US"])
        self.title_label.setText(texts["title"])
        self.reposition_button.setText(texts["reposition"])
        self.help_label.setText(texts["help"])
        # self.key_status.setText(texts["key_status"])
        self.update()
        self.repositionWindow()
        

    def languageChanged(self, index):
        """语言切换事件"""
        language_map = {
            0: "",
            1: "zh_CN",  # 简体中文
            2: "zh_TW",  # 繁体中文
            3: "ja_JP",  # 日本語
            4: "en_US"   # English
        }
        if(index == 0):
            self.changeLanguage("zh_CN")
        else:
            self.changeLanguage(language_map.get(index, "en_US"))
        

    def changeToggleButton(self):
        global running
        global focus
        # 如果running不存在，等待到running被定义
        if (self.btnPosition[0] == running and self.btnPosition[1] == focus):
            return
        texts = self.language_texts.get(self.language, self.language_texts["en_US"])
        if(running and focus):
            self.toggle_button.setText(texts["running_focus"])
        elif(running and not focus):
            self.toggle_button.setText(texts["running_not_focus"])
        elif(not running and focus):
            self.toggle_button.setText(texts["not_running_focus"])
        else:
            self.toggle_button.setText(texts["note_running_not_focus"])
        if(running and focus):
            self.toggle_button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(0,100,0, 150);
                    color: white;
                    border: none;
                    padding: 5px;
                    border-radius: 3px;
                }
            """)
        else:
            self.toggle_button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 0, 0, 150);
                    color: white;
                    border: none;
                    padding: 5px;
                    border-radius: 3px;
                }
            """)
        time.sleep(0.1)
        self.btnPosition[0]=running
        self.btnPosition[1]=focus

    def toggleRunning(self):
        global running
        running=not running
        self.updateStatus()

    @pyqtSlot()  # Mark the method as a slot
    def updateStatus(self):
        self.changeToggleButton()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if hasattr(self, 'dragPosition'):  # 检查是否已定义dragPosition
                self.move(event.globalPos() - self.dragPosition)
            event.accept()

def create_overlay():
    app=QApplication(sys.argv)
    window=TransparentWindow()
    window.show()
    return app, window

def on_press(key):
    global running
    try:
        if is_window_on_top(window):  # 仅在窗口聚焦时检测输入
            if key.char == "o":  # 按下 'o' 键开始自动演奏
                running=True
            elif key.char == "p":  # 按下 'p' 键停止自动演奏
                running=False
                # 模拟esc
                keyboard.press(Key.esc)
                keyboard.release(Key.esc)
        safeChangeToggleButton()
    except AttributeError:
        pass


# 释放按键
def on_release(key):
    pass

def capture_screenshot(left, top, width, height):
    hdesktop=win32gui.GetDesktopWindow()
    hwindow=win32gui.GetWindowDC(hdesktop)
    srcdc=win32ui.CreateDCFromHandle(hwindow)
    memdc=srcdc.CreateCompatibleDC()

    bmp=win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)

    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

    bmp_info=bmp.GetInfo()
    bmp_str=bmp.GetBitmapBits(True)

    img=Image.frombuffer(
        "RGB", (bmp_info["bmWidth"], bmp_info["bmHeight"]
                ), bmp_str, "raw", "BGRX", 0, 1
    )

    win32gui.DeleteObject(bmp.GetHandle())
    memdc.DeleteDC()
    srcdc.DeleteDC()
    win32gui.ReleaseDC(hdesktop, hwindow)

    return img


def test(client_left, client_top, client_width, client_height):
    print("窗口分辨率：", client_width, client_height)
    screenshot=capture_screenshot(
        client_left, client_top, client_width, client_height
    )

    point_colors=[screenshot.getpixel(point) for point in points]
    # hyper_point_colors = [screenshot.getpixel(hyper_point) for hyper_point in hyper_points]
    print(point_colors)

    # 使用 ImageDraw 在截图上绘制点
    draw=ImageDraw.Draw(screenshot)

    # 绘制点（用红色和蓝色表示）
    for point in points:
        draw.ellipse(
            (point[0] - 5, point[1] - 5, point[0] + 5, point[1] + 5), fill="red"
        )

    # 显示截图
    screenshot.show()

    exit()


def is_window_on_top(window):
    top_window_hwnd=win32gui.GetForegroundWindow()
    return top_window_hwnd == window._hWnd


def main():
    global running
    global focus
    global window
    while True:
        now_focus=is_window_on_top(window)
        if (now_focus and not focus):
            focus=True
            # overlay_window.updateStatus()
            safeChangeToggleButton()

        elif (not now_focus and focus):
            focus=False
            # overlay_window.updateStatus()
            safeChangeToggleButton()

        if (not running or not focus):
            time.sleep(0.1)
            continue
        client_left, client_top, _, _, y_value, min_x, max_x=overlay_window.getWindowInfo()

        # 满足条件，开始打歌
        screenshot=capture_screenshot(
            client_left + min_x, client_top + y_value, max_x - min_x + 1, 1
        )

        point_colors=[
            screenshot.getpixel(
                (point[0] - min_x, 0)
            )  # x 坐标相对于截取区域的调整，y 坐标始终为 0
            for point in points
        ]

        for i, color in enumerate(point_colors):
            if key_states[keys[i]] > 0:
                key_states[keys[i]] += 1

            r, g, b=color
            # original_r, original_g, original_b = original_points_colors[i]
            # 判断color的三个数字是不是处于original_points_colors[i]和original_red_points_colors[i]之间

            original_flag=(
                (
                    r >= original_red_points_colors[i][0] - COLOR_TOLERANCE
                    and r <= original_points_colors[i][0] + COLOR_TOLERANCE
                )
                and (
                    g >= original_red_points_colors[i][1] - COLOR_TOLERANCE
                    and g <= original_points_colors[i][1] + COLOR_TOLERANCE
                )
                and (
                    b >= original_red_points_colors[i][2] - COLOR_TOLERANCE
                    and b <= original_points_colors[i][2] + COLOR_TOLERANCE
                )
            )
            original_color=blue_points_colors[i]

            if original_flag:
                keyboard.release(keys[i])
                key_states[keys[i]]=0
                continue

            if (
                r < original_red_points_colors[i][0] - COLOR_TOLERANCE
                or g < original_red_points_colors[i][1] - COLOR_TOLERANCE
                or b < original_red_points_colors[i][2] - COLOR_TOLERANCE
                or (r > 210 and g > 210 and b > 210)
            ) and key_states[keys[i]] == 0:
                keyboard.press(keys[i])
                key_states[keys[i]] += 1
                continue

            if key_states[keys[i]] > 5 and (
                abs(color[0] - original_color[0]) > COLOR_TOLERANCE
                or abs(color[1] - original_color[1]) > COLOR_TOLERANCE
                or abs(color[2] - original_color[2]) > COLOR_TOLERANCE
            ):
                keyboard.release(keys[i])
                key_states[keys[i]]=0

                continue
            # time.sleep(0.01)

# 在主脚本中使用：
if __name__ == "__main__":
    points=[(325, 810), (575, 810), (825, 810),
             (1075, 810), (1325, 810), (1575, 810)]
    app, overlay_window=create_overlay()
    listener=Listener(on_press=on_press, on_release=on_release)
    listener.start()
    keyboard=Controller()
    keys=["z", "x", "c", "v", "b", "n"]
    key_states={key: 0 for key in keys}

    original_points_colors=[
        (219, 57, 222),
        (208, 41, 211),
        (132, 49, 147),
        (118, 49, 137),
        (158, 51, 170),
        (118, 50, 138),
    ]
    original_red_points_colors=[
        (211, 54, 211),
        (201, 39, 201),
        (130, 47, 141),
        (117, 47, 132),
        (154, 49, 163),
        (117, 48, 133),
    ]
    # original_hyper_points_colors = [(79, 40, 96), (79, 40, 94), (78, 40, 93), (77, 40, 92), (77, 40, 91), (76, 40, 90)]

    blue_points_colors=[
        (162, 171, 250),
        (151, 165, 247),
        (125, 144, 244),
        (94, 116, 241),
        (81, 104, 240),
        (85, 115, 236),
    ]
    # blue_red_points_colors = [,(146, 155, 235),,(95, 106, 224)]

    # 增加颜色容差范围
    COLOR_TOLERANCE=10
    running=False
    focus=False

    # 创建一个新线程来激活主循环

    main_thread=Thread(target=lambda: main())
    main_thread.daemon=True
    main_thread.start()

    # 启动Qt事件循环
    sys.exit(app.exec_())
