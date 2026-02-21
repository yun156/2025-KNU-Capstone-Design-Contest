# DataCollectionModule.py
# 이미지 저장 & CSV 로깅

import os, cv2, csv

class DataCollector:
    def __init__(self, img_dir, log_csv):
        self.img_dir = img_dir
        self.log_csv = log_csv
        os.makedirs(self.img_dir, exist_ok=True)
        self.idx = 1 + sum(1 for n in os.listdir(self.img_dir)
                           if n.lower().endswith(".jpg"))
        self._status = ""

    def save_frame(self, rgb):
        # OpenCV는 BGR 저장 → 변환
        bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        fname = f"{self.idx:06d}.jpg"
        abs_path = os.path.join(self.img_dir, fname)
        cv2.imwrite(abs_path, bgr, [cv2.IMWRITE_JPEG_QUALITY, 90])
        self.idx += 1
        return os.path.join("data", "images", fname)  # 로그에는 상대경로

    def append_log(self, ts, rel_path, steer, throttle):
        with open(self.log_csv, "a", newline="") as f:
            w = csv.writer(f)
            w.writerow([f"{ts:.6f}", rel_path, f"{steer:.5f}", f"{throttle:.5f}"])

    def note_status(self, text):
        self._status = text

