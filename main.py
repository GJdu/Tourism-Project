import glob
import cv2
import os
import pandas as pd
from deepFaceAnalysis import deepFaceAnalysis
from locationDetect import locationDetect
from imageAIDetect import personDetect
from detectSelfie import detectSelfie

IMAGES_PATH = "FOTOS-Sample"

# Initialise list place holder
image_id = []
person_count = []
face_count = []
age_list = []
gender_list = []
race_list = []
emotion_list = []
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
    numberFaces, age, gender, race, emotion = deepFaceAnalysis(image_path)
    face_count.append(numberFaces)
    age_list.append(age)
    gender_list.append(gender)
    race_list.append(race)
    emotion_list.append(emotion)

    # Analysis location type
    scene_type.append(locationDetect(image))

    if numberFaces > 0:
        selfie.append(detectSelfie(image_path))
    else:
        selfie.append("False")

# Save extracted information to a csv file
output_df = pd.DataFrame(list(zip(image_id, person_count,face_count, age_list, gender_list, race_list, emotion_list, scene_type, selfie)), columns=["image id", "person count", "face count", "age", "gender", "race", "emotion", "scene type", "selfie"])
output_df.to_csv(r'Output.csv', index = False, header=True)
output_df.to_excel("Output.xlsx", index = False)