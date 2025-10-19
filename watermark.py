import io
from PIL import Image
import streamlit as st

# ==============================
# APP CONFIG
# ==============================
st.set_page_config(page_title="Watermark Adder", page_icon="💧", layout="wide")

# ==============================
# HEADER SECTION
# ==============================
st.markdown(
    """
    <h1 style="text-align:center; color:#00B4D8;">💧 Batch Watermark Adder</h1>
    <p style="text-align:center; color:gray; font-size:18px;">
        Made by <b style="color:#0096c7;">Garv</b> for <b style="color:#ff4d6d;">Davneet</b>
    </p>
    <hr style="border: 1px solid #00B4D8;">
    """,
    unsafe_allow_html=True
)

st.markdown(
    "Upload multiple photos, pick a watermark, adjust size live, and preview all results instantly. Download each watermarked image individually. 🚀"
)

# ==============================
# UPLOADS
# ==============================
uploaded_images = st.file_uploader(
    "📸 Upload Multiple Photos",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

watermark_file = st.file_uploader(
    "💦 Upload Watermark Image",
    type=["png", "jpg", "jpeg"]
)

scale = st.slider("🔍 Adjust Watermark Size (Live Preview)", 
                  min_value=0.05, max_value=0.5, value=0.2, step=0.01)

# ==============================
# PREVIEW WATERMARK (RESIZING)
# ==============================
if watermark_file:
    watermark = Image.open(watermark_file).convert("RGBA")
    w, h = watermark.size
    wm_resized = watermark.resize((int(w * scale * 3), int(h * scale * 3)))
    bg = Image.new("RGBA", (400, 250), (240, 240, 240, 255))
    pos = ((bg.width - wm_resized.width) // 2, (bg.height - wm_resized.height) // 2)
    bg.alpha_composite(wm_resized, pos)
    st.image(bg, caption="💧 Watermark Preview (Resizes with Slider)", use_column_width=False)
else:
    st.warning("Please upload a watermark image to continue.")

# ==============================
# APPLY WATERMARK & SHOW RESULTS
# ==============================
if uploaded_images and watermark_file:
    st.markdown("### 🖼️ Watermarked Image Previews")

    cols = st.columns(2)  # show 2 per row
    col_index = 0

    watermark = Image.open(watermark_file).convert("RGBA")

    for idx, file in enumerate(uploaded_images):
        base = Image.open(file).convert("RGBA")

        # Resize watermark
        w, h = watermark.size
        wm_resized = watermark.resize((int(w * scale), int(h * scale)))

        # Position bottom-right
        b_w, b_h = base.size
        position = (b_w - wm_resized.width - 10, b_h - wm_resized.height - 10)

        # Composite watermark
        base.alpha_composite(wm_resized, position)

        # Convert to Bytes for display/download
        img_bytes = io.BytesIO()
        base.convert("RGB").save(img_bytes, format="JPEG")
        img_bytes.seek(0)

        # Display preview in columns
        with cols[col_index]:
            st.image(base.convert("RGB"), caption=f"Preview - {file.name}", use_column_width=True)
            st.download_button(
                label=f"⬇️ Download {file.name}",
                data=img_bytes,
                file_name=f"watermarked_{file.name}",
                mime="image/jpeg",
                key=f"download_{idx}"
            )

        # Alternate between columns
        col_index = (col_index + 1) % 2

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; color:gray;">
        <b>⚙️ Built with ❤️ by Garv for Davneet — Streamlit Watermark Tool v3.0</b>
    </div>
    """,
    unsafe_allow_html=True
)
