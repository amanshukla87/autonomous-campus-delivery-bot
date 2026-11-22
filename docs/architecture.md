# System Architecture

## Overview

The Autonomous Campus Delivery Bot uses a two-controller architecture. A Raspberry Pi 5 performs camera-based AprilTag detection and high-level navigation decisions. An Arduino Uno receives movement commands over USB serial and controls the motors through an L298N driver while monitoring the HC-SR04 ultrasonic sensor.

## Control flow

1. The Raspberry Pi Camera Module 2 captures 640 × 480 image frames.
2. OpenCV converts each frame to grayscale.
3. The `pupil_apriltags` detector searches for markers from the `tag36h11` family.
4. The navigation program considers tags whose horizontal centre lies between 20% and 80% of the frame width. If multiple eligible tags are detected, it selects the largest.
5. The Raspberry Pi maps the selected tag ID to a single-character command and sends it to the Arduino over USB serial at 9600 baud.
6. The Arduino applies the requested movement while independently monitoring the ultrasonic distance.
7. The loop repeats until the stop tag is detected, the operator quits, or the program is interrupted.

## AprilTag command map

The mapping below reflects the current Raspberry Pi implementation in `software/raspberry_pi/main.py`.

| Tag ID | Action | Command sent to Arduino |
|---|---|---|
| 0 | Turn Left | `L` |
| 1 | Turn Right | `R` |
| 2 | Align Forward (steers left/right to keep the tag centred) | `F` / `L` / `R` |
| 3 | Move Backward | `B` |
| 4 | Stop & Exit | `S` |
| No tag visible | Stop (fail-safe) | `S` |

For tag ID 2, the script uses the tag's horizontal centre to choose forward, left, or right movement. A 0.5-second cooldown is applied before repeating an action for the same tag. A command is transmitted only when it differs from the previously transmitted command.

## Raspberry Pi to Arduino serial interface

- Connection: USB serial
- Raspberry Pi serial device configured in the script: `/dev/ttyACM0`
- Baud rate: `9600`
- Command characters: `F` (forward), `B` (backward), `L` (left), `R` (right), and `S` (stop)

The Raspberry Pi sends `S` when no eligible AprilTag is visible. It also sends `S` during normal program shutdown.

## Arduino motor-control and obstacle response

The Arduino Uno drives the L298N motor driver and reads the HC-SR04 ultrasonic sensor. The current firmware uses the following distance thresholds during forward movement:

- Below 30 cm: reduce motor PWM to the configured slow speed.
- Below 15 cm: enter the obstacle-avoidance routine.

The avoidance routine stops the motors, reverses briefly, turns left or right on alternating attempts, and checks the distance again before resuming forward movement. The Arduino also beeps three times during startup.

## Hardware interfaces

| Controller | Interface | Connected component / purpose |
|---|---|---|
| Raspberry Pi 5 | CSI camera interface | Raspberry Pi Camera Module 2 |
| Raspberry Pi 5 | USB serial | Arduino Uno command link |
| Arduino Uno | Digital/PWM outputs | L298N motor driver |
| Arduino Uno | Digital trigger/echo | HC-SR04 ultrasonic sensor |
| Arduino Uno | Digital output | Buzzer |

Refer to [hardware/wiring_and_pinout.md](../hardware/wiring_and_pinout.md) for the detailed pin assignments when that document is available.

## Software locations

- Raspberry Pi navigation application: [`software/raspberry_pi/main.py`](../software/raspberry_pi/main.py)
- Raspberry Pi setup and dependency guide: [`software/raspberry_pi/README.md`](../software/raspberry_pi/README.md)
- Arduino motor-control firmware: [`firmware/arduino_motor_controller/arduino_motor_controller.ino`](../firmware/arduino_motor_controller/arduino_motor_controller.ino)

This document describes the current source-code behaviour. Hardware timing, turning performance, sensing accuracy, and end-to-end navigation performance should be treated as unverified until measured through physical testing.
