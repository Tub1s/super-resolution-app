from pyrsistent import b
from streamlit.uploaded_file_manager import UploadedFile
import streamlit as st
import cv2
import numpy as np

from io import BytesIO
from typing import List, Union

def read_data(data: UploadedFile) -> BytesIO:
    """Convert UploadedFile to bytes and return as BytesIO"""
    return BytesIO(data.getvalue())

def upscale(data: UploadedFile, algorithm: Union[str, List[str]], upscaling_ratio: float) -> BytesIO:
    """
    Function performs upscaling on input imagefile by applying chosen upscaling method.

    Args:
        data (UploadedFile): object containing image data
        algorithm (Union[str, List[str]]): specifies upscaling method(s)
        upscaling_ratio (float): ratio between output and input images

    Returns:
        BytesIO: upscaled image in byte format
    """
    result = read_data(data=data)
    return result
