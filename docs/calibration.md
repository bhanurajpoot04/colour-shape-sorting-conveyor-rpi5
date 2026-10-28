# Calibrating the colours

Lighting changes HSV values a lot, so tune the ranges on your own setup.

1. Put an object on the belt under the camera, in the lighting you will use.
2. Run `python calibrate_hsv.py` (or `python calibrate_hsv.py --image sample.jpg` on a saved photo).
3. Move the sliders until only the belt is white in the `mask` window. Press `p` and copy the values into `BELT_HSV_LOW` and `BELT_HSV_HIGH` in `config.py`.
4. Repeat for each colour you want to detect and update `COLOUR_RANGES`.
5. Set `ROI` to the part of the frame where objects are inspected, and tune `MIN_AREA` so dust and shadows are ignored.
6. Run `python test_hardware.py`, then `python sorter.py`. Adjust `TRAVEL_TIME_S`, `GATE_HOLD_S` and the gate angles until objects land in the correct bin.

Tips: use steady, diffuse light, avoid shadows on the belt, and keep objects a different colour from the belt (blue objects cannot be sorted on a blue belt).
