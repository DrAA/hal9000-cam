#!/usr/bin/env bash
if [[ ! -e /dev/video20 ]]
then
    sudo modprobe \
        v4l2loopback \
        devices=1 \
        video_nr=20 \
        card_label="hal9000_cam" \
        exclusive_caps=1
fi
