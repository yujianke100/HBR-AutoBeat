# HBR-AutoBeat
An automated rhythm game player script for Heaven Burns Red

**该脚本只用于获取奖励，不提倡用于冲高分。**

**This script is intended solely for obtaining rewards and is not recommended for use in achieving high scores.**

**このスクリプトは報酬を得るためだけに使用され、高得点を狙うために使用することは推奨されません。**

[OD条刻度尺](https://github.com/yujianke100/HBR-OD-Ruler)

## 说明

**总结几个常见问题。**
- 打开脚本后游戏没开始：手动点开始，脚本只管打歌
- 只按半边：源代码按键设置是zxc,./，HBR-AutoBeat_zxcvbn.exe才是默认的zxcvbn。
- 点按正常长按变点按：按键大小改为80%。
- 闪退：确定是steam客户端，窗口名称为HeavenBurnsRed
- 疯狂连点：确认游戏是1080p，1080p屏幕应该设置100%缩放，2k我测试125%正常
- 全miss：确认脚本还开着、按键设置正确、打开脚本后已回到了游戏、游戏左上角和下方所有按键没被遮挡。**还有人通过管理员权限打开解决的**。cpu占满了还miss的话是电脑性能不够。
- 不能完美全连：故意的，我分享这个脚本是为了帮你拿奖励，不是为了攻击大佬
- 能自己凹到完美吗：和拿奖励无关，完全不推荐。hard及以上有一个逻辑我直接没做，但normal的全做了，理论上能全完美。想凹就确认好配置以及脚本运行效率(全完美重点是响应得够快，逻辑再严，脚本开个小差就G了)，然后给不同的歌凹设置

[NGA帖子传送门](https://bbs.nga.cn/read.php?&tid=41488250)

纯自用的脚本，没做任何兼容。策略非常暴力，直接靠像素点颜色变化实现。如果残血特效影响到判定点，就会失效。只优化到了hard打SS为止，打不了高分，只求打个石头。

音游相关设置可以看这个[视频](https://www.bilibili.com/video/BV1ePH7eSEwJ)的结尾。
最重要的是要把按键大小调整到80%，然后把同时按压线显示关掉

**脚本会在游戏濒临失败时因为红色光效而失效。**

测试了下，1080p显示器下开1080p游戏窗口也是能用的，就是要确保窗口左上角露出来的同时右下角的判定区域别被遮了就行。低于这个分辨率的电脑，性能估计也跑不了这个脚本。

为了方便小白，已经打包成exe可以一键启动了：

[zxcvbn 版本 (默认)](https://github.com/yujianke100/HBR-AutoBeat/releases/download/v1.0/HBR-AutoBeat_zxcvbn.exe)

[zxc,./ 版本](https://github.com/yujianke100/HBR-AutoBeat/releases/download/v1.0/HBR-AutoBeat.exe)

就不上传大陆网盘了，上不了gayhub的话你应该也玩不了红烧天堂的外服吧。

注意，启动脚本前先把游戏开到“演唱会开始”的界面，再启动脚本。脚本会自动切回游戏，然后按开始就行了。结束了就最小化游戏/切到游戏外面，脚本就会退出。


## Heaven Burns Red Auto Rhythm Game Player


[Demo video](https://www.bilibili.com/video/BV1ePH7eSEwJ)

**Need to adjust the button size to 80% and turn off the simultaneous press line display.**

Run it without setting up a Python environment: 

[zxcvbn version (default)](https://github.com/yujianke100/HBR-AutoBeat/releases/download/v1.0/HBR-AutoBeat_zxcvbn.exe)

[zxc,./ version](https://github.com/yujianke100/HBR-AutoBeat/releases/download/v1.0/HBR-AutoBeat.exe)

**The script will fail due to the red visual effects when the game is about to fail.**

### Test Environment
- **Operating System**: Windows 11
- **Screen Resolution**: 1440p (Also tested under 1080p)
- **Game Settings**: 1080p, Windowed Mode

### Usage Instructions
1. Run the script before starting the rhythm game. Ensure that the top left corner and the judgment area on the far right are uncovered.
2. The script will be exited automatically if the game window is not in focus.

## 日本語

ヘブンバーンズレッド用の自動ライブモード（音ゲー）プレイヤースクリプト

最高得点を狙うわけではなく、ハードでSSランクを取るために最適化してありますが、高得点を目指すことはできません。ただ、報酬を確保するためのものです。

**ゲームが失敗しそうなときに、赤い光のエフェクトによってスクリプトが機能しなくなります。**

音ゲーの設定については、この[動画](https://www.bilibili.com/video/BV1ePH7eSEwJ)の最後の部分をご覧ください。
最も重要なのは、ボタンのサイズを80％に調整し、同時押しラインの表示をオフにすることです。

1080pモニターで1080pのゲームウィンドウを使用しても動作確認済みです。ただし、ウィンドウの左上が表示されている状態で、右下の判定エリアが隠れないようにする必要があります。それより低い解像度のPCでは、このスクリプトを動作させる性能はないかもしれません。

初心者のために、すでにexeファイルとしてパッケージ化してあり、ワンクリックで起動できます：

[zxcvbn バージョン （デフォルト）](https://github.com/yujianke100/HBR-AutoBeat/releases/download/v1.0/HBR-AutoBeat_zxcvbn.exe)

[zxc,./ バージョン ](https://github.com/yujianke100/HBR-AutoBeat/releases/download/v1.0/HBR-AutoBeat.exe)

スクリプトを起動する前に、ゲームを「ライブ開始」画面まで進めてからスクリプトを起動してください。スクリプトは自動的にゲームに切り替え、スタートボタンを押すだけで始まります。終了したら、ゲームを最小化するか、他のウィンドウに切り替えるとスクリプトは自動的に終了します。
