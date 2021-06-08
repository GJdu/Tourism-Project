# Requires python 3.7.6
# https://towardsdatascience.com/object-detection-with-10-lines-of-code-d6cb4d86f606

from imageai.Detection import ObjectDetection
from imageai.Prediction.Custom import CustomImagePrediction
from PIL import Image
import glob
import os

os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'

execution_path = os.getcwd()

# Download this : https://github.com/OlafenwaMoses/ImageAI/releases/download/essentials-v5/resnet50_coco_best_v2.1.0.h5/
humanDetector = ObjectDetection()
humanDetector.setModelTypeAsRetinaNet()
humanDetector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.1.0.h5"))
humanDetector.loadModel()

actionDetector = CustomImagePrediction()
actionDetector.setModelPath( os.path.join(execution_path , "action_net_ex-060_acc-0.745313.h5"))
actionDetector.setJsonPath("/Users/brian/Documents/GitHub/Action-Net/model_class.json")
actionDetector.loadFullModel(num_objects=16)

def objectDetect (image_path):

    detections, extracted_images = humanDetector.detectObjectsFromImage(input_image=os.path.join(execution_path, image_path), output_image_path=os.path.join(execution_path , "Detected_" + image_path), extract_detected_objects=True)
    for Object in detections:
        print(Object["name"] , " : " , Object["percentage_probability"] )

def personDetect (image_path):

    file_head = os.path.split(image_path)[0]
    file_tail = os.path.splitext(os.path.split(image_path)[1])[0]
    face_path_head = os.path.join(file_head, file_tail + '_detected')

    custom_objects = humanDetector.CustomObjects(person=True)
    detections = humanDetector.detectObjectsFromImage(custom_objects=custom_objects,
                                                       input_image=image_path,
                                                       output_image_path=face_path_head + '.jpeg',
                                                       minimum_percentage_probability=70)
    # Count number of people present
    return len(detections)

def detectAction (image_path):
    predictions, probabilities = actionDetector.classifyImage(image_input=image_path, result_count=3)

    return predictions, probabilities

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

# test_image = "/Users/brian/Documents/GitHub/Action-Net/images/3.jpg"
# # print(str(personDetect(test_image)))
#
# predictions, probabilities  = detectAction(test_image)
#
# for prediction, probability in zip(predictions, probabilities):
#     print(prediction, " : ", probability)