import time
import serial

class SerialCommunicator:
    def __init__(self, com_port, baud_rate=115200, send_interval=0.1, send_data=False):
        self.send_data = send_data
        self.send_interval = send_interval
        self.last_send_time = time.time()
        self.com_port = com_port
        self.serial_port = serial.Serial(com_port, baud_rate) if send_data else None

    def send(self, data):
        if (time.time() - self.last_send_time) >= self.send_interval:
            data_string = ",".join(str(d) for d in data) + ",#"
            print(data_string)
            if self.send_data and self.serial_port:
                self.serial_port.write(data_string.encode())
            self.last_send_time = time.time()

    def close(self):
        if self.send_data and self.serial_port:
            self.serial_port.close()
