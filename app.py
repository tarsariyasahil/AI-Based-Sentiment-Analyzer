import os
import uuid
import time

from flask import Flask, render_template, request, jsonify
from utils.preprocessing import preprocess_image
from utils.predictor import predict

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "static", "uploads")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp", "webp"}

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def cleanup_old_uploads(max_age_seconds=3600):
    """Remove uploaded files older than max_age_seconds."""
    folder = app.config["UPLOAD_FOLDER"]
    now = time.time()
    for fname in os.listdir(folder):
        fpath = os.path.join(folder, fname)
        if os.path.isfile(fpath) and (now - os.path.getmtime(fpath)) > max_age_seconds:
            try:
                os.remove(fpath)
            except OSError:
                pass


@app.route("/")
def index():
    cleanup_old_uploads()
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict_route():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Allowed: png, jpg, jpeg, bmp, webp"}), 400

    ext = file.filename.rsplit(".", 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)

    try:
        file.save(filepath)
        img_array = preprocess_image(filepath)
        results = predict(img_array, top_k=5)
        image_url = f"/static/uploads/{unique_name}"
        return jsonify({"success": True, "image_url": image_url, "predictions": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except OSError:
                pass


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
