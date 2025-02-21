import time

class PIDController:
    def __init__(self, set_point, kp, ki, kd, min_output, max_output):
        self.set_point = set_point
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.min_output = min_output
        self.max_output = max_output
        self.integral = 0
        self.last_error = 0
        self.last_time = time.time()

    def calculate(self, input_val):
        now = time.time()
        delta_time = now - self.last_time
        if delta_time <= 0:
            delta_time = 1e-3

        error = self.set_point - input_val

        # Termo proporcional
        p = self.kp * error

        # Termo integral com anti-windup
        self.integral += self.ki * error * delta_time
        self.integral = max(min(self.integral, self.max_output), self.min_output)

        # Termo derivativo
        d = self.kd * (error - self.last_error) / delta_time

        output = p + self.integral + d
        output = max(min(output, self.max_output), self.min_output)

        self.last_error = error
        self.last_time = now

        return output
