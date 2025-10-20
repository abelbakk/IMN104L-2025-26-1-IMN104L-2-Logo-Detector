import random
import time

class MockModel:

    def __init__(self):
        self.classes = ["DHL", "Old Spice", "Bumbu"]

    def predict(self, image):
        time.sleep(5)
        width, height = image.size

        detections = []
        for _ in range(random.randint(1, 3)):
            x1 = random.randint(0, width // 2)
            y1 = random.randint(0, height // 2)
            x2 = random.randint(width // 2, width)
            y2 = random.randint(height // 2, height)
            detection = {
                "class": random.choice(self.classes),
                "confidence": round(random.uniform(0.5, 1.0), 2),
                "bbox": [x1, y1, x2, y2]
            }
            detections.append(detection)

        return detections
