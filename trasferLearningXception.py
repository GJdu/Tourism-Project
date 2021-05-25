import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import os

image_size = (150, 150)

# Load model
def getModel():
    model = keras.models.load_model("tourism_model")
    return model

# Retrain model
def trainModel():
    os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'

    batch_size = 32

    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        "/Users/brian/Desktop/BISITE/ImageDateSet",
        labels="inferred",
        label_mode="int",
        validation_split=0.2,
        subset="training",
        seed=1337,
        image_size=image_size,
        batch_size=batch_size,
    )
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        "/Users/brian/Desktop/BISITE/ImageDateSet",
        labels="inferred",
        label_mode="int",
        validation_split=0.2,
        subset="validation",
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
    outputs = keras.layers.Dense(1)(x)
    model = keras.Model(inputs, outputs)

    model.compile(optimizer=keras.optimizers.Adam(),
                  loss=keras.losses.BinaryCrossentropy(from_logits=True),
                  metrics=[keras.metrics.BinaryAccuracy()])
    model.fit(train_ds, epochs=20, validation_data=val_ds)

    # Fine-tuning model
    base_model.trainable = True
    model.summary()

    model.compile(
        optimizer=keras.optimizers.Adam(1e-5),  # Low learning rate
        loss=keras.losses.BinaryCrossentropy(from_logits=True),
        metrics=[keras.metrics.BinaryAccuracy()],
    )

    epochs = 10
    model.fit(train_ds, epochs=epochs, validation_data=val_ds)

    # Creates a SavedModel
    model.save("tourism_model")

    return model

if os.path.exists("tourism_model"):
    model = getModel()
else:
    model = trainModel()

# Makes prediction
img = keras.preprocessing.image.load_img(
    "Spain-tourists.jpeg", target_size=image_size
)

img_array = keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)

predictions = model.predict(img_array)
score = predictions[0]

if (score > 0):
    print("Image is not an advertisement")
else:
    print("Image is an advertisement")