# VisionAI - Image Recognition System

A web application that identifies objects in uploaded images using a pre-trained MobileNet deep learning model.

## Technologies

- **Python** — Core programming language
- **ONNX Runtime** — Lightweight inference engine for MobileNet model
- **OpenCV** — Image preprocessing
- **Flask** — Web application framework

## Features

- Drag-and-drop or click-to-upload image input
- Real-time object classification using MobileNet (ImageNet)
- Top-5 predictions with confidence scores
- Responsive, modern dark-themed UI
- Automatic cleanup of uploaded files

## Setup

```bash
# Clone the repository
git clone https://github.com/tarsariyasahil/Image-Recognition-System.git
cd Image-Recognition-System

# Create a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Open your browser and navigate to `http://localhost:5000`

## How It Works

1. **Upload** — User uploads an image via the web interface
2. **Preprocess** — OpenCV resizes the image to 224×224 and normalizes pixel values
3. **Predict** — MobileNet classifies the image against 1,000 ImageNet categories
4. **Display** — Top-5 predictions with confidence percentages are shown

## Project Structure

```
├── app.py                  # Flask application entry point
├── requirements.txt        # Python dependencies
├── README.md
├── model/                  # Auto-downloaded ONNX model & labels
├── static/
│   ├── css/
│   │   └── style.css       # Application styles
│   ├── js/
│   │   └── app.js          # Client-side logic
│   └── uploads/            # Temporary upload storage
├── templates/
│   └── index.html          # Main HTML template
└── utils/
    ├── __init__.py
    ├── preprocessing.py    # Image preprocessing with OpenCV
    └── predictor.py        # MobileNet ONNX model wrapper
```

## Author

**Tarsariya Sahil Devshibhai** (Sahil_1*)

- Email: sahiltarsariya1@gmail.com
- GitHub: [tarsariyasahil](https://github.com/tarsariyasahil)

## License

This project was built as part of a Python Developer Internship.
