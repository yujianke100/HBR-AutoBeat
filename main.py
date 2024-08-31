import pyautogui
import pygetwindow as gw
import win32gui
from PIL import ImageDraw, Image
from pynput.keyboard import Controller, Key
import win32ui
import win32con
import time

keyboard = Controller()
keys = ['z', 'x', 'c', ',', '.', '/']
key_states = {key: 0 for key in keys}  # 跟踪按键状态

points = [(325, 810), (575, 810), (825, 810), (1075, 810), (1325, 810), (1575, 810)]
# hyper_points = [(375, 740), (609, 740), (838, 740), (1063, 740), (1293, 740), (1522, 740)]

original_points_colors = [(219, 57, 222), (208, 41, 211), (132, 49, 147), (118, 49, 137), (158, 51, 170), (118, 50, 138)]
original_red_points_colors = [(211, 54, 211), (201, 39, 201), (130, 47, 141), (117, 47, 132), (154, 49, 163), (117, 48, 133)]
# original_hyper_points_colors = [(79, 40, 96), (79, 40, 94), (78, 40, 93), (77, 40, 92), (77, 40, 91), (76, 40, 90)]

blue_points_colors = [(161, 171, 250), (151, 165, 247), (125, 144, 244), (94, 116, 241), (81, 104, 240), (85, 115, 238)]
# blue_red_points_colors = [,(146, 155, 235),,(95, 106, 224)]

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
        'RGB',
        (bmp_info['bmWidth'], bmp_info['bmHeight']),
        bmp_str, 'raw', 'BGRX', 0, 1)
    
    win32gui.DeleteObject(bmp.GetHandle())
    memdc.DeleteDC()
    srcdc.DeleteDC()
    win32gui.ReleaseDC(hdesktop, hwindow)
    
    return img

def test(client_left, client_top, client_width, client_height):
    screenshot = capture_screenshot(client_left, client_top, client_width, client_height)

    point_colors = [screenshot.getpixel(point) for point in points]
    # hyper_point_colors = [screenshot.getpixel(hyper_point) for hyper_point in hyper_points]
    print(point_colors)

    # 使用 ImageDraw 在截图上绘制点
    draw = ImageDraw.Draw(screenshot)
    
    # 绘制点（用红色和蓝色表示）
    for point in points:
        draw.ellipse((point[0] - 5, point[1] - 5, point[0] + 5, point[1] + 5), fill='red')
    
    
    # 显示截图
    screenshot.show()

    exit()

def is_window_on_top(window):
    top_window_hwnd = win32gui.GetForegroundWindow()
    return top_window_hwnd == window._hWnd

def capture_window(window_title, test_flag=False):
    all_windows = gw.getAllTitles()
    browser_window_titles = [title for title in all_windows if window_title in title]
    chosen_browser_title = browser_window_titles[0]
    window = gw.getWindowsWithTitle(chosen_browser_title)[0]
    window.restore()
    window.activate()
    time.sleep(0.5)
    
    hwnd = window._hWnd
    
    client_rect = win32gui.GetClientRect(hwnd)
    client_left, client_top = win32gui.ClientToScreen(hwnd, (client_rect[0], client_rect[1]))

    if(test_flag):
        client_right, client_bottom = win32gui.ClientToScreen(hwnd, (client_rect[2], client_rect[3]))
        client_width = client_right - client_left
        client_height = client_bottom - client_top
        test(client_left, client_top, client_width, client_height)
        
    y_value = points[0][1]

    min_x = min(point[0] for point in points)
    max_x = max(point[0] for point in points)

    print('start!')
    while True:
        if not is_window_on_top(window):
            print('closed!')
            exit()

        screenshot = capture_screenshot(client_left + min_x, client_top + y_value, max_x - min_x + 1, 1)

        point_colors = [
            screenshot.getpixel((point[0] - min_x, 0))  # x 坐标相对于截取区域的调整，y 坐标始终为 0
            for point in points
        ]

        for i, color in enumerate(point_colors):
            
            if key_states[keys[i]] > 0:
                key_states[keys[i]] += 1

            r, g, b = color
            # original_r, original_g, original_b = original_points_colors[i]
            # 判断color的三个数字是不是处于original_points_colors[i]和original_red_points_colors[i]之间
            
            original_flag = (r >= original_red_points_colors[i][0] and r <= original_points_colors[i][0]) and (g >= original_red_points_colors[i][1] and g <= original_points_colors[i][1]) and (b >= original_red_points_colors[i][2] and b <= original_points_colors[i][2])
            original_color = blue_points_colors[i]

            if (original_flag):
                keyboard.release(keys[i])
                key_states[keys[i]] = 0
                continue

            if (r < original_red_points_colors[i][0] or g < original_red_points_colors[i][1] or b < original_red_points_colors[i][2] or (r > 210 and g > 210 and b > 210)) and key_states[keys[i]] == 0:
                keyboard.press(keys[i])
                key_states[keys[i]] += 1
                continue

            if key_states[keys[i]] > 5 and color != original_color:
                keyboard.release(keys[i])
                key_states[keys[i]] = 0
 
                continue
            # time.sleep(0.01)

if __name__ == "__main__":
    capture_window("HeavenBurnsRed", test_flag=False)
