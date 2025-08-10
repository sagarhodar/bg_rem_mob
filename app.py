import streamlit as st
from rembg import remove
from PIL import Image
import io
from streamlit_extras.add_vertical_space import add_vertical_space

st.set_page_config(page_title="Background Remover", page_icon="✂️", layout="wide")

st.title("🖼️ Remove Background")
st.divider()

col1, col2 = st.columns(2)

with st.sidebar:
    st.markdown("### Upload Images")
    images = st.file_uploader(
        "Choose images", 
        accept_multiple_files=True, 
        type=['png', 'jpg', 'jpeg', 'webp']
    )
    add_vertical_space(16)
    st.markdown("Made with ❤️ by [Parimal Hodar]")

if images:
    for idx, image in enumerate(images):
        try:
            with Image.open(image) as img:
                # Ensure image is in RGB mode
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                col1.subheader(f"Original {idx + 1}")
                col1.image(img, use_container_width=True)

                with st.spinner(f'Removing background from image {idx + 1}...'):
                    # Remove background
                    output = remove(img)
                
                # The newer versions of rembg return PIL Images directly
                if isinstance(output, Image.Image):
                    output_image = output
                else:
                    # Handle bytes or other formats
                    try:
                        output_image = Image.open(io.BytesIO(output))
                    except:
                        st.error(f"Failed to process image {idx + 1}")
                        continue
                
                col2.subheader(f"Background Removed {idx + 1}")
                col2.image(output_image, use_container_width=True)
                
                # Create download button
                output_stream = io.BytesIO()
                output_image.save(output_stream, format="PNG")
                output_stream.seek(0)
                
                filename = f"no_bg_{image.name.split('.')[0]}.png"
                col2.download_button(
                    label=f"📥 Download Image {idx + 1}",
                    data=output_stream.getvalue(),
                    file_name=filename,
                    mime="image/png",
                    key=f"download_{idx}"
                )
                
        except Exception as e:
            st.error(f"Error processing image {idx + 1}: {str(e)}")
else:
    st.info("👆 Upload some images using the sidebar to get started!")