import streamlit as st
import numpy as np
import cv2
import scaling
from PIL import Image 


@st.cache
def load_image(image_file):
    img = Image.open(image_file)
    return img

def show_main_app_page():
    st.title("Application page")

    col1, col2 = st.columns(2)
    list_of_file_names = list()
    
    IMAGE_TYPES_LIST = [
    '.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'
    ]

    LIST_OF_ALGORITHMS = ['Bilinear', 'Bicubic']

    with col1:
        with st.expander("Import data"):
            uploaded_files = st.file_uploader(label = "Choose image files:", type = IMAGE_TYPES_LIST, accept_multiple_files=True)
            list_of_file_names = [file.name for file in uploaded_files]
            
        with st.container():
                files = st.multiselect("Choose files that you want to process: ", list_of_file_names)
                
                if files:
                    choice = st.multiselect("Choose algorithm you want to apply: ", LIST_OF_ALGORITHMS)

                    if choice:
                        uploaded_files = [file for file in uploaded_files if file.name in files]
                        st.button("This is button!")

                #for file in uploaded_files:
                    #st.write(f"{file.name}")
            
                #st.write(os.path.join("/data/external/", file.name))
                #with open(file.name, 'wb') as f:
                    #f.write(file.getbuffer())
                #st.success("Saved File!")

    with col2:
        st.write("Hehe")
