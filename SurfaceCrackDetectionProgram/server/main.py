from fastapi import FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect  # Import WebSocketDisconnect
from fastapi.responses import HTMLResponse
from ultralytics import YOLO
import json
import base64
from PIL import Image
import numpy as np
import io


app = FastAPI()

model = YOLO("../runs/detect/weights/best.pt")  # your trained YOLO model

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            image_data = base64.b64decode(message["data"])

            img = Image.open(io.BytesIO(image_data)).convert("RGB")

            results = model(img)

            r = results[0]

            if r.boxes is None or len(r.boxes) == 0:
                await websocket.send_text(json.dumps({
                    "type": "prediction",
                    "has_crack": False,
                    "crack_count": 0,
                    "max_confidence": 0
                }))
                continue

            boxes = r.boxes
            crack_count = len(boxes)

            confidences = [float(box.conf[0]) for box in boxes]
            max_conf = max(confidences)

            await websocket.send_text(json.dumps({
                "type": "prediction",
                "has_crack": True,
                "crack_count": crack_count,
                "max_confidence": max_conf * 100
            }))

            if r.boxes is None or len(r.boxes) == 0:
                await websocket.send_text(json.dumps({
                    "type": "prediction",
                    "class": "none",
                    "score": 0
                }))
                continue

            box = r.boxes[0]

            cls_id = int(box.cls[0])
            conf = float(box.conf[0])

            class_name = model.names[cls_id]

            await websocket.send_text(json.dumps({
                "type": "prediction",
                "class": class_name,
                "score": conf * 100
            }))

    except WebSocketDisconnect:
        pass