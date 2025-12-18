import time

import pyautogui  # 不能省，否则会让窗口识别失效  # noqa: F401
import pygetwindow as gw
import win32con
import win32gui
import win32ui
from PIL import Image, ImageDraw
from pynput import keyboard
from pynput.keyboard import Controller, Key, KeyCode, Listener  # noqa: F401


def capture_screenshot(left, top, width, height):
    hdesktop = win32gui.GetDesktopWindow()
    hwindow = win32gui.GetWindowDC(hdesktop)
    srcdc = win32ui.CreateDCFromHandle(hwindow)
    memdc = srcdc.CreateCompatibleDC()

    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)

    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

    bmp_info = bmp.GetInfo()
    bmp_str = bmp.GetBitmapBits(True)

    img = Image.frombuffer(
        "RGB", (bmp_info["bmWidth"], bmp_info["bmHeight"]), bmp_str, "raw", "BGRX", 0, 1
    )

    win32gui.DeleteObject(bmp.GetHandle())
    memdc.DeleteDC()
    srcdc.DeleteDC()
    win32gui.ReleaseDC(hdesktop, hwindow)

    return img


def test(client_left, client_top, client_width, client_height):
    screenshot = capture_screenshot(
        client_left, client_top, client_width, client_height
    )

    point_colors = [screenshot.getpixel(point) for point in points]
    # hyper_point_colors = [screenshot.getpixel(hyper_point) for hyper_point in hyper_points]
    print(point_colors)

    # 使用 ImageDraw 在截图上绘制点
    draw = ImageDraw.Draw(screenshot)

    # 绘制点（用红色和蓝色表示）
    for point in points:
        draw.ellipse(
            (point[0] - 5, point[1] - 5, point[0] + 5, point[1] + 5), fill="red"
        )

    # 显示截图
    screenshot.show()

    exit()


def is_window_on_top(window):
    top_window_hwnd = win32gui.GetForegroundWindow()
    return top_window_hwnd == window._hWnd


def on_press(key):
    global running
    try:
        if is_window_on_top(window):  # 仅在窗口聚焦时检测输入
            if key.char == "o":  # 按下 'o' 键开始自动演奏
                running = True
                print("正在打歌，按'p'停止!")
            elif key.char == "p":  # 按下 'p' 键停止自动演奏
                running = False
                print("已停止打歌，按'o'继续!")
                # 模拟esc
                keyboard.press(Key.esc)
                keyboard.release(Key.esc)
    except AttributeError:
        pass


# 释放按键
def on_release(key):
    pass


def main(window_title, test_flag=False):
    global running
    global window  # 声明为全局变量，以便在 on_press 中访问
    global force_run  # noqa: F824
    all_windows = gw.getAllTitles()
    browser_window_titles = [title for title in all_windows if window_title in title]
    if browser_window_titles == []:
        print("未找到指定窗口，请检查窗口标题是否正确！")
        exit()
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
        print("窗口分辨率：", client_width, client_height)
        test(client_left, client_top, client_width, client_height)

    if client_width != 1920 or client_height != 1080:
        print(
            f"窗口分辨率不匹配。需要设置为1920x1080，当前识别为{client_width}x{client_height}，请重新在游戏内设置分辨率。按回车退出。"
        )
        input()
        exit()

    y_value = points[0][1]

    min_x = min(point[0] for point in points)
    max_x = max(point[0] for point in points)

    # print("已聚焦！")
    closed_printed = True  # 添加标志变量
    while True:
        if not is_window_on_top(window):
            if not closed_printed:
                if force_run != "y":
                    print("未聚焦！聚焦后按 'o' 键开始打歌，按 'p' 键停止")
                else:
                    print("未聚焦！已强制运行，聚焦后继续打歌")
                running = False  # 窗口未聚焦时停止打歌
                closed_printed = True  # 设置标志，确保只打印一次
            time.sleep(0.1)  # 添加延迟，减少CPU占用
            continue
        else:
            if closed_printed:
                print("已聚焦！", end=" ")  # 窗口重新聚焦时打印“已聚焦”
                if force_run == "y":
                    print("已强制运行")
                    running = True
                elif running:
                    print("正在打歌，按 'p' 键停止")
                else:
                    print("按 'o' 键开始打歌")
            closed_printed = False  # 窗口重新聚焦时重置标志

        if not running:
            time.sleep(0.1)
            continue

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
                keyboard.release(keys[i])
                key_states[keys[i]] = 0
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
                key_states[keys[i]] = 0

                continue
            # time.sleep(0.01)


if __name__ == "__main__":
    force_run = input(
        "是否强制运行？（y/n）,默认n。如强制运行，请先打开‘演唱会开始’界面，然后输入y："
    )

    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()
    keyboard = Controller()  # noqa: F811
    keys = ["z", "x", "c", "v", "b", "n"]
    key_states = {key: 0 for key in keys}  # 跟踪按键状态

    points = [(325, 810), (575, 810), (825, 810), (1075, 810), (1325, 810), (1575, 810)]
    # hyper_points = [(375, 740), (609, 740), (838, 740), (1063, 740), (1293, 740), (1522, 740)]

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
    main("HeavenBurnsRed", test_flag=False)
