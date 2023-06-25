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


def date_to_secs(date):
    date = datetime.datetime.strptime(date, "%H:%M:%S")
    secs = date.second + date.minute * 60 + date.hour * 60 * 60
    return secs


def date_to_frame_num(date, fps):
    date = datetime.datetime.strptime(date, "%H:%M:%S")
    secs = date.second + date.minute * 60 + date.hour * 60 * 60
    return secs * fps


def find_track(track_id, tracks, frame_num, fps, activity=1):
    if activity == -1:
        for i, t in enumerate(tracks):
            if t["id"] == track_id:
                return i
    elif activity == 1:
        for i, t in enumerate(tracks):
            if (
                t["id"] == track_id
                and t["type"] == ""
                and date_to_frame_num(t["end"], fps) + 2 * fps >= frame_num
            ):
                return i
    else:
        for i in range(len(tracks) - 1, -1, -1):
            t = tracks[i]
            if (
                t["id"] == track_id
                and t["type"] == "простой"
                and date_to_frame_num(t["end"], fps) + 2 * fps >= frame_num
            ):
                return i
    return -1


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

    # get unique tracks
    def get_unique_track_ids(frame_data_list):
        track_ids = set()
        for frame_data in frame_data_list:
            for det in frame_data.detections:
                track_ids.add(int(det.tracking_id))
        return track_ids

    unique_tracks = get_unique_track_ids(frame_data_list)

    # process tracks data
    result = [
        {
            "id": track_id,
            "class": None,
            "start": "0:00:00",
            "end": "0:00:00",
            "type": "",
        }
        for track_id in unique_tracks
    ]
    for frame_num, frame_data in enumerate(frame_data_list):
        for det in frame_data.detections:
            track_id = int(det.tracking_id)
            idx = find_track(track_id, result, frame_num, fps, -1)
            result[idx]["class"] = det.class_name
            if result[idx]["start"] is None:
                result[idx]["start"] = frame_to_timestamp[frame_num]
            result[idx]["end"] = frame_to_timestamp[frame_num]
            if not det.activity:
                activity_endtime = date_to_frame_num(result[idx]["end"], fps)
                if activity_endtime + 2 * fps >= frame_num:
                    idx = find_track(track_id, result, frame_num, fps, 0)
                    if idx == -1:
                        result.append(
                            {
                                "id": track_id,
                                "class": det.class_name,
                                "start": frame_to_timestamp[frame_num],
                                "end": frame_to_timestamp[frame_num],
                                "type": "простой",
                            }
                        )
                    else:
                        result[idx]["end"] = frame_to_timestamp[frame_num]
                else:
                    idx = find_track(track_id, result, frame_num, fps, 0)
                    result[idx]["end"] = frame_to_timestamp[frame_num]

    result = list(filter(lambda res: res["start"] != res["end"], result))

    update_task(task, {"json_res": result})
