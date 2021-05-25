# Requires python 3.7.6
# https://towardsdatascience.com/object-detection-with-10-lines-of-code-d6cb4d86f606

from imageai.Detection import ObjectDetection
from PIL import Image
import glob
import os

execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()

# Download this : https://github.com/OlafenwaMoses/ImageAI/releases/download/essentials-v5/resnet50_coco_best_v2.1.0.h5/
detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.1.0.h5"))
detector.loadModel()


def objectDetect (image_path):

    detections, extracted_images = detector.detectObjectsFromImage(input_image=os.path.join(execution_path, image_path), output_image_path=os.path.join(execution_path , "Detected_" + image_path), extract_detected_objects=True)
    for Object in detections:
        print(Object["name"] , " : " , Object["percentage_probability"] )

def personRatio (image_path):

    original_image = Image.open(image_path)
    original_image_width, original_image_height = original_image.size
    original_image_size = original_image_width * original_image_height

    img_list = []
    ratio_list = []

    detected_image_path = "Detected_" + image_path + "-objects" + "/*.jpg"
    for image in glob.glob(detected_image_path):
        if 'person' in image:
            img = Image.open(image)
            img_list.append(img)

    for image in img_list:
        width, height = image.size
        ratio = width * height / original_image_size
        ratio_list.append(ratio)

    return ratio_list

test_image = "Spain-tourists-2.jpeg"
objectDetect(test_image)
print(personRatio(test_image))