# buttons.py
import tkinter as tk
from threading import Thread

controls = {
    "SHOW_VIDEO": True,
    "SHOW_EDGES": True,
    "SHOW_ROI": True,
    "SHOW_PERSON_DETECTION": True
}

def toggle_show_video():
    controls["SHOW_VIDEO"] = not controls["SHOW_VIDEO"]
    print("SHOW_VIDEO:", controls["SHOW_VIDEO"])

def toggle_show_edges():
    controls["SHOW_EDGES"] = not controls["SHOW_EDGES"]
    print("SHOW_EDGES:", controls["SHOW_EDGES"])

def toggle_show_roi():
    controls["SHOW_ROI"] = not controls["SHOW_ROI"]
    print("SHOW_ROI:", controls["SHOW_ROI"])

def toggle_show_person_detection():
    controls["SHOW_PERSON_DETECTION"] = not controls["SHOW_PERSON_DETECTION"]
    print("SHOW_PERSON_DETECTION:", controls["SHOW_PERSON_DETECTION"])

def create_tkinter_controls():
    root = tk.Tk()
    root.title("Controles Adicionais")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    btn_video = tk.Button(frame, text="Toggle SHOW_VIDEO", command=toggle_show_video)
    btn_video.pack(side=tk.LEFT, padx=5)

    btn_edges = tk.Button(frame, text="Toggle SHOW_EDGES", command=toggle_show_edges)
    btn_edges.pack(side=tk.LEFT, padx=5)

    btn_roi = tk.Button(frame, text="Toggle SHOW_ROI", command=toggle_show_roi)
    btn_roi.pack(side=tk.LEFT, padx=5)

    btn_person_detection = tk.Button(frame, text="Toggle PERSON_DETECTION", command=toggle_show_person_detection)
    btn_person_detection.pack(side=tk.LEFT, padx=5)

    root.mainloop()

def start_tkinter_thread():
    t = Thread(target=create_tkinter_controls, daemon=True)
    t.start()
