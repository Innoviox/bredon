from keras.models import Sequential
from keras.layers import Dense

import pickle

xtrain, ytrain, xtest, ytest = pickle.load('features.pickle')

model = Sequential()

model.add(Dense(64, input_dim=512, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(84, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X, Y, epochs=150, batch_size=10)

scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
