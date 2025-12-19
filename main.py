import sys
from pathlib import Path

# Standard / third-party imports
import pyautogui  # 不能省，否则会让窗口识别失效  # noqa: F401
import requests  # type: ignore
from pynput import keyboard  # noqa: F401
from pynput.keyboard import Controller, Key, KeyCode, Listener  # noqa: F401

# Qt imports
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMessageBox

# Local imports
from core.engine import AutoSongEngine
from src.config import get
from ui.auto_song import attach as attach_auto_song
from ui.main_window import ControlWindow, create_overlay

# runtime globals
hold_th = get("hold_th", 10)
single_run_time = 0.015
low_performance_state = False
LOCAL_VERSION = "v3.0.0"
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
    # Set DPI attributes BEFORE creating QApplication
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # type: ignore[attr-defined]
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # type: ignore[attr-defined]

    # create QApplication after setting attributes
    app = QApplication(sys.argv)

    # Set Windows AppUserModelID for proper taskbar icon
    try:
        import ctypes

        myappid = "yujianke100.HBR-AutoBeat.v3.0.0"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

    # Set application icon
    icon_path = Path(__file__).resolve().parent / "icon" / "favicon.ico"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    check_for_updates()

    points = [
        (325, 810),
        (575, 810),
        (825, 810),
        (1075, 810),
        (1325, 810),
        (1575, 810),
    ]

    control = ControlWindow(local_version=LOCAL_VERSION)

    # start feature when user clicks Start in control window
    def start_feature():
        control.hide()
        overlay_window = create_overlay(points, LOCAL_VERSION)
        overlay_window.language = control.language
        overlay_window.changeLanguage(control.language)
        # Show overlay immediately and start async reposition to avoid blocking UI
        overlay_window.show()
        overlay_window.start_reposition_async(points)

        engine = AutoSongEngine(overlay_window, points, hold_th, single_run_time)
        attach_auto_song(engine, overlay_window)

        # start keyboard listener bound to engine handlers
        listener = Listener(on_press=engine.on_press, on_release=engine.on_release)
        listener.start()

        # store refs to avoid GC
        globals()["overlay_window"] = overlay_window
        globals()["engine"] = engine
        globals()["listener"] = listener

        def _on_return():
            try:
                engine.running = False
            except Exception:
                pass
            try:
                overlay_window.close()
            except Exception:
                pass
            control.show()

        overlay_window.set_return_callback(_on_return)

    control.set_start_callback(start_feature)
    control.show()

    # 启动Qt事件循环
    sys.exit(app.exec_())
