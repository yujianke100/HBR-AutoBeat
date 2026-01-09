import sys
import time
from typing import List, Optional, Tuple

import win32con
import win32gui
import win32ui
from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMessageBox

from i18n import t


def find_hbr_window(window_title: str) -> Optional[int]:
    """Find the window handle (hwnd) for the given partial title."""
    hwnds: List[int] = []

    def callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if window_title in title:
                hwnds.append(hwnd)
        return True

    win32gui.EnumWindows(callback, None)
    return hwnds[0] if hwnds else None


def deactivate_window(
    window_title: str = "HeavenBurnsRed", suppress_messages: bool = False
) -> None:
    hwnd = find_hbr_window(window_title)
    if hwnd is None:
        if suppress_messages:
            return
        # Use existing app if it exists, otherwise create temporary one
        app = QApplication.instance()
        if not app:
            app = QApplication(sys.argv)
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Window Not Found")
        msg_box.setText(t("hbr_not_found", "en-US")) # Defaulting or using local if initialized
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowStaysOnTopHint)
        msg_box.exec_()
        sys.exit()

    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    time.sleep(0.5)


def reactivate_window(
    window_title: str = "HeavenBurnsRed", suppress_messages: bool = False
) -> None:
    hwnd = find_hbr_window(window_title)
    if hwnd is None:
        if suppress_messages:
            return
        app = QApplication.instance()
        if not app:
            app = QApplication(sys.argv)
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle(t("window_not_found", "Window Not Found"))
        msg_box.setText(t("hbr_not_found", "HBR was not found."))
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowStaysOnTopHint)
        msg_box.exec_()
        sys.exit()

    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.5)


def init(
    window_title: str, points: list, test_flag: bool = False
) -> Tuple[int, int, int, int, int, int, int]:
    """Return (client_left, client_top, client_width, client_height, y_value, min_x, max_x)"""
    # allow caller to suppress message boxes when running in background
    reactivate_window(window_title, suppress_messages=test_flag)

    hwnd = find_hbr_window(window_title)
    if hwnd is None: # Should not happen after reactivate_window
        sys.exit()

    client_rect = win32gui.GetClientRect(hwnd)
    client_left, client_top = win32gui.ClientToScreen(
        hwnd, (client_rect[0], client_rect[1])
    )
    client_right, client_bottom = win32gui.ClientToScreen(
        hwnd, (client_rect[2], client_rect[3])
    )
    client_width = client_right - client_left
    client_height = client_bottom - client_top

    if client_width != 1920 or client_height != 1080:
        if test_flag:
            raise RuntimeError("resolution-mismatch")
        app = QApplication.instance()
        if not app:
            app = QApplication(sys.argv)
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle(t("resolution_error", "Resolution Error"))
        msg = (
            t("resolution_mismatch", "Window resolution does not match.\n")
            + t(
                "resolution_hint",
                f"It needs to be set to 1920x1080, currently recognized as {client_width}x{client_height}.\n",
            ).format(client_width=client_width, client_height=client_height)
            + t("resolution_reset", "Please reset the resolution in the game.")
        )
        msg_box.setText(msg)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowStaysOnTopHint)
        msg_box.exec_()
        sys.exit()

    y_value = points[0][1]
    min_x = min(point[0] for point in points)
    max_x = max(point[0] for point in points)

    return client_left, client_top, client_width, client_height, y_value, min_x, max_x


def capture_screenshot(left: int, top: int, width: int, height: int) -> Image.Image:
    hdesktop = win32gui.GetDesktopWindow()
    hwindow = win32gui.GetWindowDC(hdesktop)
    srcdc = win32ui.CreateDCFromHandle(hwindow)
    memdc = srcdc.CreateCompatibleDC()

    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)

    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

    signed_ints_array = bmp.GetBitmapBits(True)
    img = Image.frombuffer(
        "RGB", (width, height), signed_ints_array, "raw", "BGRX", 0, 1
    )

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hdesktop, hwindow)
    win32gui.DeleteObject(bmp.GetHandle())

    return img

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
