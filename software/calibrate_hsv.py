"""Find HSV ranges for the belt and objects with sliders.

Live camera:   python calibrate_hsv.py
From a photo:  python calibrate_hsv.py --image sample.jpg

Move the sliders until only the thing you want is white in the mask window.
Press 'p' to print the values (copy them into config.py), ESC to quit.
"""
import argparse

import cv2
import numpy as np

import config


def get_frame_source(path):
    if path:
        img = cv2.imread(path)
        if img is None:
            raise SystemExit(f"Could not read {path}")
        return lambda: img.copy(), lambda: None
    from picamera2 import Picamera2
    cam = Picamera2()
    cam.configure(cam.create_video_configuration(
        main={"size": config.FRAME_SIZE, "format": "RGB888"}))
    cam.start()
    return cam.capture_array, cam.stop


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", help="use a still image instead of the camera")
    args = ap.parse_args()
    grab, close = get_frame_source(args.image)

    cv2.namedWindow("mask")
    for name, maxv, start in [("H low", 179, 0), ("S low", 255, 100), ("V low", 255, 70),
                              ("H high", 179, 179), ("S high", 255, 255), ("V high", 255, 255)]:
        cv2.createTrackbar(name, "mask", start, maxv, lambda _v: None)

    while True:
        frame = grab()
        hsv = cv2.cvtColor(cv2.GaussianBlur(frame, (5, 5), 0), cv2.COLOR_BGR2HSV)
        low = np.array([cv2.getTrackbarPos(n, "mask") for n in ("H low", "S low", "V low")])
        high = np.array([cv2.getTrackbarPos(n, "mask") for n in ("H high", "S high", "V high")])
        mask = cv2.inRange(hsv, low, high)
        cv2.imshow("frame", frame)
        cv2.imshow("mask", mask)
        key = cv2.waitKey(30) & 0xFF
        if key == ord("p"):
            print(f"low={tuple(int(v) for v in low)}  high={tuple(int(v) for v in high)}")
        if key == 27:
            break
    close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
