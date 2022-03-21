import streamlit as st
from features.home_page import show_home_page
from features.import_data_page import show_import_data_page
from features.modify_data_page import show_modify_data_page
from features.download_data_page import show_download_data_page

page_sidebar = st.sidebar.selectbox("App Navigation", ("Home", "Load data", "Test algorithms", "Download"), index=0)

if page_sidebar == "Home":
    show_home_page()

elif page_sidebar == "Load data":
    show_import_data_page()

elif page_sidebar == "Test algorithms":
    show_modify_data_page()

elif page_sidebar == "Download":
    show_download_data_page()

