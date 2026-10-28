"""Check the motor, servo gate and buzzer one at a time, before running the sorter.

Keep the belt clear and be ready to cut the 12 V supply. Press Enter at each prompt.
"""
import time

import config
from gpiozero import AngularServo, Buzzer, Motor

pins = config.PINS
motor = Motor(forward=pins["motor_in1"], backward=pins["motor_in2"],
              enable=pins["motor_en"], pwm=True)
gate = AngularServo(pins["servo"], min_angle=0, max_angle=180,
                    min_pulse_width=0.0005, max_pulse_width=0.0025,
                    initial_angle=config.GATE_PASS_ANGLE)

input("1/3  Belt motor forward for 3 s. Press Enter... ")
motor.forward(config.BELT_SPEED)
time.sleep(3)
motor.stop()

input("2/3  Gate: PASS -> DIVERT -> PASS. Press Enter... ")
for angle in (config.GATE_PASS_ANGLE, config.GATE_DIVERT_ANGLE, config.GATE_PASS_ANGLE):
    gate.angle = angle
    time.sleep(1.0)

if config.USE_BUZZER:
    input("3/3  Buzzer beep. Press Enter... ")
    Buzzer(pins["buzzer"]).beep(on_time=0.2, off_time=0.2, n=2, background=False)

print("Done.")
