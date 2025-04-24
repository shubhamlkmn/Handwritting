import os
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import font_manager
from fpdf import FPDF
from PIL import Image

FONT_DIR = "fonts"
IMAGE_OUTPUT = "output.png"
PDF_OUTPUT = "handwritten_output.pdf"

def list_fonts():
    return [f for f in os.listdir(FONT_DIR) if f.endswith(".ttf")]

def render_text_to_image(text, font_path, output_image=IMAGE_OUTPUT):
    fig, ax = plt.subplots(figsize=(8.5, 11))  # Letter size
    plt.axis('off')
    font_prop = font_manager.FontProperties(fname=font_path, size=16)
    ax.text(0.05, 0.95, text, fontproperties=font_prop, va='top', wrap=True)
    plt.savefig(output_image, bbox_inches='tight', dpi=300)
    plt.close()

def image_to_pdf(image_path, pdf_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.image(image_path, x=0, y=0, w=210, h=297)  # A4 page size in mm
    pdf.output(pdf_path)

# ------------------------ Streamlit App ------------------------
st.set_page_config(page_title="Text to Handwriting", layout="centered")
st.title("📝 Convert Text to Handwriting")
st.markdown("Type your text below, choose a handwriting font, and download it as a PDF!")

text_input = st.text_area("Enter your text here", height=300)

fonts = list_fonts()
if not fonts:
    st.error("⚠️ No fonts found! Please add .ttf handwriting fonts to the `fonts/` directory.")
    st.stop()

selected_font = st.selectbox("Choose a handwriting font", fonts)

if st.button("Generate Handwriting"):
    font_path = os.path.join(FONT_DIR, selected_font)
    render_text_to_image(text_input, font_path)
    st.success("✅ Handwriting generated!")

    image = Image.open(IMAGE_OUTPUT)
    st.image(image, caption="Handwritten Preview", use_column_width=True)

    image_to_pdf(IMAGE_OUTPUT, PDF_OUTPUT)
    with open(PDF_OUTPUT, "rb") as f:
        st.download_button("📥 Download as PDF", f, file_name=PDF_OUTPUT, mime="application/pdf")
