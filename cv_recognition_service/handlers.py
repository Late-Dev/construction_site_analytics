import os

from transport.database import StatusEnum, update_task
from transport.s3 import upload_file
from workers.video import create_preview_image, process_video

minio_host = os.environ["MINIO_HOST"]

def process_video_handler(filepath: str, task: dict):
    # start video processing
    output_filepath = process_video(filepath)
    # upload processed file to bucket
    url = f"http://{minio_host}:9000/processed-videos/"
    filename = os.path.basename(output_filepath)
    res = upload_file(output_filepath, url)
    if res:
        update_task(task, {"status": StatusEnum.ready})
    else:
        update_task(task, {"status": StatusEnum.error})
