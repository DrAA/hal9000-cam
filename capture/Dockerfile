FROM python:3-slim-buster
ARG BACKGROUND_PATH

RUN pip install --upgrade pip
RUN apt-get update && \
    apt-get install -y \
      `# opencv requirements` \
      libsm6 libxext6 libxrender-dev libgl1 libglib2.0 \
      `# opencv video opening requirements` \
      libv4l-dev

WORKDIR /src
COPY requirements.txt /src/
RUN pip install --no-cache-dir -r /src/requirements.txt
COPY ${BACKGROUND_PATH} capture.py /src/
ENTRYPOINT python -u /src/capture.py
