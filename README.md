# HAL 9000 cam

A docker-compose version of
[Elder's fakecam code](https://elder.dev/posts/open-source-virtual-background/)
that captures the `/dev/video0/` camera, performs person segmentation using the
[TensorFlow body-pix model](https://github.com/tensorflow/tfjs-models/tree/master/body-pix),
adds a HAL 9000 background and some hologram effects to the real-time camera.
A new fake camera called `hal9000_cam` is created that can be used in any
video conferencing system such as Google Meet, Teams, or Zoom.

![HAL 9000](https://raw.githubusercontent.com/DrAA/hal9000-cam/master/capture/background.png)

# Installation

```bash
sudo apt install v4l2loopback-dkms
sudo modprobe -r v4l2loopback
```

# Building

```bash
make build
```

# Running

```bash
make run
```

To remove the hologram effects, set the `HOLOGRAM` env to 0 (no effect) or
1 (only some blurring), instead of default 2 (all effects). To change input camera device, set the `CAMERA` env variable.

```bash
HOLOGRAM=0 CAMERA=/dev/video2 make run
```
