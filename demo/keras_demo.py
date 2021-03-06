from tensorflow.keras.datasets import mnist
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras import callbacks

import numpy as np

import mltb.keras

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

train_5_labels = []

for lab in train_labels:
    if lab == 5:
        train_5_labels.append(1)
    else:
        train_5_labels.append(0)

train_5_labels = np.asarray(train_5_labels)

test_5_labels = []

for lab in test_labels:
    if lab == 5:
        test_5_labels.append(1)
    else:
        test_5_labels.append(0)

test_5_labels = np.asarray(test_5_labels)

train_images = train_images.reshape((60000, 28 * 28))
train_images = train_images.astype('float32') / 255

test_images = test_images.reshape((10000, 28 * 28))
test_images = test_images.astype('float32') / 255

train_images = train_images[:1000]
test_images = test_images[:1000]
train_5_labels = train_5_labels[:1000]
test_5_labels = test_5_labels[:1000]

network = models.Sequential()
network.add(layers.Dense(100, activation='relu', input_shape=(28 * 28,)))
network.add(layers.Dense(100, activation='relu'))
network.add(layers.Dense(1, activation='sigmoid'))

network.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

mltb_callback = mltb.keras.BinaryClassifierMetricsCallback(test_images, test_5_labels, 1)
es = callbacks.EarlyStopping(monitor='roc_auc', patience=5,  mode='max')

history = network.fit(train_images, train_5_labels, verbose=1, epochs=400,
                      batch_size=128,
                      #validation_data=(test_images, test_5_labels),
                      callbacks=[mltb_callback, es],
                      class_weight={0: 1.0, 1: 9.0},
                      )

print(history.history)
