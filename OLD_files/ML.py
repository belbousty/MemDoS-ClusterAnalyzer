import time
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D

class TimingCallback(tf.keras.callbacks.Callback):
    def __init__(self):
        self.times = []
        self.total_time = 0

    def on_batch_begin(self, batch, logs=None):
        self.start_time = time.time()

    def on_batch_end(self, batch, logs=None):
        end_time = time.time()
        self.times.append(end_time - self.start_time)
        self.total_time += end_time - self.start_time
        print('\nTime taken for this batch: ', end_time - self.start_time, 'seconds')

timing_callback = TimingCallback()

def main():
        start_time = time.time() 
        (x_train, y_train), (x_test, y_test) = mnist.load_data()

 
        x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
        x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
        input_shape = (28, 28, 1)

        x_train = x_train.astype('float32') / 255
        x_test = x_test.astype('float32') / 255

        y_train = tf.keras.utils.to_categorical(y_train, 10)
        y_test = tf.keras.utils.to_categorical(y_test, 10)

        model = Sequential()
        model.add(Conv2D(4, kernel_size=(3, 3), activation='relu', input_shape=input_shape))
        model.add(Conv2D(8, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(10, activation='softmax'))

        model.compile(loss=tf.keras.losses.categorical_crossentropy,
                      optimizer=tf.keras.optimizers.Adam(),
                      metrics=['accuracy'])

        model.fit(x_train, y_train,
                  batch_size=128,
                  epochs=1,
                  verbose=0, 
                  validation_data=(x_test, y_test),
                  callbacks=[timing_callback])

        end_time = time.time()

        print('Time taken for this iteration:', end_time - start_time, 'seconds')

if __name__ == '__main__':
    main()
