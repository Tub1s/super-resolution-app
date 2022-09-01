import streamlit as st
import matplotlib.pyplot as plt

def show_home_page():
    st.title("Welcome to the Super Resolution Application!")
    st.write("This application lets you upload up to 200MB of pictures and upscale them using multitude of techniques and algorithms!")
    st.write("List of currently available algorithms is as follows:")
    st.write("Nearest Neighbour, Bilinear, Bicubic, Lanczos4, ESRGAN (custom training) and ConvT (custom model).")
    