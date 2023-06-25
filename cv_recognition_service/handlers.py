import os
from dataclasses import asdict

from transport.database import StatusEnum, update_task
from transport.s3 import upload_file
from workers.video import process_video

minio_host = os.environ["MINIO_HOST"]


def process_video_handler(filepath: str, task: dict):
    # start video processing
    res = process_video(filepath)
    if res:
        update_task(task, {"status": StatusEnum.cv_ready, "recognition_results": asdict(res)})
    else:
        update_task(task, {"status": StatusEnum.error})
