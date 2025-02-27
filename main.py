# main.py
import multiprocessing as mp
import cv2 as cv
import time

# Importações dos módulos do projeto
from controllers.pid_controller import PIDController
from controllers.lane_detector import LaneDetector
from controllers.serial_comm import SerialCommunicator
from processing.video_processor import VideoProcessor
from processing.warp_perspective_processor import bird_eye
from processing.object_detection_processor import ObjectDetector
from utils.display import draw_overlays, create_main_window
from utils.real_time_trackbars import create_control_window, get_trackbar_values
from utils.buttons import start_tkinter_thread, controls  # observe que o módulo está com o nome "bottons"


def lane_detection_process(lane_queue):
    """Processo para detecção de faixas (interface, trackbars e botões)."""
    # Configurações de vídeo e ROI
    FRAME_WIDTH = int(1920 / 4)
    FRAME_HEIGHT = int(1080 / 4)
    FRAME_CENTER = FRAME_WIDTH // 2
    ROI_START = 200
    ROI_END = 220
    ROI_X_START = 100
    ROI_X_END = 380
    NUM_LINES = 10
    TARGET_CENTER_DISTANCE = 80

    # Parâmetros do PID
    KP = 0.3
    KI = 0.005
    KD = 0.01
    MIN_OUTPUT = -32
    MAX_OUTPUT = 32

    VIDEO_SOURCE = 1
    # Cria a interface de controle
    create_control_window()
    start_tkinter_thread()

    pid = PIDController(TARGET_CENTER_DISTANCE, KP, KI, KD, MIN_OUTPUT, MAX_OUTPUT)
    lane_detector = LaneDetector(ROI_START, ROI_END)
    video_proc = VideoProcessor(VIDEO_SOURCE, FRAME_WIDTH, FRAME_HEIGHT)
    morph_kernel = cv.getStructuringElement(cv.MORPH_RECT, (4, 4))

    try:
        while True:
            frame, fps = video_proc.get_frame()
            # Obtém os valores dos trackbars
            canny_1, canny_2, speed, side = get_trackbar_values()

            # Processamento de imagem para detecção de faixas
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            blur = cv.GaussianBlur(gray, (5, 5), 0)
            edges = cv.Canny(blur, canny_1, canny_2)
            edges = cv.morphologyEx(edges, cv.MORPH_CLOSE, morph_kernel)

            roi = edges[ROI_START:ROI_END, ROI_X_START:ROI_X_END]
            warped_roi = bird_eye(roi)
            interval = max(1, round((ROI_END - ROI_START) / NUM_LINES))
            avg_left, avg_right = lane_detector.calculate_center_distance(warped_roi, NUM_LINES, interval)

            # Calcula o ângulo (direção) usando o PID
            direction = 0
            if side == 1:
                if avg_right != float('inf'):
                    direction = round(pid.calculate(avg_right))
            else:
                if avg_left != float('inf'):
                    direction = round(pid.calculate(avg_left))

            # Exibição – sobrepõe informações e junta janelas
            frame_display = draw_overlays(frame, (ROI_START, ROI_END),
                                          (ROI_X_START, ROI_X_END),
                                          (avg_left, avg_right),
                                          fps,
                                          controls.get("SHOW_FPS", True),
                                          FRAME_CENTER)
            main_display = create_main_window(frame_display, edges, warped_roi,
                                              show_video=controls.get("SHOW_VIDEO", True),
                                              show_edges=controls.get("SHOW_EDGES", True),
                                              show_roi=controls.get("SHOW_ROI", True),
                                              )
            cv.imshow("Lane Detection", main_display)
            if cv.waitKey(1) == ord('q'):
                break

            # Envia dados para o processo de envio (fila)
            lane_data = {"speed": speed, "direction": direction}
            if not lane_queue.full():
                lane_queue.put(lane_data)
    except Exception as e:
        print("Lane Detection Error:", e)
    finally:
        video_proc.release()
        cv.destroyWindow("Lane Detection")


def object_detection_process(object_queue):
    """Processo para detecção de objetos (pessoas e semáforos)."""
    # Instancia o objeto da classe ObjectDetector (do arquivo object_detection_processor)
    serial_data = [0, 0, 0]  # Usando uma lista para armazenar os dados
    object_detector = ObjectDetector(serial_data)

    # Inicia o processo de detecção de objetos
    object_detector.start()

    try:
        while True:
            # Atualiza os dados de detecção na fila de objetos
            object_data = {"person": serial_data[2], "semaforo": 0}  # Aqui, semáforo é mockado
            if not object_queue.full():
                object_queue.put(object_data)

            # Remove a tentativa de exibir a janela aqui, pois o próprio ObjectDetector já o faz.
            time.sleep(0.05)  # Pausa para evitar sobrecarga

    except Exception as e:
        print("Object Detection Error:", e)
    finally:
        object_detector.stop()  # Parando a detecção
        cv.destroyAllWindows()


def data_sender_process(lane_queue, object_queue):
    """Processo para envio dos dados combinados (ângulo, velocidade, detecção de pessoa e semáforo) via serial (COM13)."""
    SEND_DATA = False  # Alterar para True para enviar via serial
    COM_PORT = 'COM13'
    serial_comm = SerialCommunicator(COM_PORT, send_data=SEND_DATA)
    # Dados padrão iniciais
    lane_data = {"speed": 255, "direction": 180}
    obj_data = {"person": 0, "semaforo": 0}
    try:
        while True:
            # Atualiza dados de lane, se disponíveis
            if not lane_queue.empty():
                lane_data = lane_queue.get()
            # Atualiza dados de objetos, se disponíveis
            if not object_queue.empty():
                obj_data = object_queue.get()
            # Combina os dados em um pacote (exemplo: [speed, direction, person, semáforo])
            data_to_send = [lane_data.get("speed", 255),
                            lane_data.get("direction", 180),
                            obj_data.get("person", 0),
                            obj_data.get("semaforo", 0)]
            serial_comm.send(data_to_send)
            time.sleep(0.05)  # Ajuste o intervalo conforme necessário
    except Exception as e:
        print("Data Sender Error:", e)
    finally:
        serial_comm.close()


if __name__ == '__main__':
    mp.set_start_method('spawn')
    lane_queue = mp.Queue(maxsize=10)
    object_queue = mp.Queue(maxsize=10)


    lane_process = mp.Process(target=lane_detection_process, args=(lane_queue,))
    object_process = mp.Process(target=object_detection_process, args=(object_queue,))
    sender_process = mp.Process(target=data_sender_process, args=(lane_queue, object_queue,))

    # Inicia os processos
    lane_process.start()
    object_process.start()
    sender_process.start()

    try:
        lane_process.join()
        object_process.join()
        sender_process.join()
    except KeyboardInterrupt:
        print("Interrompido pelo usuário. Encerrando processos...")
        lane_process.terminate()
        object_process.terminate()
        sender_process.terminate()
