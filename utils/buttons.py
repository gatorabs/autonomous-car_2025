import tkinter as tk
from threading import Thread


controls = {
    "SHOW_VIDEO": True,
    "SHOW_EDGES": True,
    "SHOW_ROI": True
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

    root.mainloop()


def start_tkinter_thread():
    # Roda a interface Tkinter em uma thread separada para não bloquear o loop do OpenCV
    t = Thread(target=create_tkinter_controls, daemon=True)
    t.start()
