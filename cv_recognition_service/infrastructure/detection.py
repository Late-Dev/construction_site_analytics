from typing import List

import numpy as np
import cv2
from ultralytics import YOLO

from infrastructure.interface import (
    DetectionModel,
    DetectionData,
)


class DummyDetector(DetectionModel):
    def __init__(self, model_path: str, conf_thresh: float) -> None:
        self.conf_thresh = conf_thresh
        self.model = self._load_model(model_path)

    def _load_model(self, model_path: str):
        def empty(image: np.ndarray):
            return [(274, 233, 300, 330, 0.98), (333, 201, 433, 320, 0.98)]

        return empty

    def _image_preprocessing(self, image: np.ndarray) -> np.ndarray:
        return cv2.resize(image, (600, 600))

    def detect(self, image: np.ndarray) -> List[DetectionData]:
        preprocessed_image = self._image_preprocessing(image)
        raw_predictions = self.model(preprocessed_image)
        predictions = self._raw_to_data(raw_predictions)
        return predictions

    def _raw_to_data(self, raw_predictions: list) -> List[DetectionData]:
        data_list = []
        for pred in raw_predictions:
            x_min = pred[0]
            y_min = pred[1]
            x_max = pred[2]
            y_max = pred[3]
            score = pred[4]
            class_name = "truck"
            if score > self.conf_thresh:
                data_model = DetectionData(
                    x_min,
                    y_min,
                    x_max,
                    y_max,
                    score,
                    class_name=class_name,
                    tracking_id=0,
                )
                data_list.append(data_model)
        return data_list


class YOLODetector(DetectionModel):
    def __init__(self, model_path: str, conf_thresh: float, device: str) -> None:
        self.conf_thresh = conf_thresh
        self.model = self._load_model(model_path)
        self.cls2name = {
            0: "digger",
            1: "tractor",
            2: "truck",
            3: "crane",
        }

    def _load_model(self, model_path: str, device: str):
        model = YOLO(model_path)
        model.to(device)
        return model

    def detect(self, video_path: str) -> List[List[DetectionData]]:
        raw_preds = self.model.track(video_path, stream=True)

        predictions = []
        for p in raw_preds:
            boxes = p.boxes.cpu().numpy()
            predictions.append(
                [
                    DetectionData(coords.tolist(), score, self.cls2name[cls], track_id)
                    for coords, cls, score, track_id in zip(
                        boxes.xyxy.astype(int), boxes.cls, boxes.conf, boxes.id
                    )
                ]
            )
        return predictions
