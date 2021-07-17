# https://towardsdatascience.com/object-detection-with-10-lines-of-code-d6cb4d86f606

import os
from paths import ROOT_DIR
from imageai.Detection import ObjectDetection

# Download this : https://github.com/OlafenwaMoses/ImageAI/releases/download/essentials-v5/resnet50_coco_best_v2.1.0.h5/
humanDetector = ObjectDetection()
humanDetector.setModelTypeAsRetinaNet()
humanDetector.setModelPath(os.path.join(ROOT_DIR , "Models/resnet50_coco_best_v2.1.0.h5"))
humanDetector.loadModel()

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
                                                       minimum_percentage_probability=80)
    os.remove(face_path_head + '.jpeg')
    # Count number of people present
    return len(detections)