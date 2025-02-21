import numpy as np
import math

class LaneDetector:
    def __init__(self, roi_start, roi_end):
        self.roi_start = roi_start
        self.roi_end = roi_end

    def calculate_center_distance(self, img, num_lines, interval):
        height, width = img.shape
        center_y = height // 2
        center_x = width // 2

        left_distances = []
        right_distances = []

        for i in range(center_y - (num_lines // 2) * interval, center_y + (num_lines // 2) * interval, interval):
            if i < 0 or i >= height:
                continue

            # Lado direito
            for x_right in range(center_x, width):
                if img[i, x_right] >= 50:
                    right_distances.append(x_right - center_x)
                    break

            # Lado esquerdo
            for x_left in range(center_x, -1, -1):
                if img[i, x_left] >= 50:
                    left_distances.append(center_x - x_left)
                    break

        avg_left = np.mean(left_distances) if left_distances else float('inf')
        avg_right = np.mean(right_distances) if right_distances else float('inf')

        return avg_left, avg_right
