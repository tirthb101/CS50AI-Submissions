import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split


df = pd.read_csv("banknotes.csv")

X = df[["variance", "skewness", "curtosis", "entropy"]].values
Y = df["class"].values


x_train, x_test, y_train,  y_test = train_test_split(X, Y, test_size=0.1)

model = tf.keras.models.Sequential()


model.add(tf.keras.layers.Dense(10, activation='relu'))

model.add(tf.keras.layers.Dense(1, activation="sigmoid"))

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.fit(x_train, y_train, epochs=20)

print(model.evaluate(x_test, y_test, verbose=2))
