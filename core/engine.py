import time
from threading import Thread
from typing import List, Tuple

import pygetwindow as gw
import win32gui
from pynput.keyboard import Controller, Key
from PyQt5.QtCore import QMetaObject, Qt

from core import window_helpers


class AutoSongEngine:
    def __init__(
        self,
        overlay_window,
        points: List[Tuple[int, int]],
        hold_th=10,
        single_run_time=0.015,
    ):
        self.overlay_window = overlay_window
        self.points = points
        self.hold_th = hold_th
        self.single_run_time = single_run_time

        self.keyboard_controller = Controller()
        self.keys = ["z", "x", "c", "v", "b", "n"]
        self.key_states = {k: 0 for k in self.keys}

        self.original_points_colors = [
            (219, 57, 222),
            (208, 41, 211),
            (132, 49, 147),
            (118, 49, 137),
            (158, 51, 170),
            (118, 50, 138),
        ]
        self.original_red_points_colors = [
            (211, 54, 211),
            (201, 39, 201),
            (130, 47, 141),
            (117, 47, 132),
            (154, 49, 163),
            (117, 48, 133),
        ]
        self.blue_points_colors = [
            (162, 171, 250),
            (151, 165, 247),
            (125, 144, 244),
            (94, 116, 241),
            (81, 104, 240),
            (85, 115, 236),
        ]

        self.COLOR_TOLERANCE = 10
        self.running = False
        self.focus = False
        self.low_performance_state = False
        self._thread = None
        self.window_title = "HeavenBurnsRed"

    def is_window_on_top(self):
        try:
            top_window_hwnd = win32gui.GetForegroundWindow()
            all_titles = gw.getAllTitles()
            browser_window_titles = [
                title for title in all_titles if self.window_title in title
            ]
            if not browser_window_titles:
                return False
            chosen_title = browser_window_titles[0]
            window = gw.getWindowsWithTitle(chosen_title)[0]
            return top_window_hwnd == window._hWnd
        except Exception:
            return False

    def safeChangeToggleButton(self):
        QMetaObject.invokeMethod(
            self.overlay_window, "updateStatus", Qt.QueuedConnection
        )

    def on_press(self, key):
        try:
            if self.is_window_on_top():
                if hasattr(key, "char") and key.char == "o":
                    self.running = True
                elif hasattr(key, "char") and key.char == "p":
                    self.running = False
                    self.keyboard_controller.press(Key.esc)
                    self.keyboard_controller.release(Key.esc)
            self.safeChangeToggleButton()
        except AttributeError:
            pass

    def on_release(self, key):
        pass

    def toggle_running(self):
        self.running = not self.running
        self.safeChangeToggleButton()

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._thread = Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def _run_loop(self):
        while True:
            start_time = time.time()
            now_focus = self.is_window_on_top()
            if now_focus and not self.focus:
                self.focus = True
                self.safeChangeToggleButton()

            elif not now_focus and self.focus:
                self.focus = False
                self.safeChangeToggleButton()

            if not self.running or not self.focus:
                time.sleep(0.1)
                continue

            client_left, client_top, _, _, y_value, min_x, max_x = (
                self.overlay_window.getWindowInfo()
            )

            screenshot = window_helpers.capture_screenshot(
                client_left + min_x, client_top + y_value, max_x - min_x + 1, 1
            )

            point_colors = [
                screenshot.getpixel((point[0] - min_x, 0)) for point in self.points
            ]

            for i, color in enumerate(point_colors):
                if self.key_states[self.keys[i]] > 0:
                    self.key_states[self.keys[i]] += 1

                r, g, b = color
                original_flag = (
                    (
                        r
                        >= self.original_red_points_colors[i][0] - self.COLOR_TOLERANCE
                        and r
                        <= self.original_points_colors[i][0] + self.COLOR_TOLERANCE
                    )
                    and (
                        g
                        >= self.original_red_points_colors[i][1] - self.COLOR_TOLERANCE
                        and g
                        <= self.original_points_colors[i][1] + self.COLOR_TOLERANCE
                    )
                    and (
                        b
                        >= self.original_red_points_colors[i][2] - self.COLOR_TOLERANCE
                        and b
                        <= self.original_points_colors[i][2] + self.COLOR_TOLERANCE
                    )
                )
                original_color = self.blue_points_colors[i]

                if original_flag:
                    try:
                        self.keyboard_controller.release(self.keys[i])
                    except Exception:
                        pass
                    self.key_states[self.keys[i]] = 0
                    continue

                if (
                    r < self.original_red_points_colors[i][0] - self.COLOR_TOLERANCE
                    or g < self.original_red_points_colors[i][1] - self.COLOR_TOLERANCE
                    or b < self.original_red_points_colors[i][2] - self.COLOR_TOLERANCE
                    or (r > 210 and g > 210 and b > 210)
                ) and self.key_states[self.keys[i]] == 0:
                    try:
                        self.keyboard_controller.press(self.keys[i])
                    except Exception:
                        pass
                    self.key_states[self.keys[i]] += 1
                    continue

                if self.key_states[self.keys[i]] > self.hold_th and (
                    abs(color[0] - original_color[0]) > self.COLOR_TOLERANCE
                    or abs(color[1] - original_color[1]) > self.COLOR_TOLERANCE
                    or abs(color[2] - original_color[2]) > self.COLOR_TOLERANCE
                ):
                    try:
                        self.keyboard_controller.release(self.keys[i])
                    except Exception:
                        pass
                    self.key_states[self.keys[i]] = 0
                    continue

            running_time = time.time() - start_time
            if running_time < self.single_run_time:
                time.sleep(self.single_run_time - running_time)
            elif (
                not self.low_performance_state
                and running_time > self.single_run_time * 2
            ):
                self.low_performance_state = True
                window_helpers.deactivate_window()


__all__ = ["AutoSongEngine"]
