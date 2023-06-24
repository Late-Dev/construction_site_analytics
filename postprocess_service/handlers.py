import os
import dataclasses

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
