import cv2 as cv


from controllers.pid_controller import PIDController
from controllers.lane_detector import LaneDetector
from controllers.serial_comm import SerialCommunicator
from processing.video_processor import VideoProcessor
from utils.display import create_control_window, get_trackbar_values, draw_overlays

# Configurações
FRAME_WIDTH = int(1920 / 4)
FRAME_HEIGHT = int(1080 / 4)
FRAME_CENTER = FRAME_WIDTH // 2
ROI_START = 200
ROI_END = 220
NUM_LINES = 10
ANALYZE_LANE = "RIGHT"  # ou "LEFT"

TARGET_CENTER_DISTANCE = 100
KP = 0.3
KI = 0.005
KD = 0.01
MIN_OUTPUT = -32
MAX_OUTPUT = 32

VIDEO_SOURCE = "test_videos/teste1.mp4"
SEND_DATA = False
COM_PORT = 'COM13'

# Inicializações
create_control_window()
pid = PIDController(TARGET_CENTER_DISTANCE, KP, KI, KD, MIN_OUTPUT, MAX_OUTPUT)
lane_detector = LaneDetector(ROI_START, ROI_END)
serial_comm = SerialCommunicator(COM_PORT, send_interval=0.1, send_data=SEND_DATA)
video_proc = VideoProcessor(VIDEO_SOURCE, FRAME_WIDTH, FRAME_HEIGHT)

data_to_send = [255, 180, 0, 0, 0, 0, 0, 0, 0]

try:
    while True:
        frame, fps = video_proc.get_frame()
        canny_1, canny_2, speed = get_trackbar_values()

        # Pré-processamento
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray, (5, 5), 0)
        edges = cv.Canny(blur, canny_1, canny_2)
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (4, 4))
        edges = cv.morphologyEx(edges, cv.MORPH_CLOSE, kernel)

        # Extrair ROI
        roi = edges[ROI_START:ROI_END, 0:480]
        interval = max(1, round((ROI_END - ROI_START) / NUM_LINES))
        avg_left, avg_right = lane_detector.calculate_center_distance(roi, NUM_LINES, interval)

        if ANALYZE_LANE == "RIGHT":
            if avg_right != float('inf'):
                direction = round(pid.calculate(avg_right))
                data_to_send[1] = direction
        elif ANALYZE_LANE == "LEFT":
            if avg_left != float('inf'):
                direction = round(pid.calculate(avg_left))
                data_to_send[1] = direction

        # Atualizar velocidade
        data_to_send[0] = speed

        # Envio serial
        serial_comm.send(data_to_send)

        # Overlay e exibição
        frame = draw_overlays(frame, (ROI_START, ROI_END), (avg_left, avg_right), fps, FRAME_CENTER)
        cv.imshow("Video Output", frame)
        cv.imshow("Edges", edges)
        cv.imshow("ROI", roi)

        if cv.waitKey(1) == ord('q'):
            break
except Exception as e:
    print("Erro:", e)
finally:
    serial_comm.close()
    video_proc.release()
    cv.destroyAllWindows()
