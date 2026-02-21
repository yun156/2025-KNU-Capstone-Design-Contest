# DataCollectionMain.py
# 키보드 테레옵으로 주행하며 이미지/라벨(steer, throttle) 수집

import os, time, csv
from DataCollectionModule import DataCollector
from WebcamModule import Camera
from KeyboardModule import Keyboard
from MotorModule import Motor, mix_pwm

# ===== 설정 =====
DATA_DIR = "data"
IMG_DIR  = os.path.join(DATA_DIR, "images")
LOG_CSV  = os.path.join(DATA_DIR, "log.csv")
os.makedirs(IMG_DIR, exist_ok=True)

# 카메라/표시
FRAME_W, FRAME_H = 320, 240
CAP_FPS   = 12
VIEW_SCALE= 2.0
HFLIP, VFLIP = True, True
ROI_KEEP  = 0.60  # 화면 하단 60%가 노면

# 주행/모터
START_DUTY = 28.0
MAX_DUTY   = 65.0
TURN_GAIN  = 25.0
STEER_CLIP = 1.0
STEER_SIGN = -1.0     # 좌/우 반전 보정 (+1.0로 바꾸면 원래대로)
ALPHA_THR  = 0.35
ALPHA_STR  = 0.50

def main():
    cam = Camera(FRAME_W, FRAME_H, CAP_FPS, HFLIP, VFLIP)
    kb  = Keyboard(VIEW_SCALE, ROI_KEEP)
    mc  = DataCollector(IMG_DIR, LOG_CSV)
    motor = Motor()

    # CSV 헤더
    if not os.path.exists(LOG_CSV):
        with open(LOG_CSV, "w", newline="") as f:
            csv.writer(f).writerow(["timestamp","image_path","steer","throttle"])

    s_thr = 0.0; s_str = 0.0
    period = 1.0/float(CAP_FPS)
    t_next = time.time()

    try:
        while True:
            rgb = cam.capture_rgb()
            if rgb is None: continue

            # 키 처리 → 명령 얻기
            #steer_cmd, thr_cmd, action = kb.poll(rgb)
            steer_cmd, thr_cmd, action = kb.update(rgb, s_str, s_thr)
            if action == "quit": break
            if action == "estop":
                s_thr = 0.0; s_str = 0.0
                motor.stop()
                mc.note_status("E-STOP")
                # 저장은 계속 진행(정지 프레임은 후처리에서 제외 권장)

            # 지령 스무딩
            s_thr = ALPHA_THR*s_thr + (1-ALPHA_THR)*thr_cmd
            s_str = ALPHA_STR*s_str + (1-ALPHA_STR)*steer_cmd

            # 모터 구동
            if s_thr <= 0.0:
                motor.stop()
            else:
                l, r = mix_pwm(s_thr, s_str, START_DUTY, MAX_DUTY,
                               TURN_GAIN, STEER_CLIP, STEER_SIGN)
                motor.set_duty(l, r)

            # 저장 타이밍 (고정 FPS로 저장)
            now = time.time()
            if now >= t_next:
                t_next += period
                rel_path = mc.save_frame(rgb)  # images/000xxx.jpg
                mc.append_log(now, rel_path, s_str, s_thr)

            # 오버레이 프리뷰
            #kb.show_preview(rgb, s_str, s_thr)

    finally:
        try: motor.close()
        except: pass
        cam.close()
        kb.close()

if __name__ == "__main__":
    main()

