import keras
from keras.datasets import cifar100
from keras.models import Sequential
from keras.layers import Conv2D, UpSampling2D, MaxPooling2D, Conv2DTranspose
import matplotlib.pyplot as plt
import numpy as np
import cv2

CONVT_MODEL_PATH = "/home/senuki/university_coding/super-resolution-app/models/ConvT/convt.h5"

def convt(dim):
  print(dim)

  model = Sequential()
  model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', kernel_initializer='he_normal', input_shape=dim))
  model.add(Conv2D(16, kernel_size=(3, 3), activation='relu', kernel_initializer='he_normal'))
  model.add(Conv2D(8, kernel_size=(3, 3), activation='relu', kernel_initializer='he_normal'))
  model.add(Conv2DTranspose(8, kernel_size=(3,3), activation='relu', kernel_initializer='he_normal'))
  model.add(Conv2DTranspose(16, kernel_size=(3,3), activation='relu', kernel_initializer='he_normal'))
  model.add(Conv2DTranspose(16, kernel_size=(3,3), activation='relu', kernel_initializer='he_normal'))
  model.add(Conv2DTranspose(32, kernel_size=(2,2), strides=(2,2), activation='relu', kernel_initializer='he_normal'))
  model.add(Conv2DTranspose(32, kernel_size=(2,2), strides=(2,2), activation='relu', kernel_initializer='he_normal'))
  model.add(Conv2DTranspose(32, kernel_size=(3,3), activation='relu', kernel_initializer='he_normal'))
  model.add(Conv2D(3, kernel_size=(3, 3), activation='linear', padding='same'))
  model.summary()
  return model

