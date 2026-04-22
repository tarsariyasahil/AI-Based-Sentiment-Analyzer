import os
import json
import urllib.request

import onnxruntime as ort
import numpy as np

_MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model")
_MODEL_PATH = os.path.join(_MODEL_DIR, "mobilenetv2.onnx")
_LABELS_PATH = os.path.join(_MODEL_DIR, "imagenet_labels.json")

_MODEL_URL = "https://github.com/onnx/models/raw/main/validated/vision/classification/mobilenet/model/mobilenetv2-7.onnx"
_LABELS_URL = "https://raw.githubusercontent.com/onnx/models/main/validated/vision/classification/mobilenet/labels/imagenet_simple_labels.json"

_session = None
_labels = None


def _download(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if not os.path.exists(dest):
        urllib.request.urlretrieve(url, dest)


def _load_session():
    global _session, _labels
    if _session is None:
        _download(_MODEL_URL, _MODEL_PATH)
        _download(_LABELS_URL, _LABELS_PATH)
        _session = ort.InferenceSession(_MODEL_PATH, providers=["CPUExecutionProvider"])
        with open(_LABELS_PATH, "r", encoding="utf-8") as f:
            _labels = json.load(f)
    return _session


def predict(image_array, top_k=5):
    """Run MobileNet V2 prediction on a preprocessed image array.

    Returns a list of dicts with 'label', 'description', 'confidence'.
    """
    session = _load_session()
    input_name = session.get_inputs()[0].name
    output = session.run(None, {input_name: image_array})[0][0]
    top_indices = np.argsort(output)[::-1][:top_k]
    results = []
    for idx in top_indices:
        label = _labels[idx] if _labels and idx < len(_labels) else str(idx)
        conf = float(output[idx])
        results.append(
            {"label": str(idx), "description": label.replace("_", " ").title(), "confidence": round(conf * 100, 2)}
        )
    return results
