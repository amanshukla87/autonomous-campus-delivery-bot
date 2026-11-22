# AprilTags Used

- **Family:** `tag36h11`
- **Printed size:** 136.58 mm

| Tag ID | Action | File |
|---|---|---|
| 0 | Turn Left | `tag36h11_id0_turn_left.png` |
| 1 | Turn Right | `tag36h11_id1_turn_right.png` |
| 2 | Align Forward | `tag36h11_id2_forward.png` |
| 3 | Move Backward | `tag36h11_id3_backward.png` |
| 4 | Stop & Exit | `tag36h11_id4_stop.png` |

Only tags whose centre falls within the central 60% of the camera frame are considered by the Raspberry Pi navigation script. When multiple eligible tags are detected, the largest is selected.

The command mapping in this document matches `software/raspberry_pi/main.py`. Printable tag image files should be added to this directory when the exact tag36h11 marker images are available.
