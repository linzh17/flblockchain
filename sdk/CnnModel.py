


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

from keras import backend as K
import tensorflow as tf

class CnnModel():
    def __init__(self,train_generator,size,BATCH_SIZE,EPOCHS):
        self.model = self.build_model()
        self.weights = self.model.get_weights()
        self.train_generator =train_generator
        #self.test_generator = test_generator
        self.BATCH_SIZE = BATCH_SIZE
        self.EPOCHS = EPOCHS
        self.model_compile()
        self.size = size
    
    def  build_model(self):
        model = Sequential()
        model.add(Conv2D(32, kernel_size=(3, 3),
                         activation='relu',
                         input_shape=(28, 28, 1)))
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(10, activation='softmax'))

        return model 

    def set_weights(self,weights):
        self.model.set_weights(weights)

    def model_compile(self):    
        self.model.compile(loss=keras.losses.categorical_crossentropy, optimizer='adam', metrics=['accuracy'])

    def model_train(self):
        self.model.fit_generator(
                                    self.train_generator,
                                    steps_per_epoch=self.size/self.BATCH_SIZE,
                                    epochs=self.EPOCHS,
                                    #validation_data=self.test_generator,
                                    #validation_steps=10000//self.BATCH_SIZE
                                    )
    def model_info(self):
        self.model.summary()
    def start(self):
        self.model_info()
        
        self.model_train()
        
