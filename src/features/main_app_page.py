import streamlit as st
from features.streamlit_juxtapose import juxtapose
from features.scaling import upscale
from cv2 import INTER_LINEAR, INTER_CUBIC, INTER_NEAREST, INTER_LANCZOS4
from PIL import Image 

def show_main_app_page():
    IMAGE_TYPES_LIST = [
    '.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'
    ]

    UPSCALING_ALGORITHMS = {'Bilinear': INTER_LINEAR, 
                          'Bicubic': INTER_CUBIC, 
                          'Nearest Neighbour': INTER_NEAREST, 
                          'Lanczos4': INTER_LANCZOS4}

    st.title("Application page")

    list_of_file_names = list()
    show_results = False
    

    with st.container():
        with st.expander("Import data"):
            uploaded_files = st.file_uploader(label = "Choose image files:", type = IMAGE_TYPES_LIST, accept_multiple_files=True)
            list_of_file_names = [file.name for file in uploaded_files]
            
        with st.container():
                files = st.multiselect("Choose files that you want to process: ", list_of_file_names)
                
                if files:
                    choices = st.multiselect("Choose algorithm you want to apply: ", UPSCALING_ALGORITHMS.keys())
                    upscaling_ratio = st.number_input("Upscaling ratio", min_value=1.0, max_value=4.0, step=1.0)

                    if choices:
                        uploaded_files = [file for file in uploaded_files if file.name in files]
        
                        if st.button(label='Apply'):
                            result_images = {key: dict() for key in choices}

                            
                            for uploaded_file in uploaded_files:
                                for choice in choices:
                                    result_images[choice][uploaded_file.name] = upscale(data = uploaded_file, 
                                                                    algorithm = UPSCALING_ALGORITHMS[choice], 
                                                                    upscaling_ratio = upscaling_ratio)

                            st.success('Data have been sucessfully processed!')
                            show_results = True


        # TODO: Add juxtapose scrolling comparisons
        with st.container():
            if show_results:
                for uploaded_file in uploaded_files:
                    for choice in choices:
                        st.image(result_images[choice][uploaded_file.name])