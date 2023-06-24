import os
from typing import List

import cv2
import numpy as np

from service.drawing import DrawingService


drawing_service = DrawingService()


def process_video(frame_data_list: List, video_path: str):
    out_path = drawing_service.process_video(video_path, frame_data_list)
    return out_path
