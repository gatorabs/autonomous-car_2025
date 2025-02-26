# main.py (trecho relevante)
import cv2 as cv
from controllers.pid_controller import PIDController
from controllers.lane_detector import LaneDetector
from controllers.serial_comm import SerialCommunicator
from processing.video_processor import VideoProcessor
from utils.display import draw_overlays, create_main_window
from utils.real_time_trackbars import create_control_window, get_trackbar_values
from processing.warp_perspective_processor import bird_eye
from utils.buttons import start_tkinter_thread, controls
from processing.object_detection_processor import ObjectDetector

# ========== Configurações ========== #
FRAME_WIDTH = int(1920 / 4)
FRAME_HEIGHT = int(1080 / 4)
FRAME_CENTER = FRAME_WIDTH // 2

ROI_START = 200
ROI_END = 220
ROI_X_START = 100
ROI_X_END = 380

NUM_LINES = 10
ANALYZE_LANE = 1  # 0 para "LEFT"

SHOW_FPS = True
SHOW_VIDEO = controls["SHOW_VIDEO"] = True
SHOW_EDGES = controls["SHOW_EDGES"] = True
SHOW_ROI = controls["SHOW_ROI"] = True

TARGET_CENTER_DISTANCE = 80

KP = 0.3
KI = 0.005
KD = 0.01

MIN_OUTPUT = -32
MAX_OUTPUT = 32

VIDEO_SOURCE = "test_videos/teste1.mp4"
SEND_DATA = False
COM_PORT = 'COM13'

create_control_window()
start_tkinter_thread()

pid = PIDController(TARGET_CENTER_DISTANCE, KP, KI, KD, MIN_OUTPUT, MAX_OUTPUT)
lane_detector = LaneDetector(ROI_START, ROI_END)
serial_comm = SerialCommunicator(COM_PORT, send_interval=0.1, send_data=SEND_DATA)
video_proc = VideoProcessor(VIDEO_SOURCE, FRAME_WIDTH, FRAME_HEIGHT)

#velocidade | angulacao | pessoa | semaforo
data_to_send = [255, 180, 0, 0, 0, 0, 0, 0, 0]


object_detector = ObjectDetector(data_to_send, camera_source=0)
object_detector.start()


morph_kernel = cv.getStructuringElement(cv.MORPH_RECT, (4, 4))

try:
    while True:
        frame, fps = video_proc.get_frame()
        canny_1, canny_2, speed, side = get_trackbar_values()

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray, (5, 5), 0)
        edges = cv.Canny(blur, canny_1, canny_2)
        edges = cv.morphologyEx(edges, cv.MORPH_CLOSE, morph_kernel)

        roi = edges[ROI_START:ROI_END, ROI_X_START:ROI_X_END]
        warped_roi = bird_eye(roi)
        interval = max(1, round((ROI_END - ROI_START) / NUM_LINES))
        avg_left, avg_right = lane_detector.calculate_center_distance(warped_roi, NUM_LINES, interval)

        ANALYZE_LANE = side
        data_to_send[0] = speed
        if ANALYZE_LANE == 1:
            if avg_right != float('inf'):
                direction = round(pid.calculate(avg_right))
                data_to_send[1] = direction
        elif ANALYZE_LANE == 0:
            if avg_left != float('inf'):
                direction = round(pid.calculate(avg_left))
                data_to_send[1] = direction

        serial_comm.send(data_to_send)
        frame = draw_overlays(frame, (ROI_START, ROI_END), (ROI_X_START, ROI_X_END),
                              (avg_left, avg_right), fps, SHOW_FPS, FRAME_CENTER)
        main_display = create_main_window(frame, edges, warped_roi,
                                          show_video=controls["SHOW_VIDEO"],
                                          show_edges=controls["SHOW_EDGES"],
                                          show_roi=controls["SHOW_ROI"])
        cv.imshow("Main Display", main_display)
        if cv.waitKey(1) == ord('q'):
            break

except Exception as e:
    print("Erro:", e)
finally:
    object_detector.stop()
    object_detector.join()
    serial_comm.close()
    video_proc.release()
    cv.destroyAllWindows()
