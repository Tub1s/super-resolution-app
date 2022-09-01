from this import d
from streamlit.uploaded_file_manager import UploadedFile
import streamlit as st
import cv2
import numpy as np
import torch
import os
from PIL import Image
from torchvision import transforms
import features.esrgan as esrgan
import tensorflow as tf

import numpy as np
from torch.autograd import Variable

from io import BytesIO
from typing import List, Union

import copy
import features.convt as convt

def read_data(data: UploadedFile) -> np.ndarray:
    """Convert UploadedFile to bytes and return as np.ndarray"""
    data_stream = BytesIO(data.getvalue())
    result = np.asarray(bytearray(data_stream.read()), dtype=np.uint8)

    return result

def upscale(data: UploadedFile, algorithm: Union[int, str], 
            upscaling_ratio: float) -> np.ndarray:
    """
    Function performs upscaling on input imagefile by applying chosen upscaling method.

    Args:
        data (UploadedFile): object containing image data
        algorithm (Union[int, str]): specifies upscaling method(s); CV2 -> int, TF2 -> str
        upscaling_ratio (float): ratio between output and input images

    Returns:
        BytesIO: upscaled image in byte format
    """

    # TODO: Add support for none cv2 upscale options


    if type(algorithm) == int:
        img_array = read_data(data=data)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        img_org = copy.deepcopy(img)
        img = cv2.resize(img, (int(img.shape[1]/upscaling_ratio), int(img.shape[0]/upscaling_ratio)),
                         interpolation = cv2.INTER_AREA)
        img = cv2.resize(img, None, fx=upscaling_ratio, 
                        fy=upscaling_ratio, interpolation=algorithm)
        
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    else: 
        if algorithm == "ESRGAN":
            img_array = read_data(data=data)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            img_org = copy.deepcopy(img)
            img = cv2.resize(img, (int(img.shape[1]/upscaling_ratio), int(img.shape[0]/upscaling_ratio)),
                         interpolation = cv2.INTER_AREA)
            img = image_super_resolution(esrgan.ESRGAN_MODEL_PATH, img)

        if algorithm == "convt":
            img_array = read_data(data=data)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            img_org = copy.deepcopy(img)
            img = cv2.resize(img, (int(img.shape[1]/upscaling_ratio), int(img.shape[0]/upscaling_ratio)),
                         interpolation = cv2.INTER_AREA)
            
            img = convt_super_resolution(convt.CONVT_MODEL_PATH, img)
            img = img * 255
            img = img.astype('uint8')
    return img, img_org


def convt_super_resolution(model_path: str, image):
    dim = image.shape
    dim = (1, dim[0], dim[1], dim[2])
    image = image[np.newaxis, ...]
    print(f"img_shape: {image.shape}")
    
    dim = (image.shape[1], image.shape[2], image.shape[3])
    print(f"layer_dim: {dim}")
    model = convt.convt(dim)
    model.load_weights(model_path)
    output_img = model.predict(image)

    return output_img[0]


def image_super_resolution(model_path: str, image):
    # means = [np.mean(image[:,:][i]) for i in range(image.shape[-1])]
    # stds = [np.std(image[:,:][i]) for i in range(image.shape[-1])]
    # print(means)
    # print(stds)
    channels = 3
    residual_blocks = 23

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Define model and load model checkpoint
    generator = esrgan.GeneratorRRDB(channels, filters=64,
                              num_res_blocks=residual_blocks).to(device)
    generator.load_state_dict(torch.load(model_path))
    generator.eval()
    
    
    transform = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize(esrgan.ESRGAN_MEAN, esrgan.ESRGAN_STD)])
    # transform = transforms.Compose(
    #     [transforms.ToTensor(), transforms.Normalize(means, stds)])
    # Prepare input
    image_tensor = Variable(transform(image)
                            ).to(device).unsqueeze(0)

    # Upsample image
    with torch.no_grad():
        sr_image = esrgan.denormalize(generator(image_tensor)).cpu().numpy()
        sr_image = np.moveaxis(sr_image[0], 0, 2)
        sr_image = cv2.cvtColor(sr_image, cv2.COLOR_BGR2RGB)
        sr_image = sr_image*255
        sr_image = sr_image.astype("uint8") 

    return sr_image
