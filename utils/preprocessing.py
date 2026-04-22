import cv2
import numpy as np

_MEAN = np.array([0.485, 0.456, 0.406], dtype="float32")
_STD = np.array([0.229, 0.224, 0.225], dtype="float32")


def preprocess_image(image_path, target_size=(224, 224)):
    """Read, resize and normalize an image for MobileNetV2 ONNX prediction."""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image from {image_path}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)
    img_array = img.astype("float32") / 255.0
    img_array = (img_array - _MEAN) / _STD
    img_array = np.transpose(img_array, (2, 0, 1))
    img_array = np.expand_dims(img_array, axis=0)
    return img_array
