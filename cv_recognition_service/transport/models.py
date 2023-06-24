from typing import List

from pydantic import BaseModel


class Action(BaseModel):
    class_name: str
    class_id: str
    score: float


class ClassificationData(BaseModel):
    actions: List[Action]


class DetectionData(BaseModel):
    xyxy: List[int]
    score: float
    class_name: str
    tracking_id: int
    activity: int


class FrameData(BaseModel):
    detections: List[DetectionData]
    actions: List[ClassificationData]


class FrameDataList(BaseModel):
    data: List[FrameData]
