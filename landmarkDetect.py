#https://www.kaggle.com/rsmits/keras-landmark-or-non-landmark-identification

import os
import sys
from urllib.request import urlopen
import numpy as np
from PIL import Image
from cv2 import resize

PLACES_PATH = '/Users/brian/Documents/GitHub/Keras-VGG16-places365'
sys.path.insert(1, PLACES_PATH)

from vgg16_places_365 import VGG16_Places365

# TEST_IMAGE_URL = 'https://www.tripsavvy.com/thmb/sDAA4e7a5OLdzABTIpskD_HXK04=/400x0/filters:no_upscale():max_bytes(150000):strip_icc()/view-of-plaza--square--mayor-534494095-59b427aad963ac0011bde759.jpg'
# image = Image.open(urlopen(TEST_IMAGE_URL))

def landmarkDetect(image):
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


