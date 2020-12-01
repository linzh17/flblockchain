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
from CnnModel import CnnModel
from AlexNetModel import AlexNetModel
from event import EventCallbackImpl01
from contractFactory import ContractFactory
from fastdfs import Fdfs


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

# Generator to "flow" in the input images and labels into our model
# Takes batch_size as a parameter
'''
train_generator = gen.flow(X_train, y_train, batch_size=BATCH_SIZE)
test_generator = test_gen.flow(X_test, y_test, batch_size=BATCH_SIZE)

size = X_train.shape[0]
C1 = AlexNetModel(train_generator,test_generator,size,BATCH_SIZE,EPOCHS)
C1.start()

for i in range(1,6):
    print(i)
'''
contract_factory = ContractFactory()
fdfs = Fdfs()


def start_client(i):
    print("start client")
    train = X_train[(i-1)*12000:i*12000]
    y = y_train[(i-1)*12000:i*12000]
    size = train.shape[0]

    train_generator = gen.flow(train, y, batch_size=BATCH_SIZE)
    model = CnnModel(train_generator,size,BATCH_SIZE,EPOCHS)
    client = Client(i,model,contract_factory,fdfs)
    client.start()


if __name__ == '__main__':
    start_client(3)
    

        # threading.Thread(target=start_client).start()

