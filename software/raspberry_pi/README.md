# Raspberry Pi Navigation Software

## What it does

Detects AprilTags from the Raspberry Pi Camera using the `tag36h11` family and sends single-character drive commands to the Arduino Uno over USB serial.

## Tag-to-command map

| Tag ID | Command sent | Action |
|---|---|---|
| 0 | `L` | Turn left |
| 1 | `R` | Turn right |
| 2 | `F` / `L` / `R` | Move forward; steer left or right if the tag drifts toward the frame edge |
| 3 | `B` | Move backward |
| 4 | `S` | Stop and end the program |
| none visible | `S` | Stop (fail-safe) |

## Behaviour

- Starts by sending `F` after a 2-second delay.
- Captures 640 × 480 frames and detects AprilTags using grayscale images and the `tag36h11` family.
- Considers only tags whose centre lies in the central 60% of the frame (20% to 80% of the 640-pixel width).
- Selects the largest eligible tag when more than one tag is detected.
- Applies a 0.5-second cooldown before repeating the action for the same tag.
- Sends a serial command only when it differs from the previously sent command.
- Sends `S` when no eligible tag is visible.
- Press `q` in the camera window or use Ctrl+C to quit. The program sends `S` during shutdown.

## Setup

Install the Raspberry Pi camera package from the Raspberry Pi OS repository:

```bash
sudo apt install python3-picamera2
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Run the navigation application:

```bash
python3 main.py
```

**Note:** `picamera2` is provided by the Raspberry Pi OS package `python3-picamera2`; it is not listed as a pip dependency.

The application requires a display for the `Bot Cam` preview window. Over SSH, use a desktop session with display forwarding or remove the `cv2.imshow` and `cv2.waitKey` preview lines when running without a display.

## Serial connection

- Interface: USB connection to the Arduino Uno
- Device: `/dev/ttyACM0`
- Baud rate: `9600`
- Commands: `F` (forward), `B` (backward), `L` (left), `R` (right), and `S` (stop)

The Arduino firmware independently monitors the HC-SR04 ultrasonic sensor, slows forward movement when the measured distance is below 30 cm, and initiates obstacle avoidance below 15 cm.
