import cv2 as cv

def create_control_window():
    cv.namedWindow('Controls')
    cv.createTrackbar('canny_1', 'Controls', 20, 300, lambda x: None)
    cv.createTrackbar('canny_2', 'Controls', 152, 400, lambda x: None)
    cv.createTrackbar('speed', 'Controls', 0, 255, lambda x: None)

def get_trackbar_values():
    canny_1 = cv.getTrackbarPos('canny_1', 'Controls')
    canny_2 = cv.getTrackbarPos('canny_2', 'Controls')
    speed = cv.getTrackbarPos('speed', 'Controls')
    return canny_1, canny_2, speed

def draw_overlays(frame, roi_coords, distances, fps, frame_center):
    font = cv.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_color = (0, 0, 255)
    thickness = 1

    avg_left, avg_right = distances
    roi_start, roi_end = roi_coords

    # Desenhar retângulo para o lado direito
    if not (avg_right == float('inf')):
        top_left = (frame_center, roi_start)
        bottom_right = (int(avg_right) + frame_center, roi_end)
        cv.rectangle(frame, top_left, bottom_right, (255, 0, 0), -1)
        cv.putText(frame, f"{avg_right:.1f}", (frame_center + 30, roi_start - 10),
                   font, font_scale, font_color, thickness, cv.LINE_AA)

    # Desenhar retângulo para o lado esquerdo
    if not (avg_left == float('inf')):
        top_left = (frame_center - int(avg_left), roi_start)
        bottom_right = (frame_center, roi_end)
        cv.rectangle(frame, top_left, bottom_right, (0, 0, 255), -1)
        cv.putText(frame, f"{avg_left:.1f}", (frame_center - 60, roi_start - 10),
                   font, font_scale, font_color, thickness, cv.LINE_AA)

    # Linha central e FPS
    cv.line(frame, (frame_center, 0), (frame_center, frame.shape[0]), (0, 255, 255), 2)
    cv.putText(frame, f"FPS: {fps:.2f}", (10, 30), font, 0.7, (0, 255, 0), 2, cv.LINE_AA)

    return frame
