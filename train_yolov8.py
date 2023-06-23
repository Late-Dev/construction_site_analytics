from pathlib import Path
from ultralytics import YOLO

# Load a model
model = YOLO('yolov8s.pt')

# Train the model with 2 GPUs
data_path = (Path(__file__).parent / './datasets/construction_analytics.yaml').resolve()
model.train(data=data_path, epochs=10, imgsz=640, device=[0])
