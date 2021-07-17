import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from kaggle.api.kaggle_api_extended import KaggleApi
import pickle5 as pickle
import shutil

image_size = (150, 150)
batch_size = 32

# Load model
def getModel(MODEL):
    model = keras.models.load_model(MODEL)
    return model

# Retrain model
def trainModel(model_name):
    api = KaggleApi()
    api.authenticate()

    api.dataset_download_files('jigrubhatt/selfieimagedetectiondataset', 'data/', unzip=True)

    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        "data/Selfie-Image-Detection-Dataset/Training_data",
        labels="inferred",
        label_mode="int",
        seed=1337,
        image_size=image_size,
        batch_size=batch_size,
    )
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        "data/Selfie-Image-Detection-Dataset/Validation_data",
        labels="inferred",
        label_mode="int",
        seed=1337,
        image_size=image_size,
        batch_size=batch_size,
    )

    base_model = keras.applications.Xception(
        weights='imagenet',  # Load weights pre-trained on ImageNet.
        input_shape=(150, 150, 3),
        include_top=False)

    base_model.trainable = False

    data_augmentation = keras.Sequential(
        [
            layers.experimental.preprocessing.RandomFlip("horizontal"),
            layers.experimental.preprocessing.RandomRotation(0.1),
            layers.experimental.preprocessing.RandomZoom(0.3, 0.3),
            layers.experimental.preprocessing.RandomTranslation(0.2, 0.2),
        ]
    )

    inputs = keras.Input(shape=(150, 150, 3))
    x = data_augmentation(inputs)  # Apply random data augmentation

    norm_layer = keras.layers.experimental.preprocessing.Normalization()
    mean = np.array([127.5] * 3)
    var = mean ** 2

    # Scale inputs to [-1, +1]
    x = norm_layer(x)
    norm_layer.set_weights([mean, var])

    # We make sure that the base_model is running in inference mode here,
    # by passing `training=False`.
    x = base_model(x, training=False)

    # Convert features of shape `base_model.output_shape[1:]` to vectors
    x = keras.layers.GlobalAveragePooling2D()(x)

    # A Dense classifier with a single unit (binary classification)
    x = keras.layers.Dropout(0.2)(x)  # Regularize with dropout
    outputs = keras.layers.Dense(1, activation="sigmoid")(x)
    model = keras.Model(inputs, outputs)

    model.compile(optimizer=keras.optimizers.Adam(),
                  loss=keras.losses.BinaryCrossentropy(from_logits=True),
                  metrics=[keras.metrics.BinaryAccuracy()])
    train_history = model.fit(train_ds, epochs=20, validation_data=val_ds)

    # Save training history as a dictionary
    with open('/trainHistoryDict', 'wb') as file_pi:
        pickle.dump(train_history.history, file_pi)

    # Fine-tuning model
    base_model.trainable = True
    model.summary()

    model.compile(
        optimizer=keras.optimizers.Adam(1e-5),  # Low learning rate
        loss=keras.losses.BinaryCrossentropy(from_logits=True),
        metrics=[keras.metrics.BinaryAccuracy()],
    )

    epochs = 10
    fine_tuning_history = model.fit(train_ds, epochs=epochs, validation_data=val_ds)

    # Save fine tuning history as dictionary
    with open('/fineTuningHistoryDict', 'wb') as file_pi:
        pickle.dump(fine_tuning_history.history, file_pi)

    # Creates a SavedModel
    model.save(model_name)

    # Remove used data
    shutil.rmtree("data/Selfie-Image-Detection-Dataset")

    return model

def detectSelfie(model, image_path):
    # Makes prediction
    img = keras.preprocessing.image.load_img(image_path, target_size=image_size)

    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    predictions = model.predict(img_array)
    score = predictions[0]
    if (score > 0.5):
        return True
    else:
        return False

# Test code
# # MODEL = "Models/final_detectSelfie_model"
# MODEL = "/Users/brian/ml/DetectSelfie/detectSelfieWithFilterRemoval_model"
# model = getModel(MODEL)
# detectSelfie(model=model, image_path="/Users/brian/Desktop/Screen Shot 2021-06-27 at 11.12.17 am.png")