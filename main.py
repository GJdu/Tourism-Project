import glob
import cv2
import os
import pandas as pd
from deepFaceAnalysis import deepFaceAnalysis
from landmarkDetect import landmarkDetect
from imageAIDetect import personDetect
from trasferLearningXception import detectSelfie

IMAGES_PATH = "FOTOS-Sample"

# Initialise list place holder
image_id = []
person_count = []
face_count = []
deepface_info = []
scene_type = []
selfie = []

for image_path in glob.glob(IMAGES_PATH + '/*.jpg'):

    print(image_path)

    image_id.append(os.path.splitext(os.path.split(image_path)[1])[0])

    # Load image dataset
    image = cv2.imread(image_path)

    numberPersons = personDetect(image_path)
    person_count.append(numberPersons)

    # Perform deepface analysis
    numberFaces, face_df = deepFaceAnalysis(image_path)
    face_count.append(numberFaces)
    deepface_info.append(face_df)

    # Analysis location type
    scene_type.append(landmarkDetect(image))

    if numberFaces > 0:
        selfie.append(detectSelfie(image_path))
    else:
        selfie.append("False")

# Save extracted information to a csv file
output_df = pd.DataFrame(list(zip(image_id, person_count,face_count, deepface_info, scene_type, selfie)), columns=["image id", "person count", "face count", "deepface", "scene type", "selfie"])
output_df.to_csv(r'Output.csv', index = False, header=True)