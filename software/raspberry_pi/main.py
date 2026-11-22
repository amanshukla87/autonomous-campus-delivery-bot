"""
Autonomous Campus Delivery Bot - Raspberry Pi AprilTag Navigation
Kalam Pragati MakeX Internship 2025 | Team AVENGERS (Team 10)

Captures frames from the Pi Camera, detects tag36h11 AprilTags with
pupil_apriltags, and sends single-character drive commands (F/B/L/R/S)
to the Arduino Uno over USB serial (/dev/ttyACM0, 9600 baud).
Only tags inside the centre 60% of the frame are considered.
"""

import cv2
import time
import serial
from picamera2 import Picamera2
from pupil_apriltags import Detector


# ---------------- Serial Setup ----------------
# Connect to the Arduino Uno over USB serial.
try:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    time.sleep(2)  # Allow the Arduino serial connection to initialise.
    print("[✓] Arduino connected")
except serial.SerialException:
    print("[X] Arduino not found. Check USB port.")
    exit()


# ---------------- Camera Setup ----------------
# Configure the Raspberry Pi Camera for 640 x 480 preview frames.
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(
    main={"size": (640, 480)}
)
picam2.configure(camera_config)
picam2.start()
time.sleep(1.0)
print("[📷] Camera initialized")


# ---------------- AprilTag Detector Setup ----------------
# Detect AprilTags from the tag36h11 family.
detector = Detector(
    families='tag36h11',
    nthreads=2,
    quad_decimate=1.0,
    refine_edges=1,
    decode_sharpening=0.25,
    debug=0
)


# ---------------- Parameters ----------------
last_command = None
last_tag_id = None
last_action_time = 0
cooldown = 0.5

frame_width = 640
center_zone_start = int(frame_width * 1 / 5)  # 20% of frame width.
center_zone_end = int(frame_width * 4 / 5)    # 80% of frame width.


# ---------------- Utility Functions ----------------
def send_command(cmd):
    """Send a command only when it differs from the previous command."""
    global last_command

    if cmd != last_command:
        ser.write(cmd.encode())
        print(f"[>>] Sent: {cmd}")
        last_command = cmd


def draw_ui(frame):
    """Draw the boundaries of the central AprilTag detection zone."""
    cv2.line(
        frame,
        (center_zone_start, 0),
        (center_zone_start, frame.shape[0]),
        (200, 200, 200),
        2
    )
    cv2.line(
        frame,
        (center_zone_end, 0),
        (center_zone_end, frame.shape[0]),
        (200, 200, 200),
        2
    )


# ---------------- Initial Movement ----------------
# Start with a forward command after the initial two-second delay.
print("[🚀] Starting in 2s...")
time.sleep(2)
send_command('F')


# ---------------- Main Detection and Control Loop ----------------
try:
    while True:
        # Capture a frame and convert it to grayscale for tag detection.
        frame = picam2.capture_array()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detections = detector.detect(gray)

        draw_ui(frame)

        # Select the largest detected tag whose centre is in the
        # central 60% of the image.
        best_tag = None
        best_size = 0

        for tag in detections:
            cx = tag.center[0]
            size = cv2.norm(tag.corners[0] - tag.corners[2])

            if (
                center_zone_start <= cx <= center_zone_end
                and size > best_size
            ):
                best_size = size
                best_tag = tag

        if best_tag is not None:
            tag_id = best_tag.tag_id
            cx = best_tag.center[0]
            cy = best_tag.center[1]

            # Apply the cooldown before repeating an action for the same tag.
            if (
                tag_id != last_tag_id
                or time.time() - last_action_time > cooldown
            ):
                if tag_id == 0:
                    send_command('L')

                elif tag_id == 1:
                    send_command('R')

                elif tag_id == 2:
                    # Keep the robot aligned using the tag's horizontal
                    # position within the central detection zone.
                    if cx < center_zone_start + 40:
                        send_command('L')
                    elif cx > center_zone_end - 40:
                        send_command('R')
                    else:
                        send_command('F')

                elif tag_id == 3:
                    send_command('B')

                elif tag_id == 4:
                    send_command('S')
                    print("[🛑] Stop tag detected.")
                    break

                last_tag_id = tag_id
                last_action_time = time.time()

            # Draw the detected AprilTag outline and its ID.
            for i in range(4):
                pt1 = tuple(best_tag.corners[i - 1].astype(int))
                pt2 = tuple(best_tag.corners[i].astype(int))
                cv2.line(frame, pt1, pt2, (255, 0, 0), 2)

            cv2.putText(
                frame,
                f"ID {tag_id}",
                (int(cx), int(cy)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2
            )

        else:
            # Fail-safe: stop the robot when no eligible tag is visible.
            send_command('S')
            last_tag_id = None

        # Display the camera preview and allow the operator to quit with q.
        cv2.imshow("Bot Cam", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\n[CTRL+C] Exit")

finally:
    # Send a stop command and release connected hardware and GUI resources.
    send_command('S')
    ser.close()
    picam2.stop()
    cv2.destroyAllWindows()
    print("[✔] Done. Safe shutdown.")
