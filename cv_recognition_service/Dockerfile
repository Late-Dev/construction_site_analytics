FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime
ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /cv_recognition_service

COPY requirements.txt $WORKDIR

RUN apt-get update && apt-get clean && apt-get install g++ ffmpeg libsm6 libxext6 git -y

RUN pip install -U pip && \
    pip install jupyter && \
    pip install -r requirements.txt --no-cache-dir

RUN pip install lap>=0.4

COPY . $WORKDIR

# CMD jupyter notebook --ip 0.0.0.0 --port 9988 --allow-root --NotebookApp.token=""
ENTRYPOINT [ "bash", "start.sh" ]
