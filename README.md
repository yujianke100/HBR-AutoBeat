# HBR-AutoBeat
An automated rhythm game player script for Heaven Burns Red


## Heaven Burns Red Auto Rhythm Game Player

[Demo video](https://www.bilibili.com/video/BV1ePH7eSEwJ)

Run it without setting up a Python environment: 

[zxcvbn version (default)](https://github.com/yujianke100/HBR-AutoBeat/releases/download/v1.0/HBR-AutoBeat_zxcvbn.exe)

[zxc,./ version](https://github.com/yujianke100/HBR-AutoBeat/releases/download/v1.0/HBR-AutoBeat.exe)

**The script will fail due to the red visual effects when the game is about to fail.**

### Test Environment
- **Operating System**: Windows 11
- **Screen Resolution**: 1440p (Also tested under 1080p)
- **Game Settings**: 1080p, Windowed Mode

Other settings are at the end of the demo video.

### Usage Instructions
1. Run the script before starting the rhythm game. Ensure that the top left corner and the judgment area on the far right are uncovered.
2. The script will be exited automatically if the game window is not in focus.

## 中文说明

纯自用的脚本，没做任何兼容。策略非常暴力，直接靠像素点颜色变化实现。如果残血特效影响到判定点，就会失效。只优化到了hard打SS为止，打不了高分，只求打个石头。

音游相关设置可以看这个[视频](https://www.bilibili.com/video/BV1ePH7eSEwJ)的结尾。

**脚本会在游戏濒临失败时因为红色光效而失效。**

测试了下，1080p显示器下开1080p游戏窗口也是能用的，就是要确保窗口左上角露出来的同时右下角的判定区域别被遮了就行。低于这个分辨率的电脑，性能估计也跑不了这个脚本。

为了方便小白，已经打包成exe可以一键启动了：

[zxcvbn 版本 (默认)](https://github.com/yujianke100/HBR-AutoBeat/releases/download/v1.0/HBR-AutoBeat_zxcvbn.exe)

[zxc,./ 版本](https://github.com/yujianke100/HBR-AutoBeat/releases/download/v1.0/HBR-AutoBeat.exe)

就不上传大陆网盘了，上不了gayhub的话你应该也玩不了红烧天堂的外服吧。

注意，启动脚本前先把游戏开到“演唱会开始”的界面，再启动脚本。脚本会自动切回游戏，然后按开始就行了。结束了就最小化游戏/切到游戏外面，脚本就会退出。

## 日本語

ヘブンバーンズレッド用の自動ライブモード（音ゲー）プレイヤースクリプト

最高得点を狙うわけではなく、ハードでSSランクを取るために最適化してありますが、高得点を目指すことはできません。ただ、報酬を確保するためのものです。

**ゲームが失敗しそうなときに、赤い光のエフェクトによってスクリプトが機能しなくなります。**

音ゲーの設定については、この[動画](https://www.bilibili.com/video/BV1ePH7eSEwJ)の最後の部分をご覧ください。

1080pモニターで1080pのゲームウィンドウを使用しても動作確認済みです。ただし、ウィンドウの左上が表示されている状態で、右下の判定エリアが隠れないようにする必要があります。それより低い解像度のPCでは、このスクリプトを動作させる性能はないかもしれません。

初心者のために、すでにexeファイルとしてパッケージ化してあり、ワンクリックで起動できます：

[zxcvbn バージョン （デフォルト）](https://github.com/yujianke100/HBR-AutoBeat/releases/download/v1.0/HBR-AutoBeat_zxcvbn.exe)

[zxc,./ バージョン ](https://github.com/yujianke100/HBR-AutoBeat/releases/download/v1.0/HBR-AutoBeat.exe)

スクリプトを起動する前に、ゲームを「ライブ開始」画面まで進めてからスクリプトを起動してください。スクリプトは自動的にゲームに切り替え、スタートボタンを押すだけで始まります。終了したら、ゲームを最小化するか、他のウィンドウに切り替えるとスクリプトは自動的に終了します。
