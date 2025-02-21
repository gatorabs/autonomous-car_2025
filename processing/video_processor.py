import cv2 as cv
import time

class VideoProcessor:
    def __init__(self, video_source, frame_width, frame_height):
        self.cap = cv.VideoCapture(video_source)
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.prev_time = time.time()

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            raise Exception("Erro ao capturar frame")
        # Redimensionar
        frame = cv.resize(frame, (self.frame_width, self.frame_height))
        # Cálculo de FPS
        current_time = time.time()
        fps = 1.0 / (current_time - self.prev_time)
        self.prev_time = current_time
        return frame, fps

    def release(self):
        self.cap.release()
