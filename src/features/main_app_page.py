import streamlit as st
from streamlit_image_comparison import image_comparison
from features.scaling import upscale
from cv2 import INTER_LINEAR, INTER_CUBIC, INTER_NEAREST, INTER_LANCZOS4
import itertools


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
    
    #! Code responsible for processing data
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
                            
                            show_results = True

        
        # TODO: Maybe add original picture side by side comparison
        #! Code responsible for displaying all results
        with st.container():
            st.header("Results")
            if not show_results:
                st.write('There are no results to display, yet!')

            else:
                # If only one algorithm was applied, display results for all images
                if len(choices) < 2:
                    for file in uploaded_files:
                        st.image(result_images[choices[0]][file.name], 
                                caption=f"Image {file.name.split('.')[0]} upscaled using {choices[0]} method \
                                        by factor of {upscaling_ratio}")
                        st.write("\n")

                # Display all possible comparisons of algorithms
                else:
                    # Calculate all possible unique comparisons
                    all_permutations = list(itertools.permutations(choices, 2))
                    all_permutations = [sorted(d_p) for d_p in all_permutations]
                    final_permutations = list()
                    for perm in all_permutations:
                        if perm not in final_permutations:
                            final_permutations.append(perm)

                    # Itarate over all selected files and display comparison of algorithms
                    for file in uploaded_files:
                        st.subheader(f"Image: {file.name}")
                        for disp_perm in final_permutations:
                            with st.expander(label=f"{disp_perm[0]} vs {disp_perm[1]}"):
                                image_comparison(result_images[disp_perm[0]][file.name], 
                                                    result_images[disp_perm[1]][file.name],
                                                    label1=disp_perm[0],
                                                    label2=disp_perm[1])
                            st.write("\n")
                    