from abc import abstractmethod, ABC
from typing import List, Optional
from dataclasses import dataclass

import numpy as np

from infrastructure.interface import DetectionModel, DetectionData
from infrastructure.interface import ClassificationModel, Action


@dataclass
class FrameData:
    detections: List[DetectionData]
    actions: List[Action]


@dataclass
class FrameDataList:
    data: List[FrameData]


class BaseService(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    def process_frame(self, frame: np.ndarray) -> List[FrameData]:
        raise NotImplementedError()

    def process_video(self, video_src: str) -> FrameDataList:
        raise NotImplementedError()

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
        classes_data: List[Action] = None,
    ):
        if not classes_data:
            classes_data = [Action("None", "0", 1.0)] * len(detections_data)
        frame_data = FrameData(detections_data, classes_data)
        return frame_data
