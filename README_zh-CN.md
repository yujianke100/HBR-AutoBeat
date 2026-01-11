<p align="center">
  <img src="icon/logo.jpg" alt="HBR-AutoBeat" width="256" />
</p>

# HBR-AutoBeat

[![Release](https://img.shields.io/github/v/release/yujianke100/HBR-AutoBeat)](https://github.com/yujianke100/HBR-AutoBeat/releases/latest) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Languages](https://img.shields.io/badge/languages-zh%20%7C%20en%20%7C%20ja-blue)](README.md)


语言：**简体中文** — 其他： [English](README.md) · [日本語](README_ja-JP.md)

这是用于 Heaven Burns Red (HBR) 的 AutoBeat 辅助工具。

![screenshot](figs/screenshot.png)

## 快速开始

直接使用已打包的 [EXE可执行文件](https://github.com/yujianke100/HBR-AutoBeat/releases/latest) 使用软件。开发者可查阅 [开发文档](./docs/HOWTO.md)

## 现有功能

- 自动打歌

## 说明与常见问题

### 打歌功能

该脚本只用于获取奖励。高难度下的部分逻辑未实现，以确保本脚本无法冲高分。

纯自用的脚本，没做任何兼容。策略非常暴力，直接靠像素点颜色变化实现。如果残血特效影响到判定点，就会失效。只优化到了 hard 打 SS 为止，打不了高分，只求拿奖励。

#### 使用说明

- 打开游戏，设置为1080P （1920 x 1080）。
- 打开软件。
- 打歌设置，恢复默认，然后背景设置为“无”，按键大小改为 80%，关闭“同时按压线显示”。
- 使用“识别游戏窗口”按钮对齐游戏窗口。游戏窗口位置改变后需要重新识别。
- 确保处在“演唱会开始”界面，点击激活按钮后，回到游戏。当激活和聚焦按钮变绿，即可点击“演唱会开始”自动打歌


#### 常见问题
- 点按变长按问题：尝试将按键大小调整为 80%。
- 应用闪退：确认使用的是 Steam 客户端且窗口名为 `HeavenBurnsRed`。
- 疯狂连点或性能问题：建议将系统缩放设置为 100%（若为 2K 屏可尝试 125%）。在多显示器环境下，请务必将游戏窗口放在主显示器上运行，并确保游戏窗口未被其他窗口遮挡，以保证坐标识别的准确性。可以尝试使用“偏移检测”测试是否为识别位置不对。正确的识别结果如下： 

  ![offset-detect](figs/offset_detection.png)

- 全 miss：确认脚本已启动、按键设置正确、游戏窗口未被遮挡。以管理员权限运行在部分环境可解决问题。
- **色彩偏移修复**：若发现识别不准（如显示 `RGB: (x, y, z)` 与预期不符），请在**打歌开始后立刻点击暂停**（如下图所示），保持背景有 Note 经过或在判定线位置，随后点击“偏移检测”。软件会自动计算偏移并提示保存。

  ![pause_example](figs/offset_detection.png)

更多讨论：[NGA 帖子](https://bbs.nga.cn/read.php?tid=43140018&_ff=510381)

视频与设置建议：[观看示例视频](https://www.bilibili.com/video/BV1ePH7eSEwJ)（初始化与按键设置）

