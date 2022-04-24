from pyrsistent import b
from streamlit.uploaded_file_manager import UploadedFile
import streamlit as st
import cv2
import numpy as np

from io import BytesIO
from typing import List, Union

def read_data(data: UploadedFile) -> np.ndarray:
    """Convert UploadedFile to bytes and return as np.ndarray"""
    data_stream = BytesIO(data.getvalue())
    result = np.asarray(bytearray(data_stream.read()), dtype=np.uint8)

    return result

def upscale(data: UploadedFile, algorithm: Union[str, List[str]], 
            upscaling_ratio: float) -> np.ndarray:
    """
    Function performs upscaling on input imagefile by applying chosen upscaling method.

    Args:
        data (UploadedFile): object containing image data
        algorithm (Union[str, List[str]]): specifies upscaling method(s)
        upscaling_ratio (float): ratio between output and input images

    Returns:
        BytesIO: upscaled image in byte format
    """

    # TODO: Add support for none cv2 upscale options

    img_array = read_data(data=data)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    img = cv2.resize(img, None, fx=upscaling_ratio, 
                     fy=upscaling_ratio, interpolation=algorithm)
    
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img
