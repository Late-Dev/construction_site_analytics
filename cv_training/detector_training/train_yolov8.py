from pathlib import Path
from ultralytics import YOLO

# Load a model
model = YOLO('yolov8m.pt')

# Train the model with 2 GPUs
data_path = (Path(__file__).parent / './datasets/construction_analytics.yaml').resolve()
model.train(
    data=data_path,
    epochs=5, 
    imgsz=640, 
    device=[0],
    cache=True,
    label_smoothing=0.1,
)
