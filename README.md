# 🤖 Autonomous Campus Delivery Bot

An autonomous indoor delivery robot designed to navigate using **AprilTag visual markers**, detect nearby obstacles using an **ultrasonic sensor**, and coordinate movement through a **hierarchical control architecture**.

The system uses a **Raspberry Pi 5** for camera-based vision and high-level decision-making, while an **Arduino Uno** handles motor control and obstacle monitoring.

Developed during the **Kalam Pragati MakeX Internship 2025 – Autonomous Robotics**, organised by **ERA Foundation** in collaboration with **Dr. A.P.J. Abdul Kalam Technical University (AKTU), Lucknow**.

![Autonomous Campus Delivery Bot](media/images/robot_front.jpg)

---

## 📌 Project Overview

| Item | Details |
|---|---|
| Project | Autonomous Campus Delivery Bot |
| Team | AVENGERS (Team 10) |
| Internship | Kalam Pragati MakeX – Autonomous Robotics |
| Duration | 4 August 2025 – 1 September 2025 |
| Navigation | AprilTag-based visual navigation |
| High-level controller | Raspberry Pi 5 |
| Camera | Raspberry Pi Camera Module 2 |
| Low-level controller | Arduino Uno |
| Motor driver | L298N |
| Drive system | Four DC motors (4WD chassis) |
| Obstacle detection | HC-SR04 ultrasonic sensor |

## ❗ Problem Statement

Delivering parcels and documents across a campus often relies on manual transportation. This can be time-consuming, difficult to scale, and inefficient.

The project explores an autonomous delivery solution capable of navigating predefined indoor routes, detecting obstacles, and transporting items to designated locations.

The original problem statement is available in [docs/problem_statement.md](docs/problem_statement.md).

## 💡 Solution Overview

The robot combines camera-based navigation with a separate embedded motor-control system.

- **AprilTag-based navigation:** The Raspberry Pi camera detects AprilTag markers placed along the route. Detected tag IDs are mapped to predefined movement commands.
- **Hierarchical control:** The Raspberry Pi handles image processing and navigation decisions, then communicates commands to the Arduino over USB serial.
- **Motor control:** The Arduino processes movement commands and controls the L298N motor driver.
- **Obstacle monitoring:** The Arduino monitors the HC-SR04 ultrasonic sensor and can stop the motors when an obstacle is detected within the configured safety distance.
- **Fail-safe behaviour:** The system is designed to stop when no valid navigation instruction is available.

Example navigation commands:

`FORWARD` · `LEFT` · `RIGHT` · `STOP`

### Why AprilTags?

AprilTags provide identifiable visual markers that can be used for navigation along predefined indoor routes.

Compared with line-following systems, marker-based navigation does not depend on a continuously visible floor line. Compared with LiDAR-based SLAM, it offers a simpler approach for structured environments where navigation markers can be installed.

## 🧠 System Architecture

![System Block Diagram](hardware/block_diagram.png)

The system follows a hierarchical control approach:

1. Capture images using the Raspberry Pi camera.
2. Detect and identify AprilTag markers.
3. Map the detected tag ID to a movement command.
4. Transmit the command to the Arduino over serial communication.
5. Check obstacle distance and apply the motor-control safety logic.
6. Execute the permitted movement and repeat the navigation cycle.

Detailed explanation: [docs/architecture.md](docs/architecture.md).

## 🔌 Hardware Components

| Component | Function |
|---|---|
| Raspberry Pi 5 | Image processing and navigation decisions |
| Raspberry Pi Camera Module 2 | Image acquisition |
| Arduino Uno | Motor control and obstacle monitoring |
| L298N motor driver | DC motor control |
| 4WD acrylic chassis | Mechanical platform |
| Four DC gear motors | Robot movement |
| HC-SR04 ultrasonic sensor | Obstacle detection |
| 11.1 V 3S LiPo battery | Motor power supply |
| Power bank | Raspberry Pi power supply |

**Hardware documentation:** [Bill of Materials](hardware/bill_of_materials.md) · [Wiring and Pinout](hardware/wiring_and_pinout.md)

![Circuit Diagram](hardware/circuit_diagram.png)

## 💻 Software and Technologies

**Raspberry Pi – Python**
- Python
- OpenCV
- pupil-apriltags
- PySerial
- Picamera2

**Arduino – Embedded C/C++**
- Arduino programming environment
- Serial command handling
- L298N motor-control routines
- HC-SR04 distance measurement
- Obstacle-response logic

### Running the Project

**1. Upload the Arduino firmware**

Open the Arduino sketch in Arduino IDE:

`firmware/arduino_motor_controller/arduino_motor_controller.ino`

Select the appropriate Arduino Uno board and port, then upload the firmware.

**2. Set up the Raspberry Pi software**

```bash
cd software/raspberry_pi

pip install -r requirements.txt

python3 main.py
```

Picamera2 may need to be installed separately through Raspberry Pi OS:

```bash
sudo apt install python3-picamera2
```

**3. Configure serial communication**

The serial device is commonly `/dev/ttyACM0`, but the actual port depends on the connected board and operating system. Update the configuration in `config.py` if necessary.

Refer to the [Raspberry Pi software guide](software/raspberry_pi/README.md) and [Arduino firmware guide](firmware/arduino_motor_controller/README.md) before running the complete system.

## 📊 Testing and Results

The project involves testing the robot's sensing, navigation, and movement-control subsystems.

| Test Area | Evaluation |
|---|---|
| Ultrasonic sensing | Distance measurement and obstacle detection |
| Obstacle response | Motor stopping at the configured safety threshold |
| AprilTag detection | Marker recognition under different lighting conditions |
| Serial communication | Command transfer between Raspberry Pi and Arduino |
| Motor calibration | PWM adjustment for controlled movement |

Detailed measurements and test observations: [docs/calibration_and_results.md](docs/calibration_and_results.md).

## 🎥 Project Demonstration

- **Project photographs:** [media/images/](media/images/)
- **AprilTag detection screenshots:** [media/screenshots/](media/screenshots/)

## 🚀 Future Scope

Potential improvements and extensions include:

- GPS and IMU integration for outdoor navigation.
- Web-based monitoring and parcel registration.
- QR-code or OCR-based parcel identification.
- SMS-based delivery notifications.
- LiDAR integration and SLAM-based navigation.
- A* path planning and dynamic route selection.
- Recipient-location-based delivery.

These are proposed extensions and are not presented as completed features of the current prototype.

More details: [docs/future_scope.md](docs/future_scope.md).

## 👥 Team AVENGERS – Team 10

- Shashank Rai
- Ajay Kumar
- **Aman Shukla**
- Sujal Prajapati
- Akhil Dalal
- Abhay Yadav

## 🏅 Internship Recognition

The project was developed as part of the Kalam Pragati MakeX Internship 2025 – Autonomous Robotics.

Internship certificate and event documentation: [internship/](internship/).

## 📄 Project Documentation

- [Internship Report](docs/Internship_Report.pdf)
- [Problem Statement](docs/problem_statement.md)
- [System Architecture](docs/architecture.md)
- [Calibration and Results](docs/calibration_and_results.md)
- [Future Scope](docs/future_scope.md)

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgements

Sincere thanks to the **AKTU Central Training & Placement Cell**, **ERA Foundation**, and the **Kalam Pragati MakeX internship mentors** for their guidance and support throughout the programme.

---

*Designing, building, testing, and learning through practical robotics and embedded systems.*
