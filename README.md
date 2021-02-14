# Installation

https://elder.dev/posts/open-source-virtual-background/

```bash
sudo apt install v4l2loopback-dkms
sudo modprobe -r v4l2loopback
sudo modprobe v4l2loopback devices=1 video_nr=20 card_label="v4l2loopback" exclusive_caps=1
sudo chmod +rw /dev/video20
```

# Building

```bash
make build
```

# Running

```bash
docker run --rm   --name=bodyfix   --network=fakecam   -p 9000:9000   --gpus=all --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864   bodyfix

docker run --rm --name=fakecam   --network=fakecam   -u "$(id -u):$(getent group video | cut -d: -f3)"   $(sudo find /dev -name 'video*' -printf "--device %p ") fakecam

# -itu0 --entrypoint bash

CURRENT_UID=$(id -u):$(getent group video | cut -d: -f3) docker-compose up
```
