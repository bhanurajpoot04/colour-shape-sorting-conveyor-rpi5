# Pin map

> **Important:** the pin mapping of the original class-built PCB was not recorded. The GPIO numbers below are the
> **proposed mapping used by the reference software** (`software/config.py`). They are for rebuilding the project,
> not a record of the original wiring. Edit `config.py` to match your own wiring.

## Proposed Raspberry Pi 5 mapping (BCM numbering)

| Function | GPIO | Connects to |
|---|---|---|
| Belt motor direction 1 | 17 | L293D IN1 |
| Belt motor direction 2 | 27 | L293D IN2 |
| Belt motor speed (PWM) | 22 | L293D EN1 |
| Sorting-gate servo signal | 18 | Servo header (`SERVO1` on the PCB layout) |
| Buzzer (optional) | 24 | Buzzer on the PCB |
| Camera | CSI connector | Raspberry Pi Camera (ribbon cable) |

The PCB also has a `SERVO2` header and an `IR1` header. The reference software does not use them.

## L293D reference (standard DIP-16 pinout)

| Pin | Name | Use here |
|---|---|---|
| 1 | EN1 | Speed PWM |
| 2 | IN1 | Direction |
| 3 | OUT1 | Motor terminal |
| 4, 5, 12, 13 | GND | Ground |
| 6 | OUT2 | Motor terminal |
| 7 | IN2 | Direction |
| 8 | Vs | Motor supply (12 V) |
| 16 | Vss | Logic supply (5 V) |

Check the chip marking on your board. The photo of the original PCB shows a 16-pin DIP driver IC, but the marking
is not readable in the photo.

## Recording the real mapping of a PCB (multimeter method)

1. Power everything off. Set the multimeter to continuity (beep) mode.
2. Touch one probe to a pin of the 40-pin Pi header on the PCB, and the other to the L293D pins (2, 7, 1), the servo
   header signal pin and the buzzer pad, one at a time.
3. When it beeps, note which GPIO the header pin is. Use the Raspberry Pi pinout to convert header pin numbers to GPIO numbers.
4. Write the result into the table above and into `software/config.py`.
