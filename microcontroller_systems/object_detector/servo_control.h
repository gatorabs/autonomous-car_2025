#ifndef SERVO_CONTROL_H
#define SERVO_CONTROL_H

#include <Arduino.h>
#include <Servo.h>

#define SERVO_PIN 9

void setupServo();
void setServoAngle(int angle);

#endif
