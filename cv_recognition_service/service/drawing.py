import os
import math
from typing import List

import cv2
import numpy as np
from tqdm import trange

from service.interface import BaseService, FrameData


class DrawingService(BaseService):
    def __init__(self) -> None:
        super().__init__()
        self.color_map = {
            "truck": np.array([178, 255, 54]),
            "tractor": np.array([244, 183, 64]),
            "crane": np.array([106, 150, 255]),
            "digger": np.array([220, 140, 236]),
            "no_action": np.array([220, 140, 236]),
        }

    def process_video(self, video_filepath: str, frame_data_list: List[FrameData]):
        capture = cv2.VideoCapture(video_filepath)
        length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))

        fps = 10
        fourcc = cv2.VideoWriter_fourcc(*"h264")
        out_path = f"output/{os.path.basename(video_filepath)}"
        writer = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

        for frame_num in trange(length):
            _, frame = capture.read()
            if frame is None:
                break
            new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_data = frame_data_list[frame_num]

            plotted_frame = self.draw(new_frame, frame_data)
            plotted_frame = cv2.cvtColor(plotted_frame, cv2.COLOR_RGB2BGR)
            writer.write(plotted_frame)

        writer.release()
        capture.release()

    def draw(
        self,
        frame: np.ndarray,
        frame_data: FrameData,
        font=cv2.FONT_HERSHEY_SIMPLEX,
        font_scale=1,
        line_thickness=3,
    ):
        detections = frame_data.detections
        vehicle_actions = frame_data.actions

        for detection, actions in zip(detections, vehicle_actions):
            # draw object bbox
            rect_color = tuple(
                self.color_map[detection.class_name].tolist()
                + [min(1, math.ceil(detection.score * 10) / 10 * 2)]
            )
            cv2.rectangle(
                frame,
                (detection.x_min, detection.y_min),
                (detection.x_max, detection.y_max),
                rect_color,
                line_thickness,
            )

            # draw naming bbox and write tracking_id
            rect_len = 50 if detection.tracking_id < 10 else 75
            cv2.rectangle(
                frame,
                (detection.x_min, detection.y_min - 25),
                (detection.x_min + rect_len, detection.y_min),
                rect_color,
                -1,
            )
            cv2.putText(
                frame,
                f"#{detection.tracking_id}: {detection.class_name}",
                (detection.x_min, detection.y_min),
                font,
                font_scale,
                (0, 0, 0),
                2,
                cv2.FILLED,
            )

        return frame
