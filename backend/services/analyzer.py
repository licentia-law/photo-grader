import cv2
import numpy as np


def analyze_image(image: np.ndarray) -> dict:
    brightness = _brightness(image)
    warm, cool = _color_temp(image)
    saturation = _saturation(image)
    histogram = _histogram(image)
    mood = _mood(brightness, warm, saturation)

    return {
        "brightness": round(brightness, 2),
        "color_temp": {"warm": round(warm, 2), "cool": round(cool, 2)},
        "saturation": round(saturation, 2),
        "mood": mood,
        "histogram": histogram,
    }


def _brightness(image: np.ndarray) -> float:
    lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    return float(lab[:, :, 0].mean() / 255 * 100)


def _color_temp(image: np.ndarray) -> tuple[float, float]:
    r_mean = float(image[:, :, 0].mean())
    b_mean = float(image[:, :, 2].mean())
    total = r_mean + b_mean
    if total == 0:
        return 50.0, 50.0
    warm = r_mean / total * 100
    cool = b_mean / total * 100
    return warm, cool


def _saturation(image: np.ndarray) -> float:
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    return float(hsv[:, :, 1].mean() / 255 * 100)


def _histogram(image: np.ndarray) -> dict:
    result = {}
    for i, ch in enumerate(["r", "g", "b"]):
        hist, _ = np.histogram(image[:, :, i], bins=256, range=(0, 256))
        result[ch] = hist.tolist()
    return result


def _mood(brightness: float, warm: float, saturation: float) -> str:
    is_bright = brightness >= 60
    is_mid = 35 <= brightness < 60
    is_dark = brightness < 35
    is_warm = warm >= 55
    is_cool = warm < 45
    is_vivid = saturation >= 55
    is_mid_sat = 30 <= saturation < 55
    is_muted = saturation < 30

    if is_bright and is_warm and is_vivid:
        return "☀️ 따뜻한 골든아워"
    if is_dark and is_cool and is_muted:
        return "🌙 다크 무드"
    if (is_mid or is_dark) and is_cool and is_muted:
        return "🌫️ 차가운 필름"
    if is_bright and is_cool and is_vivid:
        return "💎 선명한 블루톤"
    if is_mid and is_warm and (is_muted or is_mid_sat):
        return "🍂 빈티지 필름"
    if is_dark and is_warm and is_mid_sat:
        return "🕯️ 따뜻한 저조도"
    return "🎨 자연스러운 색감"
