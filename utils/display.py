import cv2 as cv
import numpy as np


def draw_overlays(frame, roi_coords, roi_x_coords, distances, fps, show_fps, frame_center):
    font = cv.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_color = (0, 255, 255)
    thickness = 1

    avg_left, avg_right = distances
    roi_start, roi_end = roi_coords
    roi_x_start, roi_x_end = roi_x_coords

    # Criar uma cópia do frame para desenhar a sobreposição
    overlay = frame.copy()


    overlay_color = (0, 255, 0)  # Verde
    alpha = 0.3

    # Desenhar retângulo semi-transparente sobre o ROI
    cv.rectangle(overlay, (roi_x_start, roi_start), (roi_x_end, roi_end), overlay_color, -1)


    cv.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    # Desenhar retângulo para o lado direito
    if avg_right != float('inf'):
        top_left = (frame_center, roi_start)
        bottom_right = (int(avg_right) + frame_center, roi_end)
        cv.rectangle(frame, top_left, bottom_right, (255, 0, 0), 2)
        cv.putText(frame, f"{avg_right:.1f}", (frame_center + 30, roi_start - 10),
                   font, font_scale, font_color, thickness, cv.LINE_AA)

    # Desenhar retângulo para o lado esquerdo
    if avg_left != float('inf'):
        top_left = (frame_center - int(avg_left), roi_start)
        bottom_right = (frame_center, roi_end)
        cv.rectangle(frame, top_left, bottom_right, (0, 255, 255), 2)
        cv.putText(frame, f"{avg_left:.1f}", (frame_center - 60, roi_start - 10),
                   font, font_scale, font_color, thickness, cv.LINE_AA)

    # Linha central
    cv.line(frame, (frame_center, 0), (frame_center, frame.shape[0]), (255, 255, 255), 2)
    # Exibir FPS
    if show_fps:
        cv.putText(frame, f"FPS: {fps:.2f}", (10, 30), font, 0.7, (0, 255, 0), 2, cv.LINE_AA)
    else:
        print(f"FPS: {fps}")
    return frame


def create_main_window(video_img, edges_img, roi_img, show_video=True, show_edges=True, show_roi=True):

    reference = None
    for img in [video_img, edges_img, roi_img]:
        if img is not None:
            reference = img
            break
    if reference is None:
        reference = np.zeros((480, 640, 3), dtype=np.uint8)  # Criar um espaço em branco se não houver referência

    height, width, _ = reference.shape
    blank = np.zeros((height, width, 3), dtype=np.uint8)

    # Se a flag estiver desativada, usamos a imagem em branco
    video_disp = video_img if show_video and video_img is not None else blank
    edges_disp = edges_img if show_edges and edges_img is not None else blank
    roi_disp   = roi_img if show_roi and roi_img is not None else blank

    # Converter imagens em escala de cinza para BGR
    def ensure_color(img):
        if len(img.shape) == 2:  # Se for grayscale, converte para BGR
            return cv.cvtColor(img, cv.COLOR_GRAY2BGR)
        return img

    video_disp = ensure_color(video_disp)
    edges_disp = ensure_color(edges_disp)
    roi_disp = ensure_color(roi_disp)

    # Garantir que todas as imagens tenham a mesma altura
    def resize_to_reference(img, ref_height):
        if img.shape[0] != ref_height:
            return cv.resize(img, (img.shape[1], ref_height))
        return img

    video_disp = resize_to_reference(video_disp, height)
    edges_disp = resize_to_reference(edges_disp, height)
    roi_disp = resize_to_reference(roi_disp, height)

    main_window = cv.hconcat([video_disp, edges_disp, roi_disp])
    return main_window