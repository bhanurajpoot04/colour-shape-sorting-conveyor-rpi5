"""Colour and shape detection with OpenCV. No hardware imports, so it can be tested anywhere."""
import math
from dataclasses import dataclass
from typing import Optional, Tuple

import cv2
import numpy as np

import config


@dataclass
class Detection:
    colour: str                       # "red", "green", ... or "unknown"
    shape: str                        # "circle", "square", "rectangle", "triangle", "other"
    area: float
    bbox: Tuple[int, int, int, int]   # x, y, w, h in full-frame pixels


def _crop(frame):
    if config.ROI is None:
        return frame, (0, 0)
    x, y, w, h = config.ROI
    return frame[y:y + h, x:x + w], (x, y)


def object_mask(hsv):
    """Everything that is not belt-coloured, cleaned with morphology."""
    belt = cv2.inRange(hsv, np.array(config.BELT_HSV_LOW), np.array(config.BELT_HSV_HIGH))
    mask = cv2.bitwise_not(belt)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return mask


def classify_colour(hsv, mask) -> str:
    """Pick the colour range that covers most of the object's pixels."""
    total = int(cv2.countNonZero(mask))
    if total == 0:
        return "unknown"
    best_name, best_count = "unknown", 0
    for name, ranges in config.COLOUR_RANGES.items():
        count = 0
        for low, high in ranges:
            hit = cv2.inRange(hsv, np.array(low), np.array(high))
            count += int(cv2.countNonZero(cv2.bitwise_and(hit, mask)))
        if count > best_count:
            best_name, best_count = name, count
    if best_count / total < config.MIN_COLOUR_FRACTION:
        return "unknown"
    return best_name


def classify_shape(contour) -> str:
    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)
    if perimeter == 0 or area == 0:
        return "other"
    circularity = 4 * math.pi * area / (perimeter * perimeter)
    if circularity > 0.85:
        return "circle"
    approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
    sides = len(approx)
    if sides == 3:
        return "triangle"
    if sides == 4:
        (_, _), (w, h), _ = cv2.minAreaRect(contour)
        ratio = max(w, h) / max(1.0, min(w, h))
        return "square" if ratio < 1.2 else "rectangle"
    return "other"


def find_object(frame_bgr) -> Optional[Detection]:
    """Return the largest object in the detection zone, or None."""
    roi, (ox, oy) = _crop(frame_bgr)
    blurred = cv2.GaussianBlur(roi, (5, 5), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = object_mask(hsv)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = [c for c in contours if cv2.contourArea(c) >= config.MIN_AREA]
    if not contours:
        return None
    contour = max(contours, key=cv2.contourArea)

    filled = np.zeros(mask.shape, np.uint8)
    cv2.drawContours(filled, [contour], -1, 255, thickness=cv2.FILLED)
    colour = classify_colour(hsv, filled)
    shape = classify_shape(contour)
    x, y, w, h = cv2.boundingRect(contour)
    return Detection(colour, shape, float(cv2.contourArea(contour)), (x + ox, y + oy, w, h))
