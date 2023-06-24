from abc import abstractmethod, ABC
from typing import List, Optional
from dataclasses import dataclass

import numpy as np

from infrastructure.interface import DetectionModel, DetectionData
from infrastructure.interface import ClassificationModel, ClassificationData


@dataclass
class FrameData:
    detections: List[DetectionData]
    actions: List[ClassificationData]


class BaseService(ABC):
    @abstractmethod
    def __init__(
        self, detection_model: DetectionModel, classification_model: ClassificationModel
    ) -> None:
        self.detection_model = detection_model
        self.classification_model = classification_model

    @abstractmethod
    def process_frame(self, frame: np.ndarray) -> List[FrameData]:
        pass

    @abstractmethod
    def process_video(self, video_src: str) -> List[FrameData]:
        pass

    @staticmethod
    def _crop_images(image: np.ndarray, det_predictions: List[DetectionData]):
        cropped_images = []
        for det_data in det_predictions:
            cropped = image[
                det_data.y_min : det_data.y_max, det_data.x_min : det_data.x_max
            ]
            cropped_images.append(cropped)
        return cropped_images

    @staticmethod
    def _serialize_frame_data(
        detections_data: List[DetectionData],
        classes_data: Optional[ClassificationData] = None,
    ):
        detections = []
        pred_classes = []
        for det, cls_data in zip(detections_data, classes_data):
            detections.append(det)
            pred_classes.append(cls_data)
        frame_data = FrameData(detections, pred_classes)
        return frame_data
