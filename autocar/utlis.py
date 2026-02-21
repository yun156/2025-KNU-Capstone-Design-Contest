# utlis.py
# - 데이터 로드(훈련용), 전처리/증강, DAVE-2 경량 모델 (훈련 시)
# - runMain.py에서는 preprocess_img()만 사용

import os, random
import numpy as np
import cv2

# =========================
# 데이터 로드(훈련에만 사용)
# =========================
def import_data(data_dir, min_throttle=0.05):
    """
    data/log.csv을 읽어 [image, steer] DataFrame 반환.
    - 구분자 자동 감지(쉼표/세미콜론/탭 등)
    - 인코딩 BOM 처리
    - 헤더가 없을 때도 자동 복구 (timestamp,image_path,steer,throttle)
    - 열 이름 공백 제거 + 소문자화
    - image_path / image / img / path / filepath 모두 허용
    - steer / steering / angle / turn 모두 허용
    """
    # pandas는 훈련에서만 필요하므로, 여기 내부에서 임포트
    try:
        import pandas as pd
    except ImportError as e:
        raise ImportError(
            "import_data()는 훈련 전용이며 pandas가 필요합니다. "
            "라즈베리파이에서 추론만 할 경우 utlis.import_data()를 호출하지 마세요. "
            "훈련을 원한다면 'pip install pandas'로 설치하세요."
        ) from e

    log_csv = os.path.join(data_dir, "log.csv")

    # 1) 1차 시도: 일반 헤더 가정
    df = pd.read_csv(log_csv, engine="python", sep=None,
                     encoding="utf-8-sig", on_bad_lines="skip")

    # 헤더 없이 저장된 경우 감지
    bad_header = False
    if len(df.columns) == 4:
        def looks_like_data(col):
            s = str(col).strip().lower()
            return (
                s.replace('.', '', 1).isdigit() or   # timestamp처럼 보임
                s.endswith('.jpg') or
                s in {'0', '0.0', '0.00000', '0.00000.1'}
            )
        if all(looks_like_data(c) for c in df.columns):
            bad_header = True

    if bad_header:
        # 2) 헤더 없음 → 컬럼명 강제 지정
        df = pd.read_csv(log_csv, engine="python", sep=None, header=None,
                         names=["timestamp", "image_path", "steer", "throttle"],
                         encoding="utf-8-sig", on_bad_lines="skip")
        # 수치형 변환/필터
        df["throttle"] = pd.to_numeric(df["throttle"], errors="coerce").fillna(0.0)
        if min_throttle is not None:
            df = df[df["throttle"] >= float(min_throttle)].copy()
        df["steer"] = pd.to_numeric(df["steer"], errors="coerce")
        df = df.dropna(subset=["steer"]).copy()

        # 경로 정규화 (상대경로→절대경로)
        log_dir = os.path.dirname(log_csv)
        def to_abs(p):
            p = str(p).strip().replace("\\", "/")
            return os.path.normpath(p if os.path.isabs(p) else os.path.join(log_dir, p))
        df["image"] = df["image_path"].map(to_abs)

        return df[["image", "steer"]].reset_index(drop=True)

    # ---- 일반 케이스: 헤더 있음 ----
    df.columns = [c.strip().lower() for c in df.columns]

    img_col_candidates   = ["image_path", "image", "img", "path", "filepath"]
    steer_col_candidates = ["steer", "steering", "angle", "turn"]

    img_col   = next((c for c in img_col_candidates   if c in df.columns), None)
    steer_col = next((c for c in steer_col_candidates if c in df.columns), None)

    if img_col is None or steer_col is None:
        raise ValueError(f"CSV 헤더 확인 필요: 찾은 열들={list(df.columns)}")

    thr_col = "throttle" if "throttle" in df.columns else None
    if thr_col:
        df[thr_col] = pd.to_numeric(df[thr_col], errors="coerce").fillna(0.0)
        if min_throttle is not None:
            df = df[df[thr_col] >= float(min_throttle)].copy()

    df[steer_col] = pd.to_numeric(df[steer_col], errors="coerce")
    df = df.dropna(subset=[steer_col]).copy()

    # 경로 정규화
    log_dir = os.path.dirname(log_csv)
    def to_abs(p):
        p = str(p).strip().replace("\\", "/")
        return os.path.normpath(p if os.path.isabs(p) else os.path.join(log_dir, p))
    df["image"] = df[img_col].map(to_abs)

    return df[["image", steer_col]].rename(columns={steer_col: "steer"}).reset_index(drop=True)


# =========================
# 전처리/증강
# =========================
ROI_KEEP = 0.60  # 하단 60% 사용 (수집 미리보기 설정과 맞춤)

def preprocess_img(bgr, img_w=200, img_h=66, roi_keep=ROI_KEEP):
    """
    BGR → 하단 ROI → RGB → (200x66) → [-1,1]
    runMain.py(TFLite)에서도 동일하게 사용됨.
    """
    h, w = bgr.shape[:2]
    y0 = int(h * (1.0 - roi_keep))
    roi = bgr[y0:h, :, :]

    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    roi = cv2.resize(roi, (img_w, img_h), interpolation=cv2.INTER_AREA)
    roi = roi.astype(np.float32) / 255.0
    roi = (roi - 0.5) / 0.5  # [-1,1]
    return roi

def augment(bgr, steer):
    """훈련용 간단 증강: 좌우반전, 밝기, 평행이동(조향 보정)"""
    # 좌우 반전
    if random.random() < 0.5:
        bgr = cv2.flip(bgr, 1)
        steer = -steer
    # 밝기
    if random.random() < 0.5:
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        v = hsv[:, :, 2].astype(np.float32)
        v *= (0.6 + 0.8 * random.random())  # 0.6~1.4
        hsv[:, :, 2] = np.clip(v, 0, 255).astype(np.uint8)
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    # 평행이동(좌우 이동 → 조향 보정)
    if random.random() < 0.5:
        tx = int(20 * (random.random() * 2 - 1))
        ty = int(8  * (random.random() * 2 - 1))
        M = np.float32([[1, 0, tx], [0, 1, ty]])
        bgr = cv2.warpAffine(bgr, M, (bgr.shape[1], bgr.shape[0]),
                             borderMode=cv2.BORDER_REFLECT)
        steer += -tx / 100.0
        steer = float(np.clip(steer, -1.0, 1.0))
    return bgr, steer

def data_generator(df, batch_size=64, train=True, img_w=200, img_h=66):
    """Keras용 제너레이터 (훈련 시에만 사용)"""
    # pandas가 필요하므로 이 함수는 보통 노트북/훈련 환경에서만 사용
    n = len(df)
    while True:
        idxs = np.random.choice(n, batch_size)
        X = np.zeros((batch_size, img_h, img_w, 3), np.float32)
        y = np.zeros((batch_size, 1), np.float32)
        for i, idx in enumerate(idxs):
            row = df.iloc[idx]
            bgr = cv2.imread(row['image'])
            if bgr is None:  # 누락 방지
                bgr = np.zeros((240, 320, 3), np.uint8)
            steer = float(row['steer'])
            if train:
                bgr, steer = augment(bgr, steer)
            X[i] = preprocess_img(bgr, img_w=img_w, img_h=img_h)
            y[i, 0] = steer
        yield X, y


# =========================
# DAVE-2 경량 모델 (훈련 시)
# =========================
def create_model(lr=1e-3, img_w=200, img_h=66):
    """TensorFlow/Keras 훈련용 모델 (라즈베리파이 추론에는 미사용)"""
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D, Dense, Flatten, ELU
    from tensorflow.keras.optimizers import Adam

    model = Sequential([
        Conv2D(24,(5,5),strides=(2,2),input_shape=(img_h,img_w,3)), ELU(),
        Conv2D(36,(5,5),strides=(2,2)), ELU(),
        Conv2D(48,(5,5),strides=(2,2)), ELU(),
        Conv2D(64,(3,3)), ELU(),
        Conv2D(64,(3,3)), ELU(),
        Flatten(),
        Dense(100), ELU(),
        Dense(50),  ELU(),
        Dense(10),  ELU(),
        Dense(1)    # steer
    ])
    model.compile(optimizer=Adam(learning_rate=lr), loss='mse')
    return model

