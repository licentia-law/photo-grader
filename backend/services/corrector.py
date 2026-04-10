import numpy as np
from skimage.exposure import match_histograms


def correct_image(image_b: np.ndarray, image_a: np.ndarray, strength: float = 0.75) -> np.ndarray:
    strength = max(0.0, min(1.0, strength))
    matched = match_histograms(image_b, image_a, channel_axis=-1)
    result = matched * strength + image_b * (1 - strength)
    return result.astype(np.uint8)
