<p align="center">
  <img src="icon/logo.jpg" alt="HBR-AutoBeat" width="256" />
</p>

# HBR-AutoBeat

[![Release](https://img.shields.io/github/v/release/yujianke100/HBR-AutoBeat)](https://github.com/yujianke100/HBR-AutoBeat/releases/latest) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Languages](https://img.shields.io/badge/languages-zh%20%7C%20en%20%7C%20ja-blue)](README.md)

Language: **English**  other translations: [简体中文](README_zh-CN.md)  [日本語](README_ja-JP.md)

AutoBeat helper tool for Heaven Burns Red (HBR).

![screenshot](figs/screenshot.png)

## Quickstart

Download the latest release and run the bundled executable:

- https://github.com/yujianke100/HBR-AutoBeat/releases/latest

Developer quickstart (see `docs/HOWTO.md` for details)


## Features

- Auto Song Play

## Usage Instructions

### Auto Song Play

This script is designed only for obtaining rewards. High-difficulty logic is not fully implemented to prevent high-score abuse.

This is a self-use script with no compatibility considerations. The strategy is straightforward and pixel-color-based. If residual effects interfere with detection points, it may fail. Optimized for Hard SS rank only, cannot achieve top scores, intended for reward collection.

#### Setup Instructions

- Launch the game and set resolution to 1080P (1920  1080).
- Open the software.
- Configure play settings: reset to default, set background to "None", adjust key size to 80%, and disable "Show simultaneous press line".
- Use the "Detect Game Window" button to align to the game window. Re-detect if the game window moves.
- Ensure the game is at the "Concert Start" screen. After clicking the activate button, return to the game. When both activate and focus buttons turn green, click "Concert Start" to begin auto play.

#### Troubleshooting

- Key press delays: Try adjusting key size to 80%.
- Application crashes: Verify you are using the Steam client and the window title is `HeavenBurnsRed`.
- Rapid tapping or performance issues: Set system scaling to 100% (125% may work on 2K displays). In a multi-monitor setup, please ensure the game window is running on the primary monitor. Also, make sure the game window is not obscured by other windows to maintain accurate coordinate recognition. You can try using "Offset Detection" to test if the recognition position is incorrect. **Color Offset Correction**: If detection is inaccurate (e.g., `RGB: (x, y, z)` values mismatch expectations), **pause the game immediately after starting** (as shown in the screenshot below), ensuring Notes are visible or at the judgment line. Then click "Offset Detection". The software will automatically calculate the offset and prompt you to save.

  ![offset-detect](figs/offset_detection.png)

- Complete misses: Confirm the script is running, keys are correctly configured, the game window is fully visible, and try running as administrator if needed.

Discussion:

- NGA Forum (Latest): https://bbs.nga.cn/read.php?tid=43140018&_ff=510381

Video and Settings Guide:

- View example video: https://www.bilibili.com/video/BV1ePH7eSEwJ (Setup and key size configuration)
