import os
import logging
from ultralytics import YOLO

logger = logging.getLogger(__name__)

class YoloModel:

    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        weights_path = os.path.join(base_dir, "../resources/weights/small/tuned_06.pt")
        logger.info(f"Loading YOLO model from: {weights_path}")
        try:
            self.model = YOLO(weights_path)
            self.classes = self.model.names
            logger.info("YOLO model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise

    def predict(self, image):
        logger.info("Starting prediction...")
        results = self.model.predict(image, verbose=False)
        detections = []
        if results[0].boxes is not None:
            boxes = results[0].boxes.cpu().numpy()
            for box in boxes:
                try:
                    x1, y1, x2, y2 = box.xyxy[0].astype(int)
                    conf = round(float(box.conf[0]), 2)
                    cls_index = int(box.cls[0])
                    
                    class_name = self.model.names[cls_index]
                    
                    detections.append({
                        "class": class_name,
                        "confidence": conf,
                        "bbox": [x1, y1, x2, y2]
                    })
                except Exception as e:
                    logger.error(f"Error processing box: {box}. Error: {e}")
                    raise

        num_detections = len(detections)
        if num_detections > 0:
            logger.info(f"Prediction complete. Found {num_detections} detections.")
        else:
            logger.info("Prediction complete. No detections found.")

        return detections