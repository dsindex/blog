#!/bin/env python

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD
import numpy as np

## model configuration
model = Sequential()
# Dense(64) is a fully-connected layer with 64 hidden units.
# in the first layer, you must specify the expected input data shape:
# here, 20-dimensional vectors.
model.add(Dense(64, input_dim=20, init='uniform'))
model.add(Activation('tanh'))
model.add(Dropout(0.5))
model.add(Dense(64, init='uniform'))
model.add(Activation('tanh'))
model.add(Dropout(0.5))
model.add(Dense(10, init='uniform'))
model.add(Activation('softmax'))
sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd)
              
## generate train/test data
X_train = []
y_train = []
for i in xrange(10000) :
    x = np.random.uniform(-1, 1, size=20)
    y = [i % 10]
    X_train.append(x)
    y_train.append(y)
X_train = np.array(X_train)
y_train = np.array(y_train)
print "X_train shape = " + str(X_train.shape)
print "y_train shape = " + str(y_train.shape)
X_test = []
y_test = []
for i in xrange(1000) :
    x = np.random.uniform(-1, 1, size=20)
    y = [i % 10]
    X_test.append(x)
    y_test.append(y)
X_test = np.array(X_test)
y_test = np.array(y_test)
print "X_test shape = " + str(X_test.shape)
print "y_test shape = " + str(y_test.shape)

## training and evalutation
model.fit(X_train, y_train,
          nb_epoch=20,
          batch_size=100,
          show_accuracy=True)
score = model.evaluate(X_test, y_test, batch_size=100, show_accuracy=True)
