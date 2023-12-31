# Detector Training

## Prepare dataset
- place cvat annotations in yolo format into [./detector_training/datasets/construction_analytics/cvat](./detector_training/datasets/construction_analytics/cvat)
- place videos into [./detector_training/datasets/construction_analytics/videos](./detector_training/datasets/construction_analytics/videos) with the same namings
- run preparation script
    ```bash
    python prepare_data.py
    ```

The final dataset structure should look like this: 
```text
├── construction_analytics.yaml
└── construction_analytics/
    ├── cvat/                  
    │   ├── output118.zip
    │   ├── ...
    │
    ├── videos/
    │   ├── output118.mp4
    │   ├── ...
    │
    └── yolo/
        ├── images/
        │   ├── full/
        │   ├── train/
        │   └── val/
        │
        └── labels/
            ├── full/
            ├── train/
            └── val/
```

## Train yolo model
```bash
python train_yolov8.py
```