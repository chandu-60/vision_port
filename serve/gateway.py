import io

import torch
from fastapi import FastAPI, File, HTTPException, UploadFile
<<<<<<< HEAD
from ultralytics import YOLO

app = FastAPI(title="VisionPort Gateway (Session 2 prototype)")
device = "cuda" if torch.cuda.is_available() else "cpu"

model = YOLO("yolov8n.pt")


=======
from PIL import Image
from ultralytics import YOLO

app = FastAPI(title="VisionPort Gateway (Session 2 prototype)")

device = "cuda" if torch.cuda.is_available() else "cpu"
model = YOLO("yolov8n.pt")

>>>>>>> 5cd276278db67aa79a56e7c47bf00ebf0b8a781f
@app.get("/")
def home():
    return {
        "project": "VisionPort",
        "message": "VisionPort FastAPI Gateway is running!",
        "status": "success",
<<<<<<< HEAD
        "device": "cuda",
        "available_endpoint": [
=======
        "device": device,
        "available_endpoints": [
>>>>>>> 5cd276278db67aa79a56e7c47bf00ebf0b8a781f
            "/health",
            "/detect",
            "/docs"
        ]
    }

<<<<<<< HEAD


@app.post("/detect")
async def detect(file: UploadFile = File(...), conf: float = 0.35):
    # 1. Validate the request
    if file.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a JPG or PNG image."
        )

    try:
        # 2. Read the uploaded image
        contents = await file.read()

        if not contents:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )

        # 3. Convert bytes to an image
        from PIL import Image

        image = Image.open(io.BytesIO(contents)).convert("RGB")

        # 4. Run YOLO detection
        results = model.predict(
            source=image,
            conf=conf,
            device=device
        )

        # 5. Extract detections
        detections = []

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0].item())
                confidence = float(box.conf[0].item())
                coordinates = box.xyxy[0].tolist()

                detections.append({
                    "class_id": class_id,
                    "class_name": result.names[class_id],
                    "confidence": round(confidence, 4),
                    "bounding_box": {
                        "x1": round(coordinates[0], 2),
                        "y1": round(coordinates[1], 2),
                        "x2": round(coordinates[2], 2),
                        "y2": round(coordinates[3], 2)
                    }
                })

        return {
            "project": "VisionPort",
            "status": "success",
            "filename": file.filename,
            "device": device,
            "total_detections": len(detections),
            "detections": detections
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Object detection failed: {str(e)}"
        ) from e

    finally:
        await file.close()
=======
@app.post("/detect")
def detect(image: UploadFile = File(...), conf: float = 0.35):
    if image.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(status_code=415, detail="Send a JPEG or PNG image")

    try:
        image = Image.open(io.BytesIO(image.file.read())).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Could not decode image")

    r = model.predict(image, conf=conf, device=device, verbose=False)[0]

    detections = [
        {
            "class": r.names[int(c)],
            "confidence": round(float(s), 3),
            "box_xyxy": [round(float(v), 1) for v in b],
        }
        for c, s, b in zip(r.boxes.cls, r.boxes.conf, r.boxes.xyxy)
    ]

    return {
        "image_size": {"width": image.width, "height": image.height},
        "num_detections": len(detections),
        "detections": detections,
        "timing_ms": {k: round(v, 2) for k, v in r.speed.items()},
    }
>>>>>>> 5cd276278db67aa79a56e7c47bf00ebf0b8a781f
