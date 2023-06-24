from pathlib import Path
from ultralytics import YOLO

# Load a model
model = YOLO('runs/detect/train_yolov8m/weights/best.pt')

# Train the model with 2 GPUs
data_path = (Path(__file__).parent / './datasets/construction_analytics.yaml').resolve()
model.predict("datasets/construction_analytics/videos/output012.mp4", save=True, imgsz=640, conf=0.5, device=[0])
