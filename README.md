# 🧠 Autism Detection Web Application

A Flask web app for autism detection using image uploads with support for both traditional ML models and YOLOv9 object detection.

## 🧰 Features
- User authentication with SQLite
- Predict autism using `autism_model.pkl`
- Object detection using `YOLOv9` and `best.pt`
- Upload and analyze images via a browser

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Add Models
Place the following in the `models/` folder:
- `autism_model.pkl`
- `best.pt`

### 3. Run the App
```bash
python index.py
```

Then visit: `http://127.0.0.1:5000/`

## 📁 Folder Structure
```
autism_detection_app/
├── index.py
├── requirements.txt
├── README.md
├── models/
│   ├── autism_model.pkl
│   └── best.pt
├── static/
└── templates/
```
