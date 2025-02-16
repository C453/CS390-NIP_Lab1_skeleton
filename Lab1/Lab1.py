
import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.utils import to_categorical
import random

random.seed(1618)
np.random.seed(1618)
tf.random.set_seed(1618)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
#os.environ['CUDA_VISIBLE_DEVICES'] = '3'
#ALGORITHM = "guesser"
ALGORITHM = "tf_net"
#ALGORITHM = "tf_conv"

#DATASET = "mnist_d"
#DATASET = "mnist_f"
#DATASET = "cifar_10"
#DATASET = "cifar_100_f"
DATASET = "cifar_100_c"

if DATASET == "mnist_d":
    NUM_CLASSES = 10
    IH = 28
    IW = 28
    IZ = 1
    IS = 784
elif DATASET == "mnist_f":
    NUM_CLASSES = 10
    IH = 28
    IW = 28
    IZ = 1
    IS = 784
elif DATASET == "cifar_10":
    NUM_CLASSES = 10
    IH = 32
    IW = 32
    IZ = 3
    IS = 1024
elif DATASET == "cifar_100_f":
    NUM_CLASSES = 100
    IH = 32
    IW = 32
    IZ = 3
    IS = 1024
elif DATASET == "cifar_100_c":
    NUM_CLASSES = 20
    IH = 32
    IW = 32
    IZ = 3
    IS = 1024

#=========================<Classifier Functions>================================

def guesserClassifier(xTest):
    ans = []
    for entry in xTest:
        pred = [0] * NUM_CLASSES
        pred[random.randint(0, 9)] = 1
        ans.append(pred)
    return np.array(ans)

def buildTFNeuralNet(x, y, xTest, yTest, eps = 6):
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(512, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(NUM_CLASSES, activation=tf.nn.softmax))
    model.compile(optimizer="adam", loss=tf.keras.losses.CategoricalCrossentropy(), metrics=['accuracy'])
    model.fit(x, y, validation_data=(xTest, yTest), epochs=eps)
    return model

def buildTFConvNet(x, y, xTest, yTest, eps = 10, dropout = True, dropRate = 0.2):
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Conv2D(16, kernel_size=(3,3), activation=tf.nn.leaky_relu, input_shape=(IW, IH, IZ), padding='same'))
    model.add(tf.keras.layers.Conv2D(16, kernel_size=(3,3), activation=tf.nn.leaky_relu, padding='same'))
    model.add(tf.keras.layers.BatchNormalization())

    model.add(tf.keras.layers.Conv2D(32, kernel_size=(3,3), activation=tf.nn.leaky_relu, padding='same'))
    model.add(tf.keras.layers.Conv2D(32, kernel_size=(3,3), activation=tf.nn.leaky_relu, padding='same'))
    model.add(tf.keras.layers.BatchNormalization())

    model.add(tf.keras.layers.Conv2D(64, kernel_size=(3,3), activation=tf.nn.leaky_relu, padding='same'))
    model.add(tf.keras.layers.Conv2D(64, kernel_size=(3,3), activation=tf.nn.leaky_relu, padding='same'))
    model.add(tf.keras.layers.BatchNormalization())

    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2), strides=(2,2), data_format='channels_last'))

    model.add(tf.keras.layers.Conv2D(128, kernel_size=(3,3), activation=tf.nn.leaky_relu, padding='same'))
    model.add(tf.keras.layers.Conv2D(128, kernel_size=(3,3), activation=tf.nn.leaky_relu, padding='same'))
    model.add(tf.keras.layers.BatchNormalization())

    model.add(tf.keras.layers.Conv2D(256, kernel_size=(3,3), activation=tf.nn.leaky_relu, padding='same'))
    model.add(tf.keras.layers.Conv2D(256, kernel_size=(3,3), activation=tf.nn.leaky_relu, padding='same'))

    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2), strides=(2,2), data_format='channels_last'))

    model.add(tf.keras.layers.Conv2D(512, kernel_size=(3,3), activation=tf.nn.leaky_relu, padding='same'))
    model.add(tf.keras.layers.Conv2D(512, kernel_size=(3,3), activation=tf.nn.leaky_relu, padding='same'))
    model.add(tf.keras.layers.BatchNormalization())

    model.add(tf.keras.layers.Conv2D(512, kernel_size=(3,3), activation=tf.nn.leaky_relu, padding='same'))
    model.add(tf.keras.layers.Conv2D(512, kernel_size=(3,3), activation=tf.nn.leaky_relu, padding='same'))
    model.add(tf.keras.layers.BatchNormalization())

    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2), strides=(2,2), data_format='channels_last'))

    model.add(tf.keras.layers.Flatten())

    model.add(tf.keras.layers.Dropout(dropRate))
    model.add(tf.keras.layers.Dense(64, activation=tf.nn.leaky_relu))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.Dropout(dropRate))

    model.add(tf.keras.layers.Dense(512, activation=tf.nn.leaky_relu))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.Dropout(dropRate))
    model.add(tf.keras.layers.Dense(NUM_CLASSES, activation=tf.nn.softmax))

    sgd = keras.optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)

    model.compile(optimizer=sgd, loss=tf.keras.losses.CategoricalCrossentropy(), metrics=['accuracy'])

    model.fit(x, y, validation_data=(xTest, yTest), epochs=eps, batch_size = 32, callbacks=[keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True), keras.callbacks.ReduceLROnPlateau(patience=2)])
    return model

#=========================<Pipeline Functions>==================================

def getRawData():
    if DATASET == "mnist_d":
        mnist = tf.keras.datasets.mnist
        (xTrain, yTrain), (xTest, yTest) = mnist.load_data()
    elif DATASET == "mnist_f":
        mnist = tf.keras.datasets.fashion_mnist
        (xTrain, yTrain), (xTest, yTest) = mnist.load_data()
    elif DATASET == "cifar_10":
        cifar = tf.keras.datasets.cifar10
        (xTrain, yTrain), (xTest, yTest) = cifar.load_data()
    elif DATASET == "cifar_100_f":
        cifar = tf.keras.datasets.cifar100
        (xTrain, yTrain), (xTest, yTest) = cifar.load_data(label_mode='fine')
    elif DATASET == "cifar_100_c":
        cifar = tf.keras.datasets.cifar100
        (xTrain, yTrain), (xTest, yTest) = cifar.load_data(label_mode='coarse')
    else:
        raise ValueError("Dataset not recognized.")
    print("Dataset: %s" % DATASET)
    print("Shape of xTrain dataset: %s." % str(xTrain.shape))
    print("Shape of yTrain dataset: %s." % str(yTrain.shape))
    print("Shape of xTest dataset: %s." % str(xTest.shape))
    print("Shape of yTest dataset: %s." % str(yTest.shape))
    return ((xTrain, yTrain), (xTest, yTest))


def preprocessData(raw):
    ((xTrain, yTrain), (xTest, yTest)) = raw

    xTrain = xTrain.astype(np.float32) / 255.
    xTest = xTest.astype(np.float32) / 255.
    
    if ALGORITHM != "tf_conv":
        xTrainP = xTrain.reshape((xTrain.shape[0], IS, IZ))
        xTestP = xTest.reshape((xTest.shape[0], IS, IZ))
    else:
        xTrainP = xTrain.reshape((xTrain.shape[0], IH, IW, IZ))
        xTestP = xTest.reshape((xTest.shape[0], IH, IW, IZ))
    yTrainP = to_categorical(yTrain, NUM_CLASSES)
    yTestP = to_categorical(yTest, NUM_CLASSES)
    print("New shape of xTrain dataset: %s." % str(xTrainP.shape))
    print("New shape of xTest dataset: %s." % str(xTestP.shape))
    print("New shape of yTrain dataset: %s." % str(yTrainP.shape))
    print("New shape of yTest dataset: %s." % str(yTestP.shape))
    return ((xTrainP, yTrainP), (xTestP, yTestP))

def trainModel(data, test):
    xTrain, yTrain = data
    xTest, yTest = test
    if ALGORITHM == "guesser":
        return None   # Guesser has no model, as it is just guessing.
    elif ALGORITHM == "tf_net":
        print("Building and training TF_NN.")
        return buildTFNeuralNet(xTrain, yTrain, xTest, yTest, 20)
    elif ALGORITHM == "tf_conv":
        print("Building and training TF_CNN.")
        return buildTFConvNet(xTrain, yTrain, xTest, yTest, 100, True, 0.2)
    else:
        raise ValueError("Algorithm not recognized.")

def runModel(data, model):
    if ALGORITHM == "guesser":
        return guesserClassifier(data)
    elif ALGORITHM == "tf_net":
        print("Testing TF_NN.")
        preds = model.predict(data)
        for i in range(preds.shape[0]):
            oneHot = [0] * NUM_CLASSES
            oneHot[np.argmax(preds[i])] = 1
            preds[i] = oneHot
        return preds
    elif ALGORITHM == "tf_conv":
        print("Testing TF_CNN.")
        data = np.array(data).astype(np.float32)
        preds = model.predict(data)
        for i in range(preds.shape[0]):
            oneHot = [0] * NUM_CLASSES
            oneHot[np.argmax(preds[i])] = 1
            preds[i] = oneHot
        return preds
    else:
        raise ValueError("Algorithm not recognized.")

def evalResults(data, preds):
    xTest, yTest = data
    acc = 0
    for i in range(preds.shape[0]):
        if np.array_equal(preds[i], yTest[i]):   acc = acc + 1
    accuracy = acc / preds.shape[0]
    print("Classifier algorithm: %s" % ALGORITHM)
    print("Classifier accuracy: %f%%" % (accuracy * 100))
    print()

#=========================<Main>================================================

def main():
    raw = getRawData()
    data = preprocessData(raw)
    model = trainModel(data[0], data[1])
    preds = runModel(data[1][0], model)
    evalResults(data[1], preds)

if __name__ == '__main__':
    main()
