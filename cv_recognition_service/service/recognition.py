from typing import List
import numpy as np

from infrastructure.interface import DetectionModel
from infrastructure.interface import ClassificationModel
from service.interface import BaseService, FrameDataList


class RecognitionService(BaseService):
    def __init__(self, detection_model: DetectionModel):
        self.detection_model = detection_model

    def process_video(self, video_src: str) -> FrameDataList:
        detections_data = self.detection_model.detect(video_src)
        frame_data_list = [self._serialize_frame_data(d) for d in detections_data]
        return FrameDataList(data=frame_data_list)
