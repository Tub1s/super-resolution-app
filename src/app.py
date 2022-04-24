import streamlit as st

from features.home_page import show_home_page
from features.main_app_page import show_main_app_page


def main():
    page_sidebar = st.sidebar.selectbox("App Navigation", ("Home", "Application"), index=0)

    if page_sidebar == "Home":
        show_home_page()

    elif page_sidebar == "Application":
        show_main_app_page()

if __name__ == "__main__":
    main()

    



