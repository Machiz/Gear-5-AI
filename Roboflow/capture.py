import numpy as np
import win32gui
import os
from PIL import Image
import mss

class WindowCapture:
    def __init__(self, window_name):
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            return
            
        # self.update_window_rect()

    def update_window_rect(self):

        # (-9, -9, 1929, 1039)
        self.left = -9
        self.top = -9
        self.right = 1929
        self.bottom = 1039
        self.w = self.right - self.left
        self.h = self.bottom - self.top
        # self.left = window_rect[0]
        # self.top = window_rect[1]
        # self.right = window_rect[2]
        # self.bottom = window_rect[3]
        # self.w = self.right - self.left
        # self.h = self.bottom - self.top

    def get_screenshot(self):
        self.update_window_rect()

        with mss.mss() as sct:
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
        if not os.path.exists("Roboflow/capturas"):
            os.mkdir("Roboflow/capturas")
        try:
            img = self.get_screenshot()
            img_rgb = img[..., ::-1]
            im = Image.fromarray(img_rgb)
            path = f"./Roboflow/capturas/img_{len(os.listdir('Roboflow/capturas'))}.jpg"
            im.save(path)
            print("Imagen guardada.")
            return path
        except Exception as e:
            print(f"Error: {e}")
            return ""
            
def Capturar():
    # No necesitas especificar el monitor, captura por ventana directamente
    wincap = WindowCapture(window_name="OPTCGSim")
    if(wincap.hwnd == 0): return ""
    
    return wincap.generate_image_dataset()
