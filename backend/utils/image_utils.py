import io
import numpy as np
from PIL import Image

MAX_SIZE = 2048


def bytes_to_array(image_bytes: bytes) -> np.ndarray:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    w, h = image.size
    if max(w, h) > MAX_SIZE:
        ratio = MAX_SIZE / max(w, h)
        image = image.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)
    return np.array(image)


def array_to_bytes(array: np.ndarray, format: str = "JPEG") -> bytes:
    image = Image.fromarray(array.astype(np.uint8))
    buf = io.BytesIO()
    image.save(buf, format=format, quality=92)
    return buf.getvalue()
