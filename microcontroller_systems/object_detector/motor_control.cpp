#include "motor_control.h"

void setupMotors() {
    pinMode(MOTOR_A_PWM_PIN, OUTPUT);
    pinMode(MOTOR_A_DIR_PIN, OUTPUT);
    pinMode(MOTOR_B_PWM_PIN, OUTPUT);
    pinMode(MOTOR_B_DIR_PIN, OUTPUT);
}

void setMotorSpeed(int motorA_speed, int motorB_speed) {

    // Motor A
    if (motorA_speed >= 0) {
        digitalWrite(MOTOR_A_DIR_PIN, HIGH);
        analogWrite(MOTOR_A_PWM_PIN, motorA_speed);
    } else {
        digitalWrite(MOTOR_A_DIR_PIN, LOW);
        analogWrite(MOTOR_A_PWM_PIN, -motorA_speed);
    }

    // Motor B
    if (motorB_speed >= 0) {
        digitalWrite(MOTOR_B_DIR_PIN, HIGH);
        analogWrite(MOTOR_B_PWM_PIN, motorB_speed);
    } else {
        digitalWrite(MOTOR_B_DIR_PIN, LOW);
        analogWrite(MOTOR_B_PWM_PIN, -motorB_speed);
    }
}

void brakeMotors() {
    analogWrite(MOTOR_A_PWM_PIN, 0);
    analogWrite(MOTOR_B_PWM_PIN, 0);
}
