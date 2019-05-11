from keras.models import Sequential, load_model
from keras.layers import Dense

import pickle
import numpy as np

from model import *
from coerce import *

xtrain, ytrain, xtest, ytest = pickle.load(open('/Volumes/External Hard Drive/tak.pickle', 'rb'))

def normalized(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2==0] = 1
    return a / np.expand_dims(l2, axis)

def train():
    model = Sequential()

    model.add(Dense(50, input_dim=512, activation='relu'))
    model.add(Dense(25, activation='relu'))
    model.add(Dense(84, activation='sigmoid'))

    model.summary()

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(xtrain, ytrain, epochs=10, batch_size=10)

    scores = model.evaluate(xtest, ytest)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

    model.save("/Volumes/External Hard Drive/tak.h5")

def test():
    model = load_model("/Volumes/External Hard Drive/tak.h5")
    for a, b in zip(model.predict(xtest), ytest):
        print(non_normal_vtm(list(a)))
        print(vector_to_move(list(b)))


train()