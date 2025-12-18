import sys

# app = QApplication(sys.argv)
# app.setAttribute(Qt.AA_EnableHighDpiScaling)  # 启用 Qt 的 DPI 适配
# app.setAttribute(Qt.AA_UseHighDpiPixmaps)  # 让 QPixmap 适配高 DPI
import time
from threading import Thread

import pyautogui  # 不能省，否则会让窗口识别失效  # noqa: F401
import requests
import win32gui
from pynput import keyboard  # noqa: F401
from pynput.keyboard import Controller, Key, KeyCode, Listener  # noqa: F401
from PyQt5.QtCore import QMetaObject, Qt
from PyQt5.QtWidgets import QApplication, QMessageBox

import core.window_helpers as window_helpers
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


def on_press(key):
    global running
    try:
        if is_window_on_top(window):
            if hasattr(key, "char") and key.char == "o":
                running = True
            elif hasattr(key, "char") and key.char == "p":
                running = False
                # 模拟esc
                keyboard_controller.press(Key.esc)
                keyboard_controller.release(Key.esc)
        safeChangeToggleButton()
    except AttributeError:
        pass


# 释放按键
def on_release(key):
    pass


def capture_screenshot(left, top, width, height):
    # moved to core.window_helpers.capture_screenshot
    return window_helpers.capture_screenshot(left, top, width, height)


def safeChangeToggleButton():
    QMetaObject.invokeMethod(overlay_window, "updateStatus", Qt.QueuedConnection)


def deactivate_window(window_title="HeavenBurnsRed"):
    return window_helpers.deactivate_window(window_title)


def get_screenshot(client_left, client_top, client_width, client_height):
    screenshot = capture_screenshot(
        client_left, client_top, client_width, client_height
    )
    return screenshot


def test(client_left, client_top, client_width, client_height):
    print("窗口分辨率：", client_width, client_height)
    # screenshot=capture_screenshot(
    #     client_left, client_top, client_width, client_height
    # )
    screenshot = get_screenshot(client_left, client_top, client_width, client_height)

    [screenshot.getpixel(point) for point in points]
    # hyper_point_colors = [screenshot.getpixel(hyper_point) for hyper_point in hyper_points]
    # Debug helpers (commented out to avoid unused-variable warnings)
    # point_colors_up1 = [screenshot.getpixel((point[0], point[1] - 1)) for point in points]
    # point_colors_down1 = [screenshot.getpixel((point[0], point[1] + 1)) for point in points]
    # point_colors_left1 = [screenshot.getpixel((point[0] - 1, point[1])) for point in points]
    # point_colors_right1 = [screenshot.getpixel((point[0] + 1, point[1])) for point in points]
    # point_colors_up2 = [screenshot.getpixel((point[0], point[1] - 2)) for point in points]
    # point_colors_down2 = [screenshot.getpixel((point[0], point[1] + 2)) for point in points]
    # point_colors_left2 = [screenshot.getpixel((point[0] - 2, point[1])) for point in points]
    # point_colors_right2 = [screenshot.getpixel((point[0] + 2, point[1])) for point in points]

    # # 使用 ImageDraw 在截图上绘制点
    # draw=ImageDraw.Draw(screenshot)

    # # 绘制点（用红色和蓝色表示）
    # for point in points:
    #     draw.ellipse(
    #         (point[0] - 5, point[1] - 5, point[0] + 5, point[1] + 5), fill="red"
    #     )

    # # 显示截图
    # screenshot.show()

    # exit()


def is_window_on_top(window):
    top_window_hwnd = win32gui.GetForegroundWindow()
    return top_window_hwnd == window._hWnd


def main():
    global running  # noqa: F824
    global focus  # noqa: F824
    global window  # noqa: F824
    global low_performance_state  # noqa: F824
    while True:
        start_time = time.time()
        now_focus = is_window_on_top(window)
        if now_focus and not focus:
            focus = True
            # overlay_window.updateStatus()
            safeChangeToggleButton()

        elif not now_focus and focus:
            focus = False
            # overlay_window.updateStatus()
            safeChangeToggleButton()

        if not running or not focus:
            time.sleep(0.1)
            continue

        client_left, client_top, _, _, y_value, min_x, max_x = (
            overlay_window.getWindowInfo()
        )

        # 满足条件，开始打歌
        screenshot = capture_screenshot(
            client_left + min_x, client_top + y_value, max_x - min_x + 1, 1
        )

        point_colors = [
            screenshot.getpixel(
                (point[0] - min_x, 0)
            )  # x 坐标相对于截取区域的调整，y 坐标始终为 0
            for point in points
        ]

        for i, color in enumerate(point_colors):
            if key_states[keys[i]] > 0:
                key_states[keys[i]] += 1

            r, g, b = color
            # original_r, original_g, original_b = original_points_colors[i]
            # 判断color的三个数字是不是处于original_points_colors[i]和original_red_points_colors[i]之间

            original_flag = (
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
            original_color = blue_points_colors[i]

            if original_flag:
                keyboard_controller.release(keys[i])
                key_states[keys[i]] = 0
                continue

            if (
                r < original_red_points_colors[i][0] - COLOR_TOLERANCE
                or g < original_red_points_colors[i][1] - COLOR_TOLERANCE
                or b < original_red_points_colors[i][2] - COLOR_TOLERANCE
                or (r > 210 and g > 210 and b > 210)
            ) and key_states[keys[i]] == 0:
                keyboard_controller.press(keys[i])
                key_states[keys[i]] += 1
                continue

            if key_states[keys[i]] > hold_th and (
                abs(color[0] - original_color[0]) > COLOR_TOLERANCE
                or abs(color[1] - original_color[1]) > COLOR_TOLERANCE
                or abs(color[2] - original_color[2]) > COLOR_TOLERANCE
            ):
                keyboard_controller.release(keys[i])
                key_states[keys[i]] = 0
                continue
            # time.sleep(0.01)
        running_time = time.time() - start_time
        if running_time < single_run_time:
            time.sleep(single_run_time - running_time)
        elif not low_performance_state and running_time > single_run_time * 2:
            low_performance_state = True
            deactivate_window()


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
    app, overlay_window = create_overlay(points)
    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()
    keyboard_controller = Controller()
    keys = ["z", "x", "c", "v", "b", "n"]
    key_states = {key: 0 for key in keys}

    original_points_colors = [
        (219, 57, 222),
        (208, 41, 211),
        (132, 49, 147),
        (118, 49, 137),
        (158, 51, 170),
        (118, 50, 138),
    ]
    original_red_points_colors = [
        (211, 54, 211),
        (201, 39, 201),
        (130, 47, 141),
        (117, 47, 132),
        (154, 49, 163),
        (117, 48, 133),
    ]
    # original_hyper_points_colors = [(79, 40, 96), (79, 40, 94), (78, 40, 93), (77, 40, 92), (77, 40, 91), (76, 40, 90)]

    blue_points_colors = [
        (162, 171, 250),
        (151, 165, 247),
        (125, 144, 244),
        (94, 116, 241),
        (81, 104, 240),
        (85, 115, 236),
    ]
    # blue_red_points_colors = [,(146, 155, 235),,(95, 106, 224)]

    # 增加颜色容差范围
    COLOR_TOLERANCE = 10
    running = False
    focus = False

    # 创建一个新线程来激活主循环

    main_thread = Thread(target=lambda: main())
    main_thread.daemon = True
    main_thread.start()

    # 启动Qt事件循环
    sys.exit(app.exec_())
