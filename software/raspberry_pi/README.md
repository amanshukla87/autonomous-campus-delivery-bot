# Raspberry Pi Navigation Software

## What it does

The primary Raspberry Pi application detects AprilTags from the Raspberry Pi Camera using the `tag36h11` family and sends single-character drive commands to the Arduino Uno over USB serial.

## Primary script: `main.py`

The primary script is `main.py`. It considers tags whose centre lies in the central 60% of the camera frame and uses the tag position to help centre the robot for Tag ID 2.

### Tag-to-command map

| Tag ID | Command sent | Action |
|---|---|---|
| 0 | `L` | Turn left |
| 1 | `R` | Turn right |
| 2 | `F` / `L` / `R` | Move forward; steer left or right to keep the tag centred |
| 3 | `B` | Move backward |
| 4 | `S` | Stop and end the program |
| No eligible tag visible | `S` | Stop (fail-safe) |

### Primary-script behaviour

- Starts by sending `F` after a 2-second delay.
- Captures 640 × 480 frames and detects AprilTags using grayscale images and the `tag36h11` family.
- Considers only tags whose centre lies in the central 60% of the frame (20% to 80% of the 640-pixel width).
- Selects the largest eligible tag when more than one tag is detected.
- Applies a 0.5-second cooldown before repeating the action for the same tag.
- Sends a serial command only when it differs from the previously sent command.
- Sends `S` when no eligible tag is visible.
- Press `q` in the camera window or use Ctrl+C to quit. The program sends `S` during shutdown.

## Alternative script: largest-tag variant

An alternative implementation is available at:

`variants/main_simple_largest_tag.py`

This version selects the largest detected tag anywhere in the frame. Tag ID 2 always maps to forward (`F`), without the centering correction used by the primary script.

Its command behaviour differs from the primary script:

- Sends `F` immediately after camera and serial setup, then waits 2.5 seconds.
- Repeats the mapped command for a visible supported tag at intervals of 0.8 seconds.
- Sends `S` when no tag is visible; an unsupported visible tag also causes a stop command.
- Tag ID 4 sends `S` and exits immediately.
- Displays the camera feed in a window titled `AprilTag Detector`.

Run the alternative explicitly from this directory:

```bash
python3 variants/main_simple_largest_tag.py
```

Both scripts use the same dependencies listed in `requirements.txt`. The alternative is retained for comparison and is not the default entry point. The actual behaviour used during the internship demonstration has not been confirmed, so this repository identifies the central-zone implementation as the primary script without claiming that it was the demonstrated version.

## Setup

Install the Raspberry Pi camera package from the Raspberry Pi OS repository:

```bash
sudo apt install python3-picamera2
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Run the primary navigation application:

```bash
python3 main.py
```

**Note:** `picamera2` is provided by the Raspberry Pi OS package `python3-picamera2`; it is not listed as a pip dependency.

The applications require a display for their OpenCV preview windows. Over SSH, use a desktop session with display forwarding or remove the `cv2.imshow` and `cv2.waitKey` preview lines when running without a display.

## Serial connection

- Interface: USB connection to the Arduino Uno
- Device: `/dev/ttyACM0`
- Baud rate: `9600`
- Commands: `F` (forward), `B` (backward), `L` (left), `R` (right), and `S` (stop)

The Arduino firmware independently monitors the HC-SR04 ultrasonic sensor, slows forward movement when the measured distance is below 30 cm, and initiates obstacle avoidance below 15 cm.
