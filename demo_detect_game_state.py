import os

import cv2
from paddleocr import PaddleOCR

# 关键字规则
GAME_STATES = [
    ("successful", ["COMBO"]),
    ("ready", ["總戰鬥力"]),
    ("select", ["Lv"]),
]


def crop_regions(img):
    h, w = img.shape[:2]
    crops = []
    crops.append(img[765:825, 1300:1470])  # 左上
    return crops


def detect_state(img_path, ocr):
    img = cv2.imread(img_path)
    if img is None:
        return "unreadable"
    text_all = []
    for crop in crop_regions(img):
        # 显示裁剪区域用于调试
        try:
            result = ocr.predict(crop)
            recs = result[0].json.get("res", {}).get("rec_texts", [])
            if recs:
                text_all.extend(recs)
        except Exception:
            # 忽略单个区域识别错误，继续其他区域
            continue

    if not text_all:
        return "unreadable"

    text_all = "".join(text_all)
    for state, keywords in GAME_STATES:
        if any(k in text_all for k in keywords):
            return state
    return "live"  # 默认


def main():
    ocr = PaddleOCR(
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
    )
    img_dir = os.path.join(os.path.dirname(__file__), "screenshot")
    img_files = [
        f for f in os.listdir(img_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]
    print(img_files)
    for img in img_files:
        state = detect_state(os.path.join(img_dir, img), ocr)
        print(f"{img}: {state}")


if __name__ == "__main__":
    main()
