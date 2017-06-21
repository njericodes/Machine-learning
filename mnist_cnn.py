#simple cnn for mnist

import numpy 
from keras.datasets import mnist
from keras.models import Sequential 
from keras.layers import Dense
from keras.layers import Dropout 
from keras.layers import Flatten 
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils

from keras import backend as K
K.set_image_dim_ordering('th')


seed = 7
numpy.random.seed(seed)

(X_train, Y_train), (X_test, Y_test) = mnist.load_data()

num_pixels = X_train.shape[1]*X_train.shape[2]
X_train = X_train.reshape(X_train.shape[0], 1, 28, 28).astype('float32')
X_test = X_test.reshape(X_test.shape[0], 1, 28, 28).astype('float32')

#normalize 
X_train = X_train/255
X_test = X_test/255

Y_train = np_utils.to_categorical(Y_train)
Y_test = np_utils.to_categorical(Y_test)
num_classes = Y_test.shape[1]

def baseline_model():
    model = Sequential()
    
    #cnn
    model.add(Conv2D(32, (5,5), input_shape=(1, 28, 28), activation='relu'))
    
    #pooling
    model.add(MaxPooling2D(pool_size=(2,2)))
    
     #cnn
    model.add(Conv2D(64, (5,5), input_shape=(1, 28, 28), activation='relu'))
    
    #pooling
    model.add(MaxPooling2D(pool_size=(2,2)))
    
    model.add(Dropout(0.2))
    model.add(Flatten())
    
    #fully connected layer
    model.add(Dense(1024, activation='relu'))
    
    #output layer
    model.add(Dense(num_classes, activation='softmax'))
    
    #compile
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    return model
    
#build the model
model = baseline_model()
model.fit(X_train, Y_train, validation_data=(X_test, Y_test), epochs=10, batch_size=200, verbose=0)
scores = model.evaluate(X_test, Y_test, verbose=0)
print("Error: %.2f%%" % (scores[1]*100))
