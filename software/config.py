"""All tunable settings for the sorter in one place.

Everything marked PROPOSED / TUNE is a starting value for a rebuild. The original
project's pin numbers and tuned values were not recorded, so check each one against
your own wiring and lighting before running.
"""

# ---- GPIO pins (BCM numbering) -------------------------------------------
# PROPOSED mapping. The pin mapping of the original PCB was not recorded.
# Edit these to match how your Raspberry Pi is actually wired.
PINS = {
    "motor_in1": 17,   # L293D IN1
    "motor_in2": 27,   # L293D IN2
    "motor_en": 22,    # L293D EN1 (PWM speed control)
    "servo": 18,       # sorting-gate servo signal
    "buzzer": 24,      # optional buzzer
}
USE_BUZZER = True

# ---- Camera ---------------------------------------------------------------
FRAME_SIZE = (640, 480)
# Detection zone as (x, y, width, height) in pixels. None = whole frame.   TUNE
ROI = None

# ---- Belt -----------------------------------------------------------------
BELT_SPEED = 0.6          # 0.0 - 1.0 PWM duty                              TUNE

# ---- Colour model (OpenCV HSV: H 0-179, S 0-255, V 0-255) -----------------
# The belt is blue, so anything that is NOT belt-coloured is treated as an object.
# This means blue objects cannot be sorted on this belt.                    TUNE
BELT_HSV_LOW = (95, 70, 50)
BELT_HSV_HIGH = (130, 255, 255)

COLOUR_RANGES = {                                                        # TUNE
    "red":    [((0, 100, 70), (10, 255, 255)), ((170, 100, 70), (179, 255, 255))],
    "orange": [((11, 100, 70), (22, 255, 255))],
    "yellow": [((23, 100, 70), (35, 255, 255))],
    "green":  [((36, 70, 50), (85, 255, 255))],
}
MIN_COLOUR_FRACTION = 0.30   # a colour must cover this share of the object

# ---- Object detection -----------------------------------------------------
MIN_AREA = 1500              # ignore blobs smaller than this (pixels^2)       TUNE
REARM_FRAMES = 5             # empty frames needed before the next object counts

# ---- Sorting rules --------------------------------------------------------
# The gate has two positions: PASS (object continues) or DIVERT (object pushed
# into the side bin). An object is diverted if its colour OR shape matches.
DIVERT_COLOURS = {"red"}
DIVERT_SHAPES = set()        # e.g. {"triangle"}

# ---- Gate servo and timing ------------------------------------------------
GATE_PASS_ANGLE = 90         # degrees                                         TUNE
GATE_DIVERT_ANGLE = 40       # degrees                                         TUNE
TRAVEL_TIME_S = 1.5          # camera zone -> gate                             TUNE
GATE_HOLD_S = 1.0            # how long the gate stays diverted                TUNE

SHOW_PREVIEW = False         # True = open an OpenCV window (needs a display)
