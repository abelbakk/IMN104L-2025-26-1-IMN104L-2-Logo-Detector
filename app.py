import streamlit as st
from PIL import Image, ImageDraw
from model.mock_model import MockModel

st.set_page_config(page_title="Brand Logo Detector", layout="centered", menu_items=None)

st.markdown(
    r"""
    <style>
    .stAppDeployButton {
            visibility: hidden;
        }
    </style>
    """, unsafe_allow_html=True
)

@st.cache_resource
def load_model():
    return MockModel()

model = load_model()

st.header("Logo detector")
st.caption("SZTE IMN104L-2025/26/1-IMN104L-2")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    with st.spinner("Generating output...", show_time=True):
        image = Image.open(uploaded_file)
        detections = model.predict(image)
        classes = []
        draw = ImageDraw.Draw(image)
        
        for det in detections:
            classes.append(f"{det['class']} ({det['confidence']})")
            x1, y1, x2, y2 = det["bbox"]
            draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
            draw.text((x1, y1 - 10), f"{det['class']} ({det['confidence']})", fill="red", font_size=20) # TODO: font size probably has to be adaptive

        st.write(f"Found the following classes (class (confidence)): {", ".join(classes)}")
        st.image(image, caption="Output", width="content")