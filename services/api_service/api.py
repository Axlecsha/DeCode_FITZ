from fastapi import (
    APIRouter, 
    Request, 
    HTTPException,
    Body,
)

from typing import List

router = APIRouter(
    prefix="/ai",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)



import os
import json

import pandas as pd
import numpy as np

import tensorflow as tf
import keras

from sklearn.preprocessing import MinMaxScaler
import joblib


BASENAME = os.path.basename(__file__)
PATH = os.path.abspath(__file__).replace(BASENAME, "")
SERIES_LENGTH = 64


@router.post("/generate_next_31")
async def generate_next_31(args: List[float] = Body(...)):
    file = np.array(args).astype(np.float32).reshape(-1, 1)

    inputs = keras.layers.Input(shape=(64, 1))

    hide = keras.layers.LSTM(64, return_sequences=True)(inputs)
    hide = keras.layers.LSTM(64, return_sequences=False)(hide)

    outputs = keras.layers.Dense(1, activation=keras.activations.sigmoid)(hide)

    model = keras.Model(inputs=inputs, outputs=outputs)
    model.summary()
    
    def metric_abs(y_true, y_pred):
        return tf.math.abs(1.0 - y_true / y_pred)

    model.compile(optimizer=keras.optimizers.Adam(0.01), loss=metric_abs, metrics=[keras.losses.mean_absolute_error])

    es_callback = keras.callbacks.EarlyStopping(
        monitor="loss",
        min_delta=0.001,
        patience=50,
        restore_best_weights=True
    )

    modelckpt_callback = keras.callbacks.ModelCheckpoint(
        monitor="loss",
        filepath=os.path.join(PATH, "AI_data", "model_3.weights.h5"),
        verbose=1,
        save_weights_only=True,
        save_best_only=True,
    )

    scaler = joblib.load(os.path.join(PATH, "AI_data", "scaler.gz"))

    def transform(rows):
        X, y = [], []

        rows = scaler.transform(rows)

        for it in range(SERIES_LENGTH, len(rows)):

            X.append(rows[it - SERIES_LENGTH : it])
            y.append(rows[it])

        return X, y


    def predict_next(rows, count):
        X = scaler.transform(rows[ - SERIES_LENGTH :])
        result = []

        for it in range(count):

            new_row = model.predict(X.reshape(1, -1, 1), verbose=0)[0]

            result.append(new_row)

            X = np.concatenate([X[1 :], [new_row]])

        if len(result) != 0:
            result = scaler.inverse_transform(result)

        return np.array(result)


    X, y = transform(file)

    X = np.array(X)
    y = np.array(y)

    model.load_weights(modelckpt_callback.filepath)

    model.fit(
        X, y,
        epochs=1,
        shuffle=True,
        callbacks=[es_callback],
        batch_size=30
    )

    y = scaler.inverse_transform(y)
    y_pred = scaler.inverse_transform(model.predict(np.array(X)))

    y_new = predict_next(file, 31)

    return {
        "y": list(y.reshape(-1).astype(float)),    
        "y_pred": list(y_pred.reshape(-1).astype(float)),    
        "y_new": list(y_new.reshape(-1).astype(float)),    
    }

