"""
Game State Detector Module
用于识别 Heaven Burns Red 游戏界面状态

Usage:
    from game_state_detector import init, detect, close

    # 初始化OCR
    init()

    # 检测游戏状态（传入游戏窗口左上角坐标）
    state = detect(game_left=100, game_top=50)
    print(f"Current state: {state}")

    # 关闭OCR
    close()
"""

import os

import cv2
import numpy as np
from paddleocr import PaddleOCR
from PIL import ImageGrab

# 全局OCR实例
_ocr_instance = None

# 关键字规则（优先级从高到低）
GAME_STATES = [
    ("successful", ["COMBO"]),  # 游戏结算成功界面
    ("ready", ["總戰鬥力"]),  # 准备界面
    ("select", ["Lv"]),  # 选曲界面
]

# 截图区域（相对于游戏窗口左上角的坐标）
# 格式：(x1, y1, x2, y2)
CROP_REGION = (1300, 765, 1470, 825)


def init():
    """
    初始化OCR模块，加载模型并保持等待状态

    Returns:
        bool: 初始化是否成功
    """
    global _ocr_instance

    if _ocr_instance is not None:
        print("OCR already initialized.")
        return True

    try:
        # 设置环境变量以跳过模型连接检查（可选）
        os.environ["DISABLE_MODEL_SOURCE_CHECK"] = "True"

        print("Initializing OCR...")
        _ocr_instance = PaddleOCR(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
        )
        print("OCR initialized successfully.")
        return True
    except Exception as e:
        print(f"Failed to initialize OCR: {e}")
        _ocr_instance = None
        return False


def close():
    """
    关闭OCR模块，释放资源
    """
    global _ocr_instance

    if _ocr_instance is None:
        print("OCR not initialized.")
        return

    try:
        # PaddleOCR 没有显式的close方法，设置为None让GC回收
        _ocr_instance = None
        print("OCR closed.")
    except Exception as e:
        print(f"Error closing OCR: {e}")


def detect(game_left, game_top):
    """
    截取游戏画面并检测当前界面状态

    Args:
        game_left (int): 游戏窗口左上角的X坐标
        game_top (int): 游戏窗口左上角的Y坐标

    Returns:
        str: 界面类型，可能的值：
            - "successful": 游戏成功结算界面
            - "ready": 准备界面
            - "select": 选曲界面
            - "live": 默认/游戏中
            - "unreadable": 截图失败或无法识别
    """
    global _ocr_instance

    if _ocr_instance is None:
        print("OCR not initialized. Please call init() first.")
        return "unreadable"

    try:
        # 计算绝对坐标
        x1 = game_left + CROP_REGION[0]
        y1 = game_top + CROP_REGION[1]
        x2 = game_left + CROP_REGION[2]
        y2 = game_top + CROP_REGION[3]

        # 截取屏幕指定区域
        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        if img is None or img.size == 0:
            return "unreadable"

        # OCR识别
        result = _ocr_instance.predict(img)

        # 提取文本
        if not result or len(result) == 0:
            return "unreadable"

        text_all = result[0].json.get("res", {}).get("rec_texts", [])

        if not text_all:
            return "live"  # 没有识别到文本，默认为游戏中

        # 合并所有识别文本
        text_combined = "".join(text_all)

        # 按优先级匹配关键字
        for state, keywords in GAME_STATES:
            if any(keyword in text_combined for keyword in keywords):
                return state

        # 默认返回游戏中
        return "live"

    except Exception as e:
        print(f"Error during detection: {e}")
        return "unreadable"


def detect_from_file(img_path):
    """
    从文件检测界面状态（用于测试）

    Args:
        img_path (str): 图片文件路径

    Returns:
        str: 界面类型
    """
    global _ocr_instance

    if _ocr_instance is None:
        print("OCR not initialized. Please call init() first.")
        return "unreadable"

    try:
        img = cv2.imread(img_path)
        if img is None:
            return "unreadable"

        h, w = img.shape[:2]

        # 裁剪指定区域
        crop = img[CROP_REGION[1] : CROP_REGION[3], CROP_REGION[0] : CROP_REGION[2]]

        if crop.size == 0:
            return "unreadable"

        # OCR识别
        result = _ocr_instance.predict(crop)

        # 提取文本
        if not result or len(result) == 0:
            return "unreadable"

        text_all = result[0].json.get("res", {}).get("rec_texts", [])

        if not text_all:
            return "live"

        # 合并所有识别文本
        text_combined = "".join(text_all)

        # 按优先级匹配关键字
        for state, keywords in GAME_STATES:
            if any(keyword in text_combined for keyword in keywords):
                return state

        return "live"

    except Exception as e:
        print(f"Error during detection: {e}")
        return "unreadable"


# 测试代码
if __name__ == "__main__":
    # 初始化
    if not init():
        exit(1)

    # 测试从文件识别
    img_dir = os.path.join(os.path.dirname(__file__), "screenshot")
    if os.path.exists(img_dir):
        img_files = [
            f
            for f in os.listdir(img_dir)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]

        print("\nTesting detection from files:")
        for img in sorted(img_files):
            img_path = os.path.join(img_dir, img)
            state = detect_from_file(img_path)
            print(f"  {img}: {state}")

    # 关闭
    close()
