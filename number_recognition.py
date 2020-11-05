import numpy as np
import os
from keras.models import Sequential, load_model
from keras.layers import Dense, Conv2D, Flatten, MaxPool2D, Dropout
from keras.optimizers import Adam, SGD
import cv2


def create_model():
    model = Sequential()
    model.add(Dense(1056, activation="relu", input_shape=(32, 33)))
    model.add(Flatten())
    model.add(Dense(10, activation="softmax"))
    model.compile(loss="categorical_crossentropy", optimizer=Adam())
    return model


def save_weights(model):
    dir = "number_recognition"
    index = len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))])
    model.save("number_recognition/model_{}.h5".format(index))


def get_number_data():
    images = []
    expected_output = np.zeros((10, 10))
    files = [name for name in os.listdir("numbers") if os.path.isfile(os.path.join("numbers", name))]
    for i, file in enumerate(files):
        image = cv2.imread("numbers/{}".format(file))
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        images.append(image)
        expected_output[i][i] = 1
    return images, expected_output
