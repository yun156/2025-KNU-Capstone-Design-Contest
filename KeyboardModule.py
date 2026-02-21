# KeyboardModule.py
# 표시 + 키 입력을 한 번에 처리 (imshow 후 waitKeyEx)

import cv2, numpy as np

def _kin(k,*ks): return k in ks

K_ESC=[27,65307]; K_Q=[ord('q'),ord('Q')]
K_W=[ord('w'),ord('W')]; K_S=[ord('s'),ord('S')]
K_A=[ord('a'),ord('A')]; K_D=[ord('d'),ord('D')]
K_UP=[2490368,65362]; K_DOWN=[2621440,65364]
K_LEFT=[2424832,65361]; K_RIGHT=[2555904,65363]
K_SPACE=[32,1048608]; K_R=[ord('r'),ord('R')]

class Keyboard:
    def __init__(self, view_scale=2.0, roi_keep=0.6):
        self.view_scale = view_scale
        self.roi_keep = roi_keep
        self.throttle = 0.0
        self.steer = 0.0
        self.THROTTLE_STEP = 0.05
        self.STEER_STEP    = 0.10
        self.win = "collect (W/S,A/D, SPACE=E-STOP, R reset, Q/ESC quit)"
        cv2.namedWindow(self.win, cv2.WINDOW_NORMAL)

    def update(self, rgb, steer_now, thr_now):
        """화면을 그리고, 키 입력을 읽어 조작값/액션을 반환"""
        # --- 표시 ---
        bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        h,w=bgr.shape[:2]; y0=int(h*(1-self.roi_keep))
        cv2.rectangle(bgr,(0,y0),(w-1,h-1),(0,255,0),1)
        cv2.line(bgr,(w//2,0),(w//2,h-1),(255,0,0),1)
        cv2.putText(bgr,f"steer:{steer_now:+.2f} thr:{thr_now:.2f}",
                    (8,20), cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
        if self.view_scale != 1.0:
            bgr = cv2.resize(bgr, (int(w*self.view_scale), int(h*self.view_scale)),
                             interpolation=cv2.INTER_NEAREST)
        cv2.imshow(self.win, bgr)

        # --- 키 입력 (반드시 imshow 뒤) ---
        k = cv2.waitKeyEx(1)
        action = None
        if k != -1:
            if _kin(k,*K_ESC) or _kin(k,*K_Q):
                action = "quit"
            elif _kin(k,*K_SPACE):
                self.throttle = 0.0
                action = "estop"
            elif _kin(k,*K_R):
                self.throttle = 0.0; self.steer = 0.0
            elif _kin(k,*K_W) or _kin(k,*K_UP):
                self.throttle = min(1.0, self.throttle + self.THROTTLE_STEP)
            elif _kin(k,*K_S) or _kin(k,*K_DOWN):
                self.throttle = max(0.0, self.throttle - self.THROTTLE_STEP)
            elif _kin(k,*K_A) or _kin(k,*K_LEFT):
                self.steer = max(-1.0, self.steer - self.STEER_STEP)
            elif _kin(k,*K_D) or _kin(k,*K_RIGHT):
                self.steer = min(+1.0, self.steer + self.STEER_STEP)

        return self.steer, self.throttle, action

    def close(self):
        cv2.destroyAllWindows()

