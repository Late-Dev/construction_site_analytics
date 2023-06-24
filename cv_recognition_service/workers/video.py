import os

import cv2
import numpy as np

from building import build_recognition_service

color_map = {
    "digger": np.array([178, 255, 54]),
    "tractor": np.array([244, 183, 64]),
    "truck": np.array([106, 150, 255]),
    "crane": np.array([220, 140, 236]),
}

service = build_recognition_service()


def process_video(video_path: str):
    frame_data_list = service.process_video(video_path)

    capture = cv2.VideoCapture(video_path)
    length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)) + int(
        capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    )
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fps = 10
    fourcc = cv2.VideoWriter_fourcc(*"h264")
    out_path = f"output/{os.path.basename(video_path)}"
    writer = cv2.VideoWriter(out_path, fourcc, fps, (width, height))
    line_data = {}
    bar_data = {}
    # has_frame = True

    for frame_num in range(length):
        has_frame, frame = capture.read()
        if frame is None:
            break
        new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_data = frame_data_list.detections[frame_num]

        # TODO: drawing logic
        plotted_frame = service.draw(new_frame, frame_data)
        plotted_frame = cv2.cvtColor(plotted_frame, cv2.COLOR_RGB2BGR)
        writer.write(plotted_frame)

    writer.release()
    capture.release()
    return out_path, frame_data_list, bar_data, line_data


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
