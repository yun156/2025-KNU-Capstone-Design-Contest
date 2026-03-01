import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # INFO 숨김

import time
import cv2
import numpy as np
import tflite_runtime.interpreter as tflite
from picamera2 import Picamera2
from libcamera import Transform

import RPi.GPIO as GPIO
from collections import deque

from MotorModule import Motor
from utlis import preprocess_img

# ===================== 모델/표시 =====================
MODEL_PATH = "models/model_dave2.tflite"
BASE_SPEED = 0.25
VIEW = True

# 런타임 부호(토글 키: F=전후, S=좌우)
# ─ 현재 하드웨어에서 "전진"이 되도록 기본값을 -1.0로 설정(더 이상 F키 필요 없음)
SPEED_SIGN = -1.0    # 전/후 부호 (하드웨어 기준 전진에 맞춤)
TURN_SIGN  = -1.0    # 좌/우 부호 (필요시 S로 토글)

# ===================== 초음파/LED =====================
TRIG = 2
ECHO = 3
LED_PINS = [16, 21, 26, 20]

SND_SPEED = 343.0
MAX_ECHO_TIME = 0.03
FILTER_N = 5
DETECT_DT = 0.05

SLOW_TOP = 20.0   # 감속 상한(cm)
STOP_AT  = 8.0    # 정지할 부분
EMERGENCY_AT = 5.0  # 급정지 + LED ON
STEER_TRIM     = 0.00   # 중심 트림(왼쪽으로 쳐지면 +0.02 정도, 오른쪽이면 -0.02)
STEER_DEADZONE = 0.08   # 이내는 0으로 무시(미세 떨림 억제)
STEER_CLIP     = 0.40   # 예측 조향의 절대 최대값 제한(0~1)
STEER_EMA_A    = 0.6    # 지수이동평균 계수(높을수록 더 느리게 반응)
TURN_SCALE     = 0.50   # MotorModule 내 turn*70이 커서, 진입 전 스케일 다운
WARMUP_SEC     = 1.0    # 시동 후 N초 동안 조향 0(카메라 안정 대기)
SOFTSTART_SEC  = 1.5    # 속도 서서히 올리기(급출발 방지)


# ===================== 유틸 =====================
def load_interpreter():
    print("[BOOT] loading TFLite...")
    itp = tflite.Interpreter(model_path=MODEL_PATH, num_threads=2)
    itp.allocate_tensors()
    inp = itp.get_input_details()[0]["index"]
    out = itp.get_output_details()[0]["index"]
    print("[BOOT] TFLite ready")
    return itp, inp, out

def predict(itp, inp_idx, out_idx, img):
    itp.set_tensor(inp_idx, img.astype(np.float32))
    itp.invoke()
    return float(itp.get_tensor(out_idx)[0][0])

def open_cam():
    print("[BOOT] opening camera...")
    cam = Picamera2()
    # 640x480보다 큰 해상도 우선 시도 -> 실패 시 자동 롤백
    tried = [(1024, 768), (800, 600), (640, 480)]
    for W, H in tried:
        try:
            cfg = cam.create_preview_configuration(
                main={"size": (W, H), "format": "RGB888"},
                transform=Transform(hflip=True, vflip=True)
            )
            cam.configure(cfg)
            cam.start()
            t0 = time.time()
            while True:
                arr = cam.capture_array()
                if arr is not None and arr.size and arr.mean() > 1:
                    print(f"[BOOT] camera ready @ {W}x{H}")
                    return cam
                if time.time() - t0 > 2.0:
                    break
                time.sleep(0.02)
            cam.stop()
        except Exception as e:
            try:
                cam.stop()
            except:
                pass
            # 다음 해상도 시도
            continue
    # 모든 시도가 실패한 경우 마지막으로 640x480 강제
    cfg = cam.create_preview_configuration(
        main={"size": (640, 480), "format": "RGB888"},
        transform=Transform(hflip=True, vflip=True)
    )
    cam.configure(cfg)
    cam.start()
    print("[BOOT] camera ready @ 640x480 (fallback)")
    return cam

# ----- 초음파 + LED -----
def gpio_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)  # GPIO3는 하드웨어 풀업 존재
    GPIO.output(TRIG, GPIO.LOW)
    for p in LED_PINS:
        GPIO.setup(p, GPIO.OUT)
        GPIO.output(p, GPIO.LOW)

def leds_on(on=True):
    val = GPIO.HIGH if on else GPIO.LOW
    for p in LED_PINS:
        GPIO.output(p, val)

def read_distance_once():
    GPIO.output(TRIG, GPIO.LOW)
    time.sleep(0.000005)
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.000010)
    GPIO.output(TRIG, GPIO.LOW)

    t0 = time.time()
    while GPIO.input(ECHO) == 0:
        if time.time() - t0 > MAX_ECHO_TIME:
            return None
    start = time.time()

    while GPIO.input(ECHO) == 1:
        if time.time() - start > MAX_ECHO_TIME:
            return None
    end = time.time()

    dt = end - start
    dist_m = (SND_SPEED * dt) / 2.0
    return dist_m * 100.0

class DistFilter:
    def __init__(self, n=FILTER_N):
        self.buf = deque(maxlen=n)
    def push(self, v):
        if v is not None:
            self.buf.append(float(v))
    def value(self):
        if not self.buf:
            return None
        arr = sorted(self.buf)
        mid = len(arr) // 2
        if len(arr) % 2:
            return arr[mid]
        return 0.5 * (arr[mid-1] + arr[mid])

# ===================== 메인 =====================
def main():
    global SPEED_SIGN, TURN_SIGN

    itp, INP, OUT = load_interpreter()
    cam = open_cam()
    motor = Motor(18, 22, 27, 23, 25, 24)

    gpio_setup()
    dfilter = DistFilter()
    last_echo = 0.0

    throttle = BASE_SPEED
    last_log = 0.0
    
    steer_s = 0.0              # 조향 EMA 초기값
    t_start = time.time()      # 기동 시각(워밍업/소프트스타트용)


    print("[RUN] entering loop")
    try:
        while True:
            # ---- 카메라/추론 ----
            rgb = cam.capture_array()
            steer = 0.0
            if rgb is not None and rgb.size:
                bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
                proc = preprocess_img(bgr)         # (66,200,3), [-1,1]
                proc = np.expand_dims(proc, 0)
                steer = predict(itp, INP, OUT, proc)
                
            else:
                # 프레임 없을 때도 파이프 유지
                bgr = np.zeros((480, 640, 3), np.uint8)
            
            # ---- [조향 후처리] 트림 → 데드존 → 클립 → EMA → 스케일
            steer = TURN_SIGN * (steer + STEER_TRIM)            # 부호/트림
            if abs(steer) < STEER_DEADZONE:                     # 데드존
                steer = 0.0
            steer = float(np.clip(steer, -STEER_CLIP, STEER_CLIP))  # 클립

            # EMA 스무딩 (steer_s는 main()에서 초기화)
            steer_s = STEER_EMA_A * steer_s + (1.0 - STEER_EMA_A) * steer

            # MotorModule로 넘길 조향(너무 예민하면 TURN_SCALE 줄여주기)
            turn_f = TURN_SCALE * steer_s


            # ---- 초음파(주기 측정) ----
            now = time.time()
            if now - last_echo >= DETECT_DT:
                d = read_distance_once()
                dfilter.push(d)
                last_echo = now
            d_cm = dfilter.value()

            # ---- 속도/조향 결정 ----
            # ---- [속도/조향 결정] WARMUP + SOFTSTART + 초음파 감속/정지

            # 1) 소프트스타트: 시작 후 SOFTSTART_SEC 동안 0->throttle로 선형 상승
            elapsed = time.time() - t_start
            base_spd = throttle
            if elapsed < SOFTSTART_SEC:
                ramp = elapsed / SOFTSTART_SEC
                base_spd = base_spd * float(np.clip(ramp, 0.0, 1.0))

            # 2) 워밍업: 초기 WARMUP_SEC 동안은 조향을 0으로 고정
            turn_cmd = 0.0 if elapsed < WARMUP_SEC else turn_f

            # 3) 초음파 기반 감속/정지
            spd_eff = SPEED_SIGN * base_spd
            emergency = False
            if d_cm is not None:
                if d_cm <= EMERGENCY_AT:
                    # 5cm 이내 -> 급정지 + LED ON
                    spd_eff = 0.0
                    emergency = True
                elif d_cm <= STOP_AT:
                    # 5~8cm -> 정지(LED OFF)
                    spd_eff = 0.0
                elif d_cm <= SLOW_TOP:
                    # 8~20cm -> 선형 감속 (20→100%, 8→0%)
                    scale = (d_cm - STOP_AT) / max(1e-6, (SLOW_TOP - STOP_AT))  # (d-8)/(20-8)
                    scale = float(np.clip(scale, 0.0, 1.0))
                    spd_eff = spd_eff * scale

            # 4) LED (긴급 시 ON)
            leds_on(emergency)

            # 5) 모터 구동
            if spd_eff != 0.0:
                motor.move(speed=spd_eff, turn=turn_cmd)
            else:
                motor.stop()



            # ---- 표시/키 ----
            if VIEW:
                info = f"steer={steer:+.2f} spd={spd_eff:.2f} dist={'NA' if d_cm is None else f'{d_cm:.1f}cm'}"
                cv2.putText(bgr, info, (6, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
                cv2.putText(bgr, f"SIGN(F)={SPEED_SIGN:+.0f} TURN(S)={TURN_SIGN:+.0f}", (6, 36),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255,255,255), 2)
                cv2.imshow("autocar (q:quit, F/S:flip signs)", bgr)
                k = cv2.waitKey(1) & 0xFF
                if k == ord("q"):
                    break
                elif k in (ord("f"), ord("F")):
                    SPEED_SIGN *= -1.0
                    print(f"[KEY] SPEED_SIGN -> {SPEED_SIGN:+.0f}")
                elif k in (ord("s"), ord("S")):
                    TURN_SIGN *= -1.0
                    print(f"[KEY] TURN_SIGN  -> {TURN_SIGN:+.0f}")

            # 로그(0.5s 주기)
            if time.time() - last_log > 0.5:
                print(f"[LOOP] steer={steer:+.2f}  spd_eff={spd_eff:.2f}  dist={'NA' if d_cm is None else f'{d_cm:.1f}cm'}")
                last_log = time.time()

    finally:
        try:
            motor.stop()
        except:
            pass
        leds_on(False)
        GPIO.cleanup()
        cam.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()



