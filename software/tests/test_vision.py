"""Checks the vision logic on synthetic frames (blue belt + coloured shapes).

Run from the software/ folder:  python -m pytest tests
These tests use drawn images only. They do not prove the sorter works on the real machine.
"""
import os
import sys
import time

import cv2
import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import config
from sorter import Scheduler, decide
from vision import find_object

HUES = {"red": 0, "orange": 16, "yellow": 30, "green": 60}


def bgr(h, s=220, v=220):
    return tuple(int(c) for c in cv2.cvtColor(np.uint8([[[h, s, v]]]), cv2.COLOR_HSV2BGR)[0, 0])


def belt_frame():
    frame = np.full((480, 640, 3), bgr(110, 200, 200), np.uint8)
    noise = np.random.default_rng(1).normal(0, 4, frame.shape)
    return np.clip(frame + noise, 0, 255).astype(np.uint8)


def draw(frame, shape, colour):
    c = bgr(HUES[colour])
    if shape == "circle":
        cv2.circle(frame, (320, 240), 60, c, -1)
    elif shape == "square":
        cv2.rectangle(frame, (260, 180), (380, 300), c, -1)
    elif shape == "rectangle":
        cv2.rectangle(frame, (230, 200), (410, 280), c, -1)
    elif shape == "triangle":
        cv2.fillPoly(frame, [np.array([(320, 170), (250, 300), (390, 300)])], c)
    return frame


@pytest.mark.parametrize("shape", ["circle", "square", "rectangle", "triangle"])
@pytest.mark.parametrize("colour", ["red", "orange", "yellow", "green"])
def test_colour_and_shape(shape, colour):
    det = find_object(draw(belt_frame(), shape, colour))
    assert det is not None
    assert det.colour == colour
    assert det.shape == shape


def test_empty_belt_gives_none():
    assert find_object(belt_frame()) is None


def test_tiny_speck_is_ignored():
    frame = belt_frame()
    cv2.circle(frame, (100, 100), 8, bgr(HUES["red"]), -1)
    assert find_object(frame) is None


def test_decide_follows_rules(monkeypatch):
    monkeypatch.setattr(config, "DIVERT_COLOURS", {"red"})
    monkeypatch.setattr(config, "DIVERT_SHAPES", {"triangle"})
    red = find_object(draw(belt_frame(), "circle", "red"))
    green_tri = find_object(draw(belt_frame(), "triangle", "green"))
    green_sq = find_object(draw(belt_frame(), "square", "green"))
    assert decide(red) == "divert"
    assert decide(green_tri) == "divert"
    assert decide(green_sq) == "pass"


def test_scheduler_runs_jobs_in_order():
    ran = []
    s = Scheduler()
    s.call_later(0.02, lambda: ran.append("second"))
    s.call_later(0.0, lambda: ran.append("first"))
    s.run_due()
    assert ran == ["first"]
    time.sleep(0.05)
    s.run_due()
    assert ran == ["first", "second"]
