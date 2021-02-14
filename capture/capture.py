from argparse import ArgumentParser
import itertools
import os
import time

import cv2
import numpy as np
import pyfakewebcam
import requests
from tqdm import tqdm


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--realcam-dev', default='/dev/video0')
    parser.add_argument('--fakecam-dev', default='/dev/video20')
    parser.add_argument('--width', default=848, type=int)
    parser.add_argument('--height', default=480, type=int)
    parser.add_argument('--fps', default=60, type=int)
    parser.add_argument('--bodypix-url', default='http://bodypix:9000')
    parser.add_argument(
        '--background-path',
        default=os.getenv('BACKGROUND_PATH', 'background.png'))
    parser.add_argument(
        '--hologram', type=int,
        default=os.getenv('HOLOGRAM', '2'))
    return parser.parse_args()


def get_mask(frame):
    _, data = cv2.imencode(".jpg", frame)
    r = requests.post(
        url=args.bodypix_url,
        data=data.tobytes(),
        headers={'Content-Type': 'application/octet-stream'})
    mask = np.frombuffer(r.content, dtype=np.uint8)
    mask = mask.reshape((frame.shape[0], frame.shape[1]))
    return mask


def post_process_mask(mask):
    mask = cv2.dilate(mask, np.ones((10, 10), np.uint8), iterations=1)
    mask = cv2.blur(mask.astype(float), (30, 30))
    return mask


def shift_image(img, dx, dy):
    img = np.roll(img, dy, axis=0)
    img = np.roll(img, dx, axis=1)
    if dy > 0:
        img[:dy, :] = 0
    elif dy < 0:
        img[dy:, :] = 0
    if dx > 0:
        img[:, :dx] = 0
    elif dx < 0:
        img[:, dx:] = 0
    return img


def hologram_effect(img):
    # add a blue tint
    holo = cv2.applyColorMap(img, cv2.COLORMAP_HOT)

    # add a halftone effect
    bandLength, bandGap = 1, 4
    for y in range(holo.shape[0]):
        if y % (bandLength+bandGap) < bandLength:
            holo[y, :, :] = holo[y, :, :] * np.random.uniform(0.3, 0.3)

    # add some ghosting
    holo_blur = cv2.addWeighted(
        holo, 0.7, shift_image(holo.copy(), 3, 3), 0.8, 0)
    holo_blur = cv2.addWeighted(
        holo_blur, 0.8, shift_image(holo.copy(), -3, -3), 0.9, 0)

    # combine with the original color, oversaturated
    out = cv2.addWeighted(img, 0.7, holo_blur, 0.3, 0)

    return out


def get_frame(cam, background):
    _, frame = cam.read()
    mask = None
    while mask is None:
        try:
            mask = get_mask(frame)
        except requests.RequestException:
            print("Accessing realcam failed, retrying")
            time.sleep(1)

    # post-process mask and frame
    if args.hologram > 0:
        mask = post_process_mask(mask)
    if args.hologram > 1:
        frame = hologram_effect(frame)

    # composite the foreground and background
    inv_mask = 1-mask
    for c in range(frame.shape[2]):
        frame[:, :, c] = (
            frame[:, :, c] * mask + background[:, :, c] * inv_mask)

    return frame


def setup_cam():
    realcam = cv2.VideoCapture(args.realcam_dev)
    realcam.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    realcam.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)
    realcam.set(cv2.CAP_PROP_FPS, args.fps)

    fakecam = pyfakewebcam.FakeWebcam(
        video_device=args.fakecam_dev,
        width=args.width,
        height=args.height
    )

    return realcam, fakecam


def setup_background():
    background = cv2.imread(args.background_path)
    scaled_background = cv2.resize(
        src=background,
        dsize=(args.width, args.height),
    )
    return scaled_background


def main():
    realcam, fakecam = setup_cam()
    background = setup_background()

    print(
        f'Starting capture using background {args.background_path} and '
        f'hologram effects {args.hologram}')
    for frame_index in tqdm(itertools.count(), unit=' frames'):
        frame = get_frame(realcam, background)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        fakecam.schedule_frame(frame)
        if frame_index % 100 == 1:
            print()


if __name__ == '__main__':
    args = parse_args()
    main()
