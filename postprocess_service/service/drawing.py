import os
import subprocess
import math
from typing import List

import cv2
import numpy as np
from tqdm import trange

from transport.models import FrameData, FrameDataList


class DrawingService:
    def __init__(self) -> None:
        super().__init__()
        self.color_map = {
            "truck": np.array([178, 255, 54]),
            "tractor": np.array([244, 183, 64]),
            "crane": np.array([106, 150, 255]),
            "digger": np.array([220, 140, 236]),
            "no_action": np.array([220, 140, 236]),
        }

    def process_video(self, video_filepath: str, frame_data_list: FrameDataList):
        capture = cv2.VideoCapture(video_filepath)
        length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))

        fps = int(capture.get(cv2.CAP_PROP_FPS))
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        raw_out_path = f"output/raw_{os.path.basename(video_filepath)}"
        out_path = f"output/{os.path.basename(video_filepath)}"

        writer = cv2.VideoWriter(raw_out_path, fourcc, fps, (width, height))

        for frame_num in trange(length):
            _, frame = capture.read()
            if frame is None:
                break
            new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_data = frame_data_list.data[frame_num]

            plotted_frame = self.process_frame(new_frame, frame_data)
            plotted_frame = cv2.cvtColor(plotted_frame, cv2.COLOR_RGB2BGR)
            writer.write(plotted_frame)

        writer.release()
        capture.release()

        subprocess.run(["ffmpeg", "-i", raw_out_path, "-c:v", "libx265", out_path])
        return out_path

    def process_frame(
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
                (detection.xyxy[0], detection.xyxy[1]),
                (detection.xyxy[2], detection.xyxy[3]),
                rect_color,
                line_thickness,
            )

            # draw naming bbox and write tracking_id
            naming = f"#{detection.tracking_id}: {detection.class_name}"
            rect_len = 200
            cv2.rectangle(
                frame,
                (detection.xyxy[0], detection.xyxy[1] - 25),
                (detection.xyxy[0] + rect_len, detection.xyxy[1]),
                rect_color,
                -1,
            )
            cv2.putText(
                frame,
                naming,
                (detection.xyxy[0], detection.xyxy[1]),
                font,
                font_scale,
                (0, 0, 0),
                2,
                cv2.FILLED,
            )

        return frame
