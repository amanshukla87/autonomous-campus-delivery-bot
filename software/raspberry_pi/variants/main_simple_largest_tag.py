"""
Autonomous Campus Delivery Bot - Raspberry Pi AprilTag Navigation
Kalam Pragati MakeX Internship 2025 | Team AVENGERS (Team 10)

Captures frames from the Pi Camera, detects tag36h11 AprilTags with
pupil_apriltags, picks the largest (closest) tag and sends a single-character
drive command (F/B/L/R/S) to the Arduino Uno over USB serial
(/dev/ttyACM0, 9600 baud). Commands repeat every 0.8 s while a tag is visible.
"""

import cv2
import time
import serial
from picamera2 import Picamera2
from pupil_apriltags import Detector


# ---------------- Serial Setup ----------------
try:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    time.sleep(2)
    print("[✓] Arduino connected")
except serial.SerialException:
    print("[X] Arduino not found. Check USB port.")
    raise SystemExit(1)


# ---------------- Camera Setup ----------------
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(config)
picam2.start()
time.sleep(1.0)
print("[📷] Camera initialized")


# ---------------- AprilTag Detector Setup ----------------
detector = Detector(
    families='tag36h11',
    nthreads=2,
    quad_decimate=1.0,
    refine_edges=1,
    decode_sharpening=0.25,
    debug=0
)


# ---------------- Parameters ----------------
last_command_sent = None
last_action_time = 0.0
send_interval = 0.8


# ---------------- Utility ----------------
def send_command(cmd):
    """Send a single-character command to the Arduino."""
    global last_command_sent

    print(f"[>>] Sending command: {cmd}")
    ser.write(cmd.encode())
    last_command_sent = cmd


# ---------------- Initial Move ----------------
print("[🚀] Initial move: Forward")
send_command('F')
time.sleep(2.5)


# ---------------- Main Loop ----------------
print("[▶] Running. Press 'q' to quit.")

try:
    while True:
        frame = picam2.capture_array()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detections = detector.detect(gray)

        # Select the largest detected tag anywhere in the frame.
        best_tag = None
        best_size = 0.0

        for tag in detections:
            size = cv2.norm(tag.corners[0] - tag.corners[2])
            if size > best_size:
                best_size = size
                best_tag = tag

        now = time.time()

        if best_tag is not None:
            tag_id = best_tag.tag_id

            # Stop immediately for the stop tag, regardless of the repeat timer.
            if tag_id == 4:
                send_command('S')
                print("[🛑] STOP tag detected. Exiting.")
                break

            action = {
                0: 'L',
                1: 'R',
                2: 'F',
                3: 'B',
            }.get(tag_id)

            if action is None:
                # Unknown visible tags must not leave an old movement active.
                if last_command_sent != 'S':
                    send_command('S')
            elif now - last_action_time >= send_interval:
                send_command(action)
                last_action_time = now

            # Draw the selected tag outline and ID.
            for i in range(4):
                pt1 = tuple(best_tag.corners[i - 1, :].astype(int))
                pt2 = tuple(best_tag.corners[i, :].astype(int))
                cv2.line(frame, pt1, pt2, (255, 0, 0), 2)

            cv2.putText(
                frame,
                f"ID {tag_id}",
                (int(best_tag.center[0]) - 10, int(best_tag.center[1]) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2
            )

        else:
            # Send stop only when the command needs to change.
            if last_command_sent != 'S':
                send_command('S')

        cv2.imshow("AprilTag Detector", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\\n[CTRL+C] Interrupted by user")

finally:
    send_command('S')
    ser.close()
    picam2.stop()
    cv2.destroyAllWindows()
    print("[✔] Cleanup complete.")
