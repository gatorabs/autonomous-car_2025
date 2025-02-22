import numpy as np

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

        # Define limites seguros para iteração
        start = max(0, center_y - (num_lines // 2) * interval)
        end = min(height, center_y + (num_lines // 2) * interval)

        for i in range(start, end, interval):
            row = img[i, :]

            right_indices = np.where(row[center_x:] >= 50)[0]
            if right_indices.size > 0:
                right_distances.append(right_indices[0])

            left_indices = np.where(row[:center_x+1] >= 50)[0]
            if left_indices.size > 0:

                left_distances.append(center_x - left_indices[-1])

        avg_left = np.mean(left_distances) if left_distances else float('inf')
        avg_right = np.mean(right_distances) if right_distances else float('inf')

        return avg_left, avg_right
