import shutil
import zipfile
from pathlib import Path

import cv2
import numpy as np
from tqdm.auto import tqdm


def get_frames(video_path: str, img_size=None):
    cap = cv2.VideoCapture(video_path)
    has_frame = True
    frames = []
    while has_frame:
        has_frame, frame = cap.read()
        if has_frame:
            if img_size:
                frame = cv2.resize(frame, img_size)
            frames.append(frame)
    cap.release()
    return frames
    


def process_raw_data(yolo_dir: Path, cvat_dir: Path, videos_dir: Path, img_size=None):
    full_dst_label_dir = yolo_dir / "labels/full"
    full_dst_label_dir.mkdir(exist_ok=True, parents=True)
    full_dst_frame_dir = yolo_dir / "images/full"
    full_dst_frame_dir.mkdir(exist_ok=True, parents=True)

    for zip_filepath in cvat_dir.glob("*.zip"):
        print(zip_filepath)

        # Prepare labels & images
        tmp_dir = zip_filepath.parent / "tmp"
        with zipfile.ZipFile(zip_filepath, 'r') as f:
            f.extractall(tmp_dir)

        labels_dir = tmp_dir / "obj_train_data"
        video_path = videos_dir / f"{zip_filepath.stem}.mp4"
        labels_filepaths = sorted(list(labels_dir.iterdir()))
        # frames = get_frames(video_path.as_posix(), img_size)
        # for src, frame in tqdm(zip(labels_filepaths, frames), total=len(labels_filepaths)):

        cap = cv2.VideoCapture(video_path.as_posix())
        for src in tqdm(labels_filepaths):
            has_frame, frame = cap.read()
            if not has_frame:
                break

            if img_size:
                frame = cv2.resize(frame, img_size)
            
            # save label
            dst_label = full_dst_label_dir / f"{zip_filepath.stem}_{src.name}"
            shutil.copy(src, dst_label)
            # save frame
            dst_frame = full_dst_frame_dir / f"{zip_filepath.stem}_{src.stem}.jpg"
            cv2.imwrite(dst_frame.as_posix(), frame)

        cap.release()

        shutil.rmtree(tmp_dir)    


def split_data(data_dir: Path, test_size=0.1):
    assert test_size < 1.0
    label_filepaths = list((data_dir / "labels/full").iterdir())
    np.random.shuffle(label_filepaths)
    sep_idx = int(len(label_filepaths) * (1 - test_size))
    for i, src_label in enumerate(label_filepaths):
        stage = "train" if i < sep_idx else "val"
        dst_label = data_dir / "labels" / stage / src_label.name
        src_frame = data_dir / "images/full" / f"{src_label.stem}.jpg"
        dst_frame = data_dir / "images" / stage / f"{src_label.stem}.jpg"
        dst_label.parent.mkdir(exist_ok=True)
        dst_frame.parent.mkdir(exist_ok=True)
        shutil.copy(src_label, dst_label)
        shutil.copy(src_frame, dst_frame)


def preprocess(yolo_dir: Path, cvat_dir: Path, videos_dir: Path, test_size=0.1, img_size=None):
    print("Process raw data")
    process_raw_data(yolo_dir, cvat_dir, videos_dir, img_size)
    print("Splitting data")
    split_data(yolo_dir, test_size)

if __name__ == "__main__":
    DEFAULT_DATA_DIR = Path(__file__).parent / "datasets/construction_analytics"
    DEFAULT_YOLO_DIR = DEFAULT_DATA_DIR / "yolo"
    DEFAULT_CVAT_DIR = DEFAULT_DATA_DIR / "cvat"
    DEFAULT_VIDEO_DIR = DEFAULT_DATA_DIR / "videos"
    preprocess(
        DEFAULT_YOLO_DIR,
        DEFAULT_CVAT_DIR,
        DEFAULT_VIDEO_DIR,
        0.1,
        None
    )
