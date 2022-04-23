import streamlit as st
from features.scaling import upscale
from cv2 import INTER_LINEAR, INTER_CUBIC, INTER_NEAREST, INTER_LANCZOS4
from PIL import Image 

def show_main_app_page():
    st.title("Application page")

    col1, col2 = st.columns(2)
    list_of_file_names = list()
    
    IMAGE_TYPES_LIST = [
    '.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'
    ]

    UPSCALING_ALGORITHMS = {'Bilinear': INTER_LINEAR, 
                          'Bicubic': INTER_CUBIC, 
                          'Nearest Neighbour': INTER_NEAREST, 
                          'Lanczos4': INTER_LANCZOS4}

    with col1:
        with st.expander("Import data"):
            uploaded_files = st.file_uploader(label = "Choose image files:", type = IMAGE_TYPES_LIST, accept_multiple_files=True)
            list_of_file_names = [file.name for file in uploaded_files]
            
        with st.container():
                files = st.multiselect("Choose files that you want to process: ", list_of_file_names)
                
                if files:
                    choice = st.multiselect("Choose algorithm you want to apply: ", UPSCALING_ALGORITHMS.keys())
                    upscaling_ratio = st.number_input("Upscaling ratio", min_value=1.0, max_value=4.0)

                    if choice:
                        uploaded_files = [file for file in uploaded_files if file.name in files]
        
                        if st.button(label='Apply'):
                            img = upscale(uploaded_files[0], UPSCALING_ALGORITHMS[choice[0]], upscaling_ratio)
                            #image = Image.open(image)
                            st.image(img)
    with col2:
        st.write("Test")
