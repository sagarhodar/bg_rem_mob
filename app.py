import streamlit as st
from rembg import remove
from PIL import Image
import io
from streamlit_extras.add_vertical_space import add_vertical_space

# Set page config with mobile-friendly layout
st.set_page_config(
    page_title="Background Remover",
    page_icon="✂️",
    layout="centered",  # Use centered layout for better mobile display
    initial_sidebar_state="collapsed"  # Collapse sidebar by default on mobile
)

st.title("🖼️ Remove Background")
st.markdown("Upload images to remove their backgrounds instantly! Works best on PC and mobile.(by Sagar Hodar)")
st.divider()

# Move file uploader to main content for mobile accessibility
st.markdown("### Upload Images")
images = st.file_uploader(
    "Choose images",
    accept_multiple_files=True,
    type=['png', 'jpg', 'jpeg', 'webp'],
    help="Select one or more images to remove backgrounds."
)

# Add footer in sidebar
with st.sidebar:
    add_vertical_space(2)
    st.markdown("Made with ❤️ by [Parimal Hodar]")

if images:
    for idx, image in enumerate(images):
        try:
            with Image.open(image) as img:
                # Ensure image is in RGB mode
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Use a single column for mobile stacking
                st.subheader(f"Image {idx + 1}")
                col1, col2 = st.columns([1, 1])  # Equal width columns for better mobile scaling

                with col1:
                    st.markdown("**Original**")
                    st.image(img, use_container_width=True)

                with st.spinner(f'Removing background from image {idx + 1}...'):
                    # Remove background
                    output = remove(img)
                
                # Handle output format
                if isinstance(output, Image.Image):
                    output_image = output
                else:
                    try:
                        output_image = Image.open(io.BytesIO(output))
                    except:
                        st.error(f"Failed to process image {idx + 1}")
                        continue
                
                with col2:
                    st.markdown("**Background Removed**")
                    st.image(output_image, use_container_width=True)
                    
                    # Create download button
                    output_stream = io.BytesIO()
                    output_image.save(output_stream, format="PNG")
                    output_stream.seek(0)
                    
                    filename = f"no_bg_{image.name.split('.')[0]}.png"
                    st.download_button(
                        label=f"📥 Download Image {idx + 1}",
                        data=output_stream.getvalue(),
                        file_name=filename,
                        mime="image/png",
                        key=f"download_{idx}"
                    )
                
        except Exception as e:
            st.error(f"Error processing image {idx + 1}: {str(e)}")
else:
    st.info("👆 Upload some images to get started!")


