FROM jrottenberg/ffmpeg:3.4-ubuntu2004
ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /postprocess_service

COPY requirements.txt $WORKDIR

RUN apt-get update && apt-get clean && apt-get install g++ libsm6 libxext6 python3 python3-pip libgl1-mesa-dev libglib2.0-0 -y

RUN pip install -U pip && \
    pip install -r requirements.txt

COPY . $WORKDIR

ENTRYPOINT [ "python3", "main.py" ]
