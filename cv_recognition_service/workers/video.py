import os

import cv2
import numpy as np

from building import build_recognition_service, build_drawing_service

color_map = {
    "digger": np.array([178, 255, 54]),
    "tractor": np.array([244, 183, 64]),
    "truck": np.array([106, 150, 255]),
    "crane": np.array([220, 140, 236]),
}

service = build_recognition_service()
drawing_service = build_drawing_service()


def process_video(video_path: str):
    frame_data_list = service.process_video(video_path)
    out_path = drawing_service.process_video(video_path, frame_data_list)
    return out_path


def create_preview_image(video_path: str):
    capture = cv2.VideoCapture(video_path)
    length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    imagename = f"{str(os.path.basename(video_path)).split('.')[-2]}.jpg"
    out_path = f"output/{imagename}"
    for _ in range(15):
        if _ == 14:
            ret, frame = capture.read()
            if frame is None:
                break
            new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            plotted_frame = service.process_frame(new_frame)
            cv2.imwrite(out_path, cv2.cvtColor(plotted_frame, cv2.COLOR_BGR2RGB))
            return out_path
