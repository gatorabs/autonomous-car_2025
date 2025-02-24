#ifndef MOTOR_CONTROL_H
#define MOTOR_CONTROL_H

#include <Arduino.h>

#define MOTOR_A_PWM_PIN 5   
#define MOTOR_A_DIR_PIN 4   

#define MOTOR_B_PWM_PIN 6   
#define MOTOR_B_DIR_PIN 7   

void setupMotors();
void setMotorSpeed(int motorA_speed, int motorB_speed);
void brakeMotors();

#endif
