# Standard / third-party imports
import ctypes
import os
import sys

try:
    # 设置 DPI 识别（必须在创建 QApplication 之前）
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Process_System_DPI_Aware
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass


def get_resource_path(relative_path):
    """获取资源的绝对路径，兼容开发环境和 PyInstaller 打包环境"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


import json  # noqa: E402
import urllib.request  # noqa: E402

from pynput.keyboard import Listener  # noqa: E402

# Qt imports
from PyQt5.QtCore import Qt  # noqa: E402
from PyQt5.QtGui import QIcon  # noqa: E402
from PyQt5.QtWidgets import QApplication, QMessageBox  # noqa: E402

# Local imports
from core.engine import AutoSongEngine  # noqa: E402
from ui.auto_song import attach as attach_auto_song  # noqa: E402
from ui.main_window import create_overlay  # noqa: E402

# runtime globals
hold_th = 10
single_run_time = 0.015
low_performance_state = False
LOCAL_VERSION = "v2.3.0"
window = None
running = False
focus = None
force_run = False


def check_for_updates():
    GITHUB_API_URL = (
        "https://api.github.com/repos/yujianke100/HBR-AutoBeat/releases/latest"
    )
    try:
        # 使用原生 urllib 检查更新，减少打包体积
        req = urllib.request.Request(
            GITHUB_API_URL, headers={"User-Agent": "HBR-AutoBeat-Updater"}
        )
        with urllib.request.urlopen(req, timeout=2) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                latest_version = data.get("tag_name", "")
                if latest_version and latest_version > LOCAL_VERSION:
                    # 弹出提示框
                    msg_box = QMessageBox()
                    icon_path = get_resource_path("icon/favicon.ico")
                    if os.path.exists(icon_path):
                        msg_box.setWindowIcon(QIcon(icon_path))
                    msg_box.setIcon(QMessageBox.Information)
                    msg_box.setWindowTitle("New Version Found")
                    msg_box.setText(
                        f"Latest version: {latest_version}\nLocal version: {LOCAL_VERSION} \nDo you want to update?"
                    )
                    msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    msg_box.setWindowFlags(
                        msg_box.windowFlags() | Qt.WindowStaysOnTopHint
                    )
                    ret = msg_box.exec_()
                    if ret == QMessageBox.Ok:
                        import webbrowser

                        webbrowser.open(
                            "https://github.com/yujianke100/HBR-AutoBeat/releases/latest"
                        )
                        sys.exit()
    except Exception:
        pass


# 在主脚本中使用：
if __name__ == "__main__":
    # 在创建 QApplication 之前设置属性
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)

    # 设置 Windows 的 AppUserModelID，确保任务栏图标显示正确
    try:
        myappid = "yujianke100.HBR-AutoBeat.v2.3.0"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

    # 设置应用程序全局图标
    icon_path = get_resource_path("icon/favicon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    check_for_updates()

    points = [
        (325, 810),
        (575, 810),
        (825, 810),
        (1075, 810),
        (1325, 810),
        (1575, 810),
    ]

    # 直接创建打歌界面，不再显示主窗口
    overlay_window = create_overlay(points, LOCAL_VERSION)
    overlay_window.language = "zh-CN"  # 默认语言
    overlay_window.changeLanguage("zh-CN")

    # 显示打歌界面并开始异步定位窗口
    overlay_window.show()
    overlay_window.start_reposition_async(points)

    # 创建引擎并附加到界面
    engine = AutoSongEngine(overlay_window, points, hold_th, single_run_time)
    attach_auto_song(engine, overlay_window)

    # 启动键盘监听
    listener = Listener(on_press=engine.on_press, on_release=engine.on_release)
    listener.start()

    # 存储全局引用避免被垃圾回收
    globals()["overlay_window"] = overlay_window
    globals()["engine"] = engine
    globals()["listener"] = listener

    # 启动Qt事件循环
    sys.exit(app.exec_())
