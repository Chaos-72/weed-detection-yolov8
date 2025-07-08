
# Real‑Time Weed Detection using YOLOv8 & ONNX Runtime on Raspberry Pi 3B+

A compact, low‑cost real‑time weed detection system for smart agriculture.  
Uses a fine‑tuned YOLOv8 model exported to ONNX, running on a Raspberry Pi 3B+ with camera.

---

## Project Overview

Distinguishes **crops** vs **weeds** in real‑time on the edge.  
When a weed is detected, a buzzer is triggered. Works offline in the field.

---

## Model & Training Details

- **Base Model:** YOLOv8s (`yolov8s.pt`)  
- **Framework:** [Ultralytics YOLOv8](https://docs.ultralytics.com/)  
- **Dataset:** Custom crop/weed images (`0 = crop`, `1 = weed`)  
- **Classes:**  
  ```yaml
  nc: 2
  names: ['crop','weed']
  ```

* **Augmentations:** HSV, scale, translate, flip, mosaic
* **Export Format:** ONNX (`.onnx`)
* **Inference Engine:** ONNX Runtime

## Folder Structure

```
weed-detection-yolov8/
│
├── configs/
│   └── args.yaml               # training parameters
│
├── dataset/                    # YOLOv8 data layout
│   ├── images/
│   │   ├── train/              # 70% images
│   │   ├── val/                # 20%
│   │   └── test/               # 10%
│   ├── labels/
│   │   ├── train/              # .txt labels
│   │   ├── val/
│   │   └── test/
│   └── data.yaml               # dataset config
│
├── models/
│   ├── yolov8s_weed.pt         # trained PyTorch model
│   └── yolov8s_weed.onnx       # exported ONNX model
│
├── scripts/
│   ├── organize.py             # split & copy images into train/val/test
│   ├── convert_to_onnx.py      # export .pt → .onnx
│   ├── yolo_detect.py          # multi‑source inference (images/video/webcam)
│
├── training_logs/
│   ├── results.csv             # epoch metrics
│   └── plots/                  # PR, F1, confusion matrix, etc.
│
├── utils/
│   └── test_cam.py             # basic webcam test (optional)
│
├── requirements.txt            # Python dependencies
└── README.md                   # you are here
```

---

[Download ONNX Model](https://github.com/Chaos-72/weed-detection-yolov8/releases/tag/v1.0-onnx-release/yolov8s_weed.onnx)
[Download Sample Dataset](https://github.com/Chaos-72/weed-detection-yolov8/releases/tag/v1.0-onnx-release/dataset.zip)


## Setup & Installation

1. **Flash OS**
   Use Raspberry Pi Imager → **Raspberry Pi OS (32‑bit) with Desktop**, enable SSH.

2. **Create conda environment**
   ```bash
   conda create --name <env_name> python=3.11 -y
   ```
   - <env_name> add your conda env name here. <br>
   ```bash
   conda activate <env_name>
   ```


2. **Install packages**

   ```bash
   pip install -r requirements.txt
   ```

3. **Enable camera**

   ```bash
   sudo raspi-config
   # Interface Options → Camera → Enable → Reboot
   ```

4. **Clone**

   ```bash
   git clone https://github.com/chaos-72/weed-detection-yolov8.git
   cd weed-detection-yolov8
   ```

---

## Data Preparation

Run the dataset splitter:

```bash
python scripts/organize.py
```

✔️ Creates `dataset/images/{train,val,test}` and corresponding `dataset/labels/…`.

---

## Training

```bash
> run the notebook -> Weed_Detection.ipynb
```
---

## Export to ONNX

```bash
python scripts/convert_to_onnx.py
```

or in Python:

```python
from ultralytics import YOLO
model = YOLO("runs/detect/yolov8s_weed/weights/best.pt")
model.export(format="onnx")
```

---

## Inference

### 1. Multi‑source (images, video, webcam, picamera)

```bash
python scripts/yolo_detect.py \
  --model models/yolov8s_weed.onnx \
  --source test/video.mp4 \
  --resolution 640x480 \
  --record
```

OR 
single line command

```bash
python scripts/yolo_detect.py --model models/yolov8s_weed.onnx --source test/video.mp4 --resolution 640x480 --record
```

### 2. Simple laptop webcam

```bash
python scripts/yolo_detect.py \
  --model models/yolov8s_weed.onnx \
  --source usb0 \
  --resolution 640x480
```
OR 
single line command

```bash
python scripts/yolo_detect.py --model models/yolov8s_weed.onnx --source usb0 --resolution 640x480 --record
```


### 3. Test camera only

```bash
python utils/test_cam.py
```

---

## Training Logs & Plots

* **results.csv** → metrics per epoch
* **training\_logs/plots/** → PR‑curve, F1, confusion matrix, class distributions
