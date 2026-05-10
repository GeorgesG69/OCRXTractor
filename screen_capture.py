import tkinter as tk
from PIL import ImageGrab

class ScreenSnip:
    def __init__(self, master):
        self.master = master
        # Toplevel crea una ventana secundaria vinculada a la principal
        self.top = tk.Toplevel(master)
        self.top.attributes('-alpha', 0.3)
        self.top.attributes('-fullscreen', True)
        self.top.configure(background='black')
        self.top.attributes("-topmost", True)
        self.top.config(cursor="cross")

        self.start_x = None
        self.start_y = None
        self.rect = None
        self.captured_image = None

        self.canvas = tk.Canvas(self.top, cursor="cross", bg="black")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.top.bind("<Escape>", lambda e: self.top.destroy())

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, 1, 1, outline='red', width=2, fill="gray"
        )

    def on_move_press(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)

        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)

        self.top.destroy()

        if x2 - x1 > 5 and y2 - y1 > 5:
            self.captured_image = ImageGrab.grab(bbox=(x1, y1, x2, y2))

def capture_screen_area(master):
    """Función helper actualizada que recibe la ventana principal."""
    snip = ScreenSnip(master)
    # Espera a que la ventana de recorte se cierre antes de continuar
    master.wait_window(snip.top)
    return snip.captured_image