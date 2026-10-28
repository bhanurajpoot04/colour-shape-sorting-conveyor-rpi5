"""Raspberry Pi 5 colour and shape sorting conveyor - REFERENCE implementation.

Rebuilt for this repository (the original training code was lost). Vision logic is
checked on synthetic images only; this script has NOT been run on the original machine.

Run:  python sorter.py        (Ctrl+C to stop)
"""
import time
from collections import Counter

import config
from vision import Detection, find_object


def decide(det: Detection) -> str:
    """Return 'divert' or 'pass' for a detected object."""
    if det.colour in config.DIVERT_COLOURS or det.shape in config.DIVERT_SHAPES:
        return "divert"
    return "pass"


class Scheduler:
    """Run actions after a delay without blocking the camera loop."""

    def __init__(self):
        self._jobs = []

    def call_later(self, delay, fn):
        self._jobs.append((time.monotonic() + delay, fn))

    def run_due(self):
        now = time.monotonic()
        due = sorted((j for j in self._jobs if j[0] <= now), key=lambda j: j[0])
        self._jobs = [j for j in self._jobs if j[0] > now]
        for _, fn in due:
            fn()


def main():
    # Hardware imports live here so vision.py and decide() can be tested on any computer.
    import cv2
    from gpiozero import AngularServo, Buzzer, Motor
    from picamera2 import Picamera2

    pins = config.PINS
    motor = Motor(forward=pins["motor_in1"], backward=pins["motor_in2"],
                  enable=pins["motor_en"], pwm=True)
    gate = AngularServo(pins["servo"], min_angle=0, max_angle=180,
                        min_pulse_width=0.0005, max_pulse_width=0.0025,
                        initial_angle=config.GATE_PASS_ANGLE)
    buzzer = Buzzer(pins["buzzer"]) if config.USE_BUZZER else None

    cam = Picamera2()
    # "RGB888" in Picamera2 is stored as B,G,R, which is what OpenCV expects.
    cam.configure(cam.create_video_configuration(
        main={"size": config.FRAME_SIZE, "format": "RGB888"}))
    cam.start()
    time.sleep(1.0)  # let exposure settle

    scheduler = Scheduler()
    counts = Counter()
    in_zone = False
    empty_frames = config.REARM_FRAMES

    def set_gate(angle):
        gate.angle = angle

    def beep():
        if buzzer:
            buzzer.beep(on_time=0.1, off_time=0.0, n=1, background=True)

    print("Starting belt. Press Ctrl+C to stop.")
    motor.forward(config.BELT_SPEED)
    try:
        while True:
            frame = cam.capture_array()
            det = find_object(frame)

            if det is None:
                empty_frames += 1
                if empty_frames >= config.REARM_FRAMES:
                    in_zone = False
            else:
                empty_frames = 0
                if not in_zone:
                    in_zone = True
                    action = decide(det)
                    counts[(det.colour, det.shape, action)] += 1
                    print(f"{time.strftime('%H:%M:%S')}  {det.colour:7s} {det.shape:9s} -> {action}")
                    beep()
                    if action == "divert":
                        scheduler.call_later(config.TRAVEL_TIME_S,
                                             lambda: set_gate(config.GATE_DIVERT_ANGLE))
                        scheduler.call_later(config.TRAVEL_TIME_S + config.GATE_HOLD_S,
                                             lambda: set_gate(config.GATE_PASS_ANGLE))

            scheduler.run_due()

            if config.SHOW_PREVIEW:
                if det is not None:
                    x, y, w, h = det.bbox
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, f"{det.colour} {det.shape}", (x, max(y - 8, 12)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                cv2.imshow("sorter", frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
    except KeyboardInterrupt:
        pass
    finally:
        motor.stop()
        gate.angle = config.GATE_PASS_ANGLE
        cam.stop()
        if config.SHOW_PREVIEW:
            cv2.destroyAllWindows()
        print("\nStopped. Totals:")
        for (colour, shape, action), n in sorted(counts.items()):
            print(f"  {colour:7s} {shape:9s} {action:6s} x{n}")


if __name__ == "__main__":
    main()
