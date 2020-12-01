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

class AlexNetModel():
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

        # 1st Convolutional Layer
        model.add(Conv2D(filters=32, input_shape=(28, 28, 1), kernel_size=(3, 3), strides=(1, 1), padding='valid'))
        model.add(Activation('relu'))
        # Max Pooling
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(1, 1), padding='valid'))

        # 2nd Convolutional Layer
        model.add(Conv2D(filters=32, kernel_size=(3, 3), strides=(1, 1), padding='valid'))
        model.add(Activation('relu'))
        # Max Pooling
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(1, 1), padding='valid'))

        # 3rd Convolutional Layer
        model.add(Conv2D(filters=64, kernel_size=(3, 3), strides=(1, 1), padding='valid'))
        model.add(Activation('relu'))

        # 4th Convolutional Layer
        model.add(Conv2D(filters=64, kernel_size=(3, 3), strides=(1, 1), padding='valid'))
        model.add(Activation('relu'))

        # Max Pooling
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding='valid'))

        # Fully Connected layer
        model.add(Flatten())
        # 1st Fully Connected Layer
        model.add(Dense(512))
        model.add(Activation('relu'))
        # Add Dropout to prevent overfitting
        model.add(Dropout(0.3))

        # Output Layer
        # important to have dense 10, since we have 10 classes
        model.add(Dense(10))
        model.add(Activation('softmax'))
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
'''
(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_train = X_train.reshape(60000, 28, 28, 1)
X_test = X_test.reshape(10000, 28, 28, 1)
X_train = X_train[0:1000]
X_test = X_test[0:1000]
y_train = y_train[0:1000]
y_test = y_test[0:1000]

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
train_generator = gen.flow(X_train, y_train, batch_size=BATCH_SIZE)
test_generator = test_gen.flow(X_test, y_test, batch_size=BATCH_SIZE)

size = X_train.shape[0]
C1 = AlexNetModel(train_generator,test_generator,size,BATCH_SIZE,EPOCHS)
C1.start()
weights = C1.weights
weights = np.array(weights)
print(weights.shape)
print(weights)
weights = weights-weights
print(weights)
'''

'''
C2 = AlexNetModel(train_generator,test_generator,BATCH_SIZE,EPOCHS)
C2.start()
weights1 = C1.weights
weights2 = C2.weights
weights1 = np.array(weights1)
weights2 = np.array(weights2)
weights = (weights1+weights2)/2
weights = weights.tolist()
C1.set_weights(weights)
C2.set_weights(weights)
C1.start()
C2.start()
'''

'''
weights = C1.weights
weights = pickle.dumps(weights)
weights = pickle.loads(weights)
C1.set_weights(weights)
C1.start()
'''