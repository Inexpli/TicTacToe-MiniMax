import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

# initializing data
data = pd.read_csv('tictactoe.csv')

# preparing data
X = data.iloc[:, :-1].fillna(0).values
y = data['Winner'].values

# reformat results for tensorflow
y[y == -1] = 2  # Transformation -1 to 2, to be able to use sparse_categorical_crossentropy

# model definition
model = Sequential([
    Dense(128, input_dim=9, activation='relu'),
    Dropout(0.2),
    Dense(64, activation='relu'),
    Dense(3, activation='softmax')
])

# model compilation
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# early stopping
early_stopping = EarlyStopping(monitor='loss', patience=2, restore_best_weights=True)

# model training
history = model.fit(X, y, epochs=10, batch_size=32, verbose=1, callbacks=[early_stopping])

# saving
model.save('tictactoe_model.h5')
