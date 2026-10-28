# Working principle

*Adapted from the project report (sections 4.1 to 4.6).*

## Computer vision sorting

This project applies image processing to industrial sorting. A Raspberry Pi identifies the colour of objects on a
moving belt, works out their shape, and runs a logic-based command to manage the flow of items.

## How it works

The system runs a real-time image processing and mechanical control loop.

1. **Conveyor movement:** a DC motor, driven through a motor driver, moves objects towards the inspection zone.
2. **Image capture:** when an object enters the detection zone, the Pi Camera captures frames.
3. **Processing:** the Raspberry Pi uses OpenCV to read pixel values in a colour space to identify the object's colour, and uses contour approximation to find its shape.
4. **Decision:** once the object is classified, the system chooses the sorting bin.
5. **Actuation:** the Raspberry Pi moves a servo-driven gate to divert the object into the right bin.
6. **Continuous cycle:** sensing, processing and actuation repeat for every object.

## Advantages

- **Fewer errors:** removes human error and fatigue in repetitive sorting.
- **High throughput:** can process many objects quickly.
- **Reliability:** a camera-based system gives consistent results and can connect to larger industrial systems.

## Applications

- **Food processing:** separating fruits, vegetables or candies by colour and quality.
- **Waste management:** sorting plastics, glass and paper in recycling.
- **Pharmaceuticals:** finding pills or capsules with colour defects.
