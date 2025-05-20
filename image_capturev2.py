import numpy as np
import win32gui
import os
from PIL import Image
from time import sleep
import mss

class WindowCapture:
    def __init__(self, window_name, monitor_number=1):
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))

        self.monitor_number = monitor_number
        self.update_window_rect()

    def update_window_rect(self):
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.left = window_rect[0]
        self.top = window_rect[1]
        self.right = window_rect[2]
        self.bottom = window_rect[3]
        self.w = self.right - self.left
        self.h = self.bottom - self.top

    def is_within_monitor(self, monitor):
        # Verifica si la ventana está completamente dentro del monitor
        return (self.left >= monitor["left"] and
                self.top >= monitor["top"] and
                self.right <= monitor["left"] + monitor["width"] and
                self.bottom <= monitor["top"] + monitor["height"])

    def get_screenshot(self):
        self.update_window_rect()

        with mss.mss() as sct:
            monitor = sct.monitors[self.monitor_number]

            if not self.is_within_monitor(monitor):
                raise Exception(f"La ventana no está completamente en el monitor {self.monitor_number}")

            capture_area = {
                "top": self.top,
                "left": self.left,
                "width": self.w,
                "height": self.h
            }
            sct_img = sct.grab(capture_area)
            img = np.array(sct_img)[..., :3]
            img = np.ascontiguousarray(img)
            return img

    def generate_image_dataset(self):
        if not os.path.exists("images"):
            os.mkdir("images")
        while True:
            try:
                img = self.get_screenshot()
                img_rgb = img[..., ::-1]
                im = Image.fromarray(img_rgb)
                im.save(f"./images/img_{len(os.listdir('images'))}.jpg")
                print("Imagen guardada.")
                sleep(0.3)
            except Exception as e:
                print(f"Error: {e}")
                sleep(1)

    def get_window_size(self):
        self.update_window_rect()
        return (self.w, self.h)

# Elegir el monitor 2, por ejemplo
wincap = WindowCapture(window_name="OPTCGSim", monitor_number=2)
wincap.generate_image_dataset()
