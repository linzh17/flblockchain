import numpy as np


# load MNIST dataset
from keras.datasets import mnist

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.optimizers import Adam
from keras.layers.normalization import BatchNormalization
from keras.utils import np_utils
from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D, GlobalAveragePooling2D
# from keras.layers.advanced_activations import LeakyReLU
from keras.preprocessing.image import ImageDataGenerator
import keras
import pickle

import multiprocessing
import threading


from Client import Client
from AlexNetModel import AlexNetModel
from event import EventCallbackImpl01
from contractFactory import ContractFactory
from CnnModel import CnnModel
contract_factory = ContractFactory()

# 导入数据集
(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_train = X_train.reshape(60000, 28, 28, 1)
X_test = X_test.reshape(10000, 28, 28, 1)


# Normalize to float between 0 and 1
# Original pixel values are between 0 and 255
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train = X_train / 255
X_test = X_test / 255

classes = 10
y_train = np_utils.to_categorical(y_train, classes)
y_test = np_utils.to_categorical(y_test, classes)


gen = ImageDataGenerator(
            rotation_range=8,
            width_shift_range=0.08,
            shear_range=0.3,
            height_shift_range=0.08,
            zoom_range=0.08
            )
test_gen = ImageDataGenerator()

# hyoer-parameters
# We train in batches to speed up the process
# (and so that our memory can handle the data)
BATCH_SIZE = 64
# How many rounds of training? Let's start from a smaller number
EPOCHS = 1

Gmodel = contract_factory.getGmodel()
print(Gmodel.contractAddress)
m_gen = gen.flow(X_train[0:1000], y_train[0:1000], batch_size=BATCH_SIZE)
m = CnnModel(m_gen,1000,BATCH_SIZE,EPOCHS)
m.start()
print(m.weights)
Gmodel.set(pickle.dumps(m.weights))
