import numpy as np
import cv2 as cv


def bird_eye(roi):
    # Pontos para transformação de perspectiva na ROI
    src_points = np.float32([[0, 0], [roi.shape[1], 0],
                             [0, roi.shape[0]], [roi.shape[1], roi.shape[0]]])

    dst_points = np.float32([[0, 0], [roi.shape[1], 0],
                             [roi.shape[1] * 0.2, roi.shape[0]], [roi.shape[1] * 0.8, roi.shape[0]]])

    M = cv.getPerspectiveTransform(src_points, dst_points)

    warped_roi = cv.warpPerspective(roi, M, (roi.shape[1], roi.shape[0]))

    return warped_roi
