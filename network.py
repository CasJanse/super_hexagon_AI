import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense, Conv2D, Flatten, MaxPool2D, Dropout
from keras.optimizers import Adam, SGD


def create_model():
    model = Sequential()
    model.add(Conv2D(256, 3, activation="relu", input_shape=(128, 72, 1)))
    model.add(MaxPool2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))
    model.add(Conv2D(128, 3, activation="relu"))
    model.add(MaxPool2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(2, activation="sigmoid"))
    mutate_weights(model)
    return model


def save_weights(model, index):
    model.save("model_weights/model_{}.h5".format(index))


def load_weights(model_name):
    model = load_model("model_weights/{}.h5".format(model_name))
    return model


def mutate_weights(model):
    base_weights = model.get_weights()
    print(base_weights)
    pass
