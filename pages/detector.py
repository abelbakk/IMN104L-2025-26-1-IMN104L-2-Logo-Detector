import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from model.mock_model import MockModel

BBOX_COLORS = [
    "#E6194B",
    "#3CB44B",
    "#0082C8",
    "#F58231",
    "#911EB4"
]

@st.cache_resource
def load_model():
    return MockModel()

def draw_detection(draw, det, image_height, color):
    x1, y1, x2, y2 = det["bbox"]
    label = f"{det['class']} ({det['confidence']})"
    
    draw.rectangle([x1, y1, x2, y2], outline=color, width=3)

    font_size = max(15, int(image_height * 0.02))
    font = ImageFont.load_default(size=font_size)

    text_bbox = draw.textbbox((x1, y1), label, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    label_x1 = x1
    label_y1 = y1 - text_height - 8 
    label_x2 = x1 + text_width + 8
    label_y2 = y1

    if label_y1 < 0:
        label_y1 = y1
        label_y2 = y1 + text_height + 8

    draw.rectangle([label_x1, label_y1, label_x2, label_y2], fill=color)
    draw.text((label_x1 + 4, label_y1 + 4), label, fill="white", font=font)

st.title("Brand Logo Detector")
st.caption("SZTE IMN104L-2025/26/1-IMN104L-2")

st.write("The brand logo detector tries to find logos from an image which can be uploaded below. To see a list of brands the application can recognise, visit the Supported Brands page from navigation.")
st.write("")

model = load_model()

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    with st.spinner("Generating output...", show_time=True):
        image = Image.open(uploaded_file)
        detections = model.predict(image)
        classes = []
        draw = ImageDraw.Draw(image)
        
        for i, det in enumerate(detections):
            classes.append(f"{det['class']} ({det['confidence']})")
            draw_detection(draw, det, image.height, BBOX_COLORS[i % len(BBOX_COLORS)])

        st.write(f"Found the following classes (with confidence): {", ".join(classes)}")
        st.image(image, caption="Output", width="content")