import os
import sys
import numpy as np
from cv2 import resize

# Clone repo at https://github.com/GKalliatakis/Keras-VGG16-places365
PLACES_PATH = '/Users/brian/Documents/GitHub/Keras-VGG16-places365'
sys.path.insert(1, PLACES_PATH)

from vgg16_places_365 import VGG16_Places365

def locationDetect(image):
    image = np.array(image, dtype=np.uint8)
    image = resize(image, (224, 224))
    image = np.expand_dims(image, 0)

    model = VGG16_Places365(weights='places')
    predictions_to_return = 5
    preds = model.predict(image)[0]
    top_preds = np.argsort(preds)[::-1][0:predictions_to_return]

    # load the class label
    file_name = os.path.join(PLACES_PATH, 'categories_places365.txt')
    if not os.access(file_name, os.W_OK):
        synset_url = 'https://raw.githubusercontent.com/csailvision/places365/master/categories_places365.txt'
        os.system('wget ' + synset_url)
    classes = list()
    with open(file_name) as class_file:
        for line in class_file:
            classes.append(line.strip().split(' ')[0][3:])
    classes = tuple(classes)

    # output the prediction
    return classes[top_preds[0]]


