# Game State Detector 使用文档

## 功能说明

`game_state_detector.py` 提供了三个核心函数用于检测 Heaven Burns Red 游戏界面状态。

## API 说明

### 1. `init()` - 初始化OCR

在使用检测功能前必须先调用此函数初始化OCR模块。

```python
from game_state_detector import init

success = init()
if success:
    print("OCR初始化成功")
```

**返回值**: `bool` - 初始化是否成功

**注意**: 
- 首次调用会下载OCR模型（约200MB），需要网络连接
- 初始化过程需要3-5秒
- 重复调用会直接返回，不会重新初始化

---

### 2. `detect(game_left, game_top)` - 检测游戏状态

截取游戏画面指定区域并识别当前界面类型。

```python
from game_state_detector import detect

# 假设游戏窗口左上角坐标为 (100, 50)
state = detect(game_left=100, game_top=50)
print(f"当前界面: {state}")
```

**参数**:
- `game_left` (int): 游戏窗口左上角的X坐标（屏幕绝对坐标）
- `game_top` (int): 游戏窗口左上角的Y坐标（屏幕绝对坐标）

**返回值**: `str` - 界面类型，可能的值：
- `"successful"`: 游戏成功结算界面
- `"ready"`: 准备界面（选择队伍）
- `"select"`: 选曲界面
- `"live"`: 游戏中/默认状态
- `"unreadable"`: 截图失败或无法识别

**检测区域**:
- 相对坐标: `(1300, 765, 1470, 825)` （相对于游戏窗口左上角）
- 检测右下角区域的文字特征

---

### 3. `close()` - 关闭OCR

释放OCR资源，程序结束前应调用。

```python
from game_state_detector import close

close()
print("OCR已关闭")
```

**注意**: 关闭后需要重新调用 `init()` 才能继续使用检测功能

---

## 完整示例

```python
from game_state_detector import init, detect, close
import time

# 1. 初始化OCR
if not init():
    print("OCR初始化失败")
    exit(1)

# 2. 循环检测游戏状态
game_left = 100  # 从 window_helpers 获取
game_top = 50

for i in range(10):
    state = detect(game_left, game_top)
    print(f"检测 {i+1}: {state}")
    time.sleep(1)

# 3. 关闭OCR
close()
```

---

## 关键字规则

当前识别规则（可在 `game_state_detector.py` 中修改）：

| 界面类型 | 关键字 | 优先级 |
|---------|-------|--------|
| successful | COMBO | 高 |
| ready | 總戰鬥力 | 中 |
| select | Lv | 低 |

**匹配逻辑**:
1. 按优先级从高到低匹配
2. 找到第一个匹配的关键字即返回
3. 若无匹配则返回 `"live"`

---

## 性能优化建议

1. **只初始化一次**: 在程序启动时调用 `init()`，不要重复初始化
2. **避免频繁检测**: 建议每0.5-1秒检测一次，避免过高CPU占用
3. **检测前确认窗口坐标**: 确保传入的 `game_left` 和 `game_top` 是准确的游戏窗口坐标

---

## 故障排查

### 问题1: `unreadable` 返回过多
- 检查游戏窗口坐标是否正确
- 确认游戏分辨率是否为1920x1080
- 检查截图区域是否被其他窗口遮挡

### 问题2: 初始化失败
- 检查网络连接（首次需下载模型）
- 确认Python环境中已安装 `paddleocr`、`opencv-python`、`Pillow`

### 问题3: 识别错误率高
- 调整关键字规则（修改 `GAME_STATES`）
- 调整截图区域（修改 `CROP_REGION`）
- 增加更多关键字以提高准确率

---

## 扩展识别规则

如需添加新的界面类型，修改 `GAME_STATES`:

```python
GAME_STATES = [
    ("successful", ["COMBO"]),
    ("failed", ["演唱會失敗", "重來"]),  # 新增失败界面
    ("ready", ["總戰鬥力"]),
    ("select", ["Lv"]),
]
```

**注意**: 优先级从上到下递减，越靠前的规则优先匹配。
