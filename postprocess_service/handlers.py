import os
import datetime

import cv2

from transport.database import StatusEnum, update_task
from transport.s3 import upload_file
from transport.models import FrameDataList
from workers.video import process_video


minio_host = os.environ["MINIO_HOST"]


def process_video_handler(filepath: str, task: dict):
    # start video processing
    frame_data_list = FrameDataList(**task["recognition_results"])
    output_filepath = process_video(frame_data_list, filepath)
    # upload processed file to bucket
    url = f"http://{minio_host}:9000/processed-videos/"
    filename = os.path.basename(output_filepath)
    res = upload_file(output_filepath, url)
    if res:
        update_task(task, {"status": StatusEnum.ready})
    else:
        update_task(task, {"status": StatusEnum.error})


def generate_json_result_handler(filepath: str, task: dict):
    """
    result = [
        {
            "track_id": ...
            "class":
            "start":
            "end":
        }
    ]
    """
    frame_data_list = FrameDataList(**task["recognition_results"]).data

    # Map frames to timestamps
    n_frames = len(frame_data_list)
    cap = cv2.VideoCapture(filepath)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    cap.release()
    frame_to_timestamp = {}
    for frame_num in range(n_frames):
        time = datetime.timedelta(seconds=frame_num // fps)
        frame_to_timestamp[frame_num] = f"{time}"

    result = []

    # process tracks
    def get_unique_track_ids(frame_data_list):
        track_ids = set()
        for frame_data in frame_data_list:
            for det in frame_data.detections:
                track_ids.add(int(det.tracking_id))
        return track_ids

    unique_tracks = get_unique_track_ids(frame_data_list)
    result = [
        {
            "id": track_id,
            "class": None,
            "start": None,
            "end": None,
        }
        for track_id in unique_tracks
    ]
    track2idx = {track: i for i, track in enumerate(unique_tracks)}
    for frame_num, frame_data in enumerate(frame_data_list):
        for det in frame_data.detections:
            track_id = int(det.tracking_id)
            result[track2idx[track_id]]["class"] = det.class_name
            if result[track2idx[track_id]]["start"] is None:
                result[track2idx[track_id]]["start"] = frame_to_timestamp[frame_num]
            result[track2idx[track_id]]["end"] = frame_to_timestamp[frame_num]

    update_task(task, {"json_res": result})
