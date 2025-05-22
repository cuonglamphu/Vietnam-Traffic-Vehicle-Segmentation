from ultralytics import YOLO
from typing import Optional

class YOLOModel:
    _instance = None  # Singleton pattern
    model_name = 'pretrained_models/traffic_detect_model.pt'
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(YOLOModel, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'model'):
            try:
                self.model = YOLO(self.model_name)
            except Exception as e:
                raise Exception(f"Error loading YOLO model: {e}")

    def predict(self, frame):
        return self.model(frame) 