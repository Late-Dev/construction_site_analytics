from typing import List, Tuple
from collections import defaultdict, deque

import cv2
import numpy as np
from tqdm.auto import tqdm

from infrastructure.interface import (
    DetectionModel,
)
from transport.models import FrameData


class ActivityDetector(DetectionModel):
    def __init__(self) -> None:
        self.win_size = 30
        self.mv_threshold = 10
        self.act_threshold = 0.15

    @staticmethod
    def has_moved(track_coords: List[Tuple[int, int]], threshold: int):
        center1 = track_coords[0]
        center2 = track_coords[-1]
        return (
            abs(center1[0] - center2[0]) > threshold
            or abs(center1[1] - center2[1]) > threshold
        )

    @staticmethod
    def has_action(frames: List[np.ndarray], threshold: float):
        start, end = frames[0], frames[-1]
        start, end = cv2.resize(start, (100, 100)), cv2.resize(end, (100, 100))
        diff = np.abs(start - end).sum()

        diff = start.copy()
        cv2.absdiff(start, end, diff)
        diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        for i in range(0, 3):
            dilated = cv2.dilate(diff.copy(), None, iterations=i + 1)
        _, thresh = cv2.threshold(dilated, 3, 255, cv2.THRESH_BINARY)

        # процент отличающихся пикселей
        diff = 1 - (thresh.sum() / 255) / np.prod(thresh.shape)
        return diff >= threshold

    def predict_action(self, track_data: List[deque], class_name: str):
        track_frames = track_data[0]
        track_coords = track_data[1]
        has_moved = self.has_moved(track_coords, self.mv_threshold)
        has_action = self.has_action(track_frames, self.act_threshold)
        if class_name == "crane":
            h, w, _ = track_frames[-1].shape
            is_active = h > w or has_moved
        elif class_name in ("truck", "tractor", "digger"):
            is_active = has_moved or has_action
        else:
            is_active = has_action
        return int(is_active)

    def detect(self, video_path: str, frame_data_list: List[FrameData]):
        track_data = defaultdict(
            lambda: [deque(maxlen=self.win_size), deque(maxlen=self.win_size)]
        )
        cap = cv2.VideoCapture(video_path)

        for frame_data in tqdm(
            frame_data_list, desc="Detecting activity"
        ):  # цикл по кадрам видоса
            _, frame = cap.read()
            for det in frame_data.detections:  # цикл по задетекченным объектам
                track_id = det.tracking_id
                track_data[track_id][0].append(
                    frame[det.y_min : det.y_max, det.x_min : det.x_max]
                )
                track_data[track_id][1].append((det.x_center, det.y_center))

                det.activity = 1
                if len(track_data[track_id][0]) == self.win_size:
                    det.activity = self.predict_action(
                        track_data[track_id], det.class_name
                    )

        cap.release()

        return frame_data_list
