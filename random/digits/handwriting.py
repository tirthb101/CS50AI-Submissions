import sys
import tensorflow as tf
from sklearn.model_selection import train_test_split
import numpy as np

(X_train, Y_train), (X_test, Y_test) = tf.keras.datasets.mnist.load_data()

X_train, X_test = X_train / 255.0, X_test / 255.0

Y_train = tf.keras.utils.to_categorical(Y_train)
Y_test = tf.keras.utils.to_categorical(Y_test)

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(
        filters=32, kernel_size=(3, 3), activation="relu", input_shape=(28, 28, 1)
    ),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    tf.keras.layers.Flatten(),

    tf.keras.layers.Dense(150, activation="relu"),
    tf.keras.layers.Dropout(0.5),


    tf.keras.layers.Dense(10, activation="softmax")

])


model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)


model.fit(X_train, Y_train, epochs=25)

print(model.evaluate(X_train, Y_train))


if len(sys.argv) == 2:
    model.save(sys.argv[1])
