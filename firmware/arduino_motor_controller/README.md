# Arduino Motor Controller Firmware

This directory contains the Arduino Uno firmware for motor control and ultrasonic obstacle monitoring.

## Firmware

- `arduino_motor_controller.ino` — Main Arduino sketch.

## Functionality

- Receives single-character movement commands from the Raspberry Pi over USB serial at 9600 baud: `F`, `B`, `L`, `R`, and `S`.
- Controls the L298N motor driver using the pin assignments defined in the sketch.
- Reads the HC-SR04 ultrasonic sensor using five-sample averaging.
- Reduces forward motor speed when the measured distance is below 30 cm.
- Starts the obstacle-avoidance routine when the measured distance is below 15 cm. The routine briefly reverses, alternates its turn direction, and checks the distance before resuming forward movement.
- Produces three short buzzer beeps during startup.

See the source file for the exact pin assignments and control implementation. Physical motor behaviour and obstacle-response performance should be validated on the assembled robot.
