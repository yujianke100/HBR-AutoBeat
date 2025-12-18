import sys

# app = QApplication(sys.argv)
# app.setAttribute(Qt.AA_EnableHighDpiScaling)  # 启用 Qt 的 DPI 适配
# app.setAttribute(Qt.AA_UseHighDpiPixmaps)  # 让 QPixmap 适配高 DPI
import pyautogui  # 不能省，否则会让窗口识别失效  # noqa: F401
import requests
from pynput import keyboard  # noqa: F401
from pynput.keyboard import Controller, Key, KeyCode, Listener  # noqa: F401
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMessageBox

from core.engine import AutoSongEngine
from ui.auto_song import attach as attach_auto_song
from ui.main_window import create_overlay

# runtime globals
hold_th = 10
single_run_time = 0.015
low_performance_state = False
LOCAL_VERSION = "v2.1.0"
window = None
running = False
focus = None
force_run = False


def check_for_updates():
    GITHUB_API_URL = (
        "https://api.github.com/repos/yujianke100/HBR-AutoBeat/releases/latest"
    )
    try:
        response = requests.get(GITHUB_API_URL, timeout=2)
        if response.status_code == 200:
            latest_version = response.json().get("tag_name", "")
            if latest_version and latest_version > LOCAL_VERSION:
                # print(f"⚠ Discover a new version: {latest_version}")
                # 弹出提示框，点击确认后打开浏览器到最新版本的下载页面，点击取消则不打开
                QApplication(sys.argv)
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setWindowTitle("New Version Found")
                msg_box.setText(
                    f"Latest version: {latest_version}\nLocal version: {LOCAL_VERSION} \nDo you want to update?"
                )
                msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowStaysOnTopHint)
                ret = msg_box.exec_()
                if ret == QMessageBox.Ok:
                    import webbrowser

                    webbrowser.open(
                        "https://github.com/yujianke100/HBR-AutoBeat/releases/latest"
                    )
                    sys.exit()

    except requests.RequestException:
        pass  # 2 秒内无法访问则跳过


# 在主脚本中使用：
if __name__ == "__main__":
    check_for_updates()
    points = [(325, 810), (575, 810), (825, 810), (1075, 810), (1325, 810), (1575, 810)]
    app, overlay_window = create_overlay(points, LOCAL_VERSION)

    # create and start the auto-song engine, attach to UI
    engine = AutoSongEngine(overlay_window, points, hold_th, single_run_time)
    attach_auto_song(engine, overlay_window)

    # start keyboard listener bound to engine handlers
    listener = Listener(on_press=engine.on_press, on_release=engine.on_release)
    listener.start()

    # 启动Qt事件循环
    sys.exit(app.exec_())
