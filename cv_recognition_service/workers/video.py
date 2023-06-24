import os

import cv2
import numpy as np

from building import build_recognition_service


service = build_recognition_service()


def process_video(video_path: str):
    frame_data_list = service.process_video(video_path)
    return frame_data_list
