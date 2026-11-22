/*
 * Autonomous Campus Delivery Bot - Arduino Motor Controller
 * Kalam Pragati MakeX Internship 2025 | Team AVENGERS (Team 10)
 *
 * Receives single-character commands from the Raspberry Pi over USB serial
 * (9600 baud): F = forward, B = backward, L = left, R = right, S = stop.
 * Reads an HC-SR04 ultrasonic sensor, slows down near obstacles and runs
 * an avoidance routine when an obstacle is too close.
 *
 * Hardware: Arduino Uno, L298N motor driver, HC-SR04 ultrasonic sensor,
 * and buzzer.
 */

// =====================
// Pin Definitions
// =====================
const int ENA = 5;
const int IN1 = 7;
const int IN2 = 8;
const int IN3 = 11;
const int IN4 = 4;
const int ENB = 6;
const int trigPin = 9;
const int echoPin = 10;
#define BUZZER_PIN 2

// =====================
// Motor Speeds
// =====================
const int fullSpeed = 255;
const int slowSpeed = 150;
const int stopSpeed = 0;

// =====================
// Distance Thresholds
// =====================
const int stopDist = 15;
const int slowDist = 30;

// =====================
// Internal States
// =====================
char currentCommand = 'S';
bool inAvoidanceMode = false;
bool tryLeftNext = false;

// =====================
// Setup
// =====================
void setup() {
  Serial.begin(9600);

  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);

  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  stopMotors();
  buzzAlive();
}

// =====================
// Main Loop
// =====================
void loop() {
  if (Serial.available()) {
    char cmd = toupper(Serial.read());

    if (cmd == 'F' || cmd == 'B' || cmd == 'L' ||
        cmd == 'R' || cmd == 'S') {
      currentCommand = cmd;
      inAvoidanceMode = false;
    }
  }

  int dist = readAverageUltrasonic();

  if (inAvoidanceMode) {
    handleObstacleAvoidance();
    return;
  }

  if (currentCommand == 'F') {
    if (dist < stopDist) {
      Serial.println("Obstacle too close! Avoiding.");
      inAvoidanceMode = true;
    } else if (dist < slowDist) {
      slowMove('F');
    } else {
      fullMove('F');
    }
  } else if (currentCommand == 'B') {
    fullMove('B');
  } else if (currentCommand == 'L' || currentCommand == 'R') {
    turn(currentCommand);
  } else if (currentCommand == 'S') {
    stopMotors();
  }

  delay(50);
}

// =====================
// Motor Movement
// =====================
void stopMotors() {
  analogWrite(ENA, stopSpeed);
  analogWrite(ENB, stopSpeed);

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

void fullMove(char dir) {
  analogWrite(ENA, fullSpeed);
  analogWrite(ENB, fullSpeed);
  setMotorDir(dir);
}

void slowMove(char dir) {
  analogWrite(ENA, slowSpeed);
  analogWrite(ENB, slowSpeed);
  setMotorDir(dir);
}

void turn(char dir) {
  analogWrite(ENA, fullSpeed);
  analogWrite(ENB, fullSpeed);

  if (dir == 'L') {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
  } else if (dir == 'R') {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
  }

  delay(500);  // Execute a sharp turn.
  stopMotors();
}

// =====================
// Obstacle Avoidance
// =====================
void handleObstacleAvoidance() {
  stopMotors();
  delay(200);

  slowMove('B');
  delay(400);

  stopMotors();
  delay(200);

  if (tryLeftNext) {
    turn('L');
  } else {
    turn('R');
  }

  delay(500);
  stopMotors();
  delay(200);

  tryLeftNext = !tryLeftNext;

  int dist = readAverageUltrasonic();

  if (dist > slowDist) {
    fullMove('F');
    delay(300);
    inAvoidanceMode = false;
  }
}

// =====================
// Motor Direction Helper
// =====================
void setMotorDir(char dir) {
  if (dir == 'F') {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
  } else if (dir == 'B') {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
  }
}

// =====================
// Ultrasonic Sensor
// =====================
int readUltrasonic() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000);

  if (duration == 0) {
    return 999;
  }

  int dist = duration * 0.034 / 2;
  return dist;
}

int readAverageUltrasonic() {
  int sum = 0;
  int count = 0;

  for (int i = 0; i < 5; i++) {
    int d = readUltrasonic();

    if (d > 2 && d < 400) {
      sum += d;
      count++;
    }

    delay(10);
  }

  return (count > 0) ? sum / count : 999;
}

// =====================
// Buzzer Feedback
// =====================
void beep(int ms) {
  digitalWrite(BUZZER_PIN, HIGH);
  delay(ms);
  digitalWrite(BUZZER_PIN, LOW);
}

void buzzAlive() {
  for (int i = 0; i < 3; i++) {
    beep(100);
    delay(100);
  }
}
