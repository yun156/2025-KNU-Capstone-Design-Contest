# WebcamModule.py
# Picamera2로 RGB 프레임 캡처

import time, numpy as np
from picamera2 import Picamera2
from libcamera import Transform

class Camera:
    def __init__(self, w=320, h=240, fps=12, hflip=True, vflip=True):
        self.w, self.h, self.fps = w, h, fps
        self.cam = Picamera2()
        cfg = self.cam.create_preview_configuration(
            main={"size": (w, h), "format":"RGB888"},
            transform=Transform(hflip=hflip, vflip=vflip)
        )
        self.cam.configure(cfg)
        us = int(1e6/float(fps))
        self.cam.set_controls({"FrameDurationLimits": (us, us)})
        self.cam.start()
        # 첫 유효 프레임 대기
        t0=time.time()
        while time.time()-t0 < 2.0:
            arr = self.cam.capture_array()
            if arr is not None and arr.size and arr.mean()>1:
                break
            time.sleep(0.02)

    def capture_rgb(self):
        arr = self.cam.capture_array()
        if arr is None or not arr.size: return None
        return arr  # RGB888 numpy(H,W,3)

    def close(self):
        try: self.cam.stop()
        except: pass

