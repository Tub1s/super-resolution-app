import streamlit as st
import matplotlib.pyplot as plt

def show_home_page():
    st.title("Welcome to the Super Resolution Application!")
    st.write("This application lets you upload up to 200MB of pictures and upscale them using multitude of techniques and algorithms!")
    st.write("List of currently available algorithms is as follows:")
    st.write("Nearest Neighbour, Bilinear, Bicubic...")
    st.write("More algorithms coming in future!")

    st.subheader("How to use app?")
    st.write("To start using our application you must first go to 'Import Data' page and import images that you want to upscale!")
    st.write("Once you selected files that you want to work with proceed to 'Modify Data' page and start playing with your files!")
    st.write("After applying all modifications to images you can save results to your hard drive in 'Downloads' section!")