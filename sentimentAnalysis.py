from tensorflow import keras
import tensorflow as tf
import re
import string

MODEL = "sentiment_analysis_model"

import re
import string

@tf.keras.utils.register_keras_serializable()
def custom_standardization(input_data):
    lowercase = tf.strings.lower(input_data)
    stripped_html = tf.strings.regex_replace(lowercase, '', ' ')
    return tf.strings.regex_replace(stripped_html,
    '[%s]' % re.escape(string.punctuation), '')

# Load model
def getModel():
    model = keras.models.load_model(MODEL)
    return model

def getPolaity(model, string):
    # Makes prediction
    input=[string]
    return model.predict(input)

model = getModel()
print(getPolaity(model=model, string="Ali is so cool and amazing!!!!"))