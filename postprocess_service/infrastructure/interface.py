from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import List

import numpy as np


@dataclass
class Action:
    class_name: str
    class_id: str
    score: float


@dataclass
class ClassificationData:
    actions: List[Action]


class ClassificationModel(ABC):
    @abstractmethod
    def _load_model(self, model_path: str):
        """
        Load model from local file
        """
        pass

    @abstractmethod
    def _image_preprocessing(self, image: np.ndarray):
        """
        Preprocess input images
        """

    @abstractmethod
    def predict(self, image: np.ndarray) -> ClassificationData:
        """
        Predict action of detected vehicle
        """
        pass


@dataclass
class DetectionData:
    xyxy: List[int]
    score: float
    class_name: str = "truck"
    tracking_id: int = None
    activity: int = 0

    def __post_init__(self):
        self.x_min, self.y_min, self.x_max, self.y_max = self.xyxy
        self.width = self.x_max - self.x_min
        self.height = self.y_max - self.y_min
        self.xywh = (self.x_min, self.y_min, self.width, self.height)


class DetectionModel:
    @abstractmethod
    def _load_model(self, model_path: str):
        """
        Load model from local file
        """
        pass

    @abstractmethod
    def _image_preprocessing(self, image: np.ndarray):
        """
        Preprocess input images
        """

    @abstractmethod
    def detect(self, image: np.ndarray) -> List[DetectionData]:
        """
        Get detections from the image
        """
        pass
