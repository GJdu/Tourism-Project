import glob
import cv2
import os
import pandas as pd
from faceDetect import faceDetect
from deepFaceAnalysis import deepFaceAnalysis
from landmarkDetect import landmarkDetect

IMAGES_PATH = "FOTOS-Sample"

# Initialise list place holder
image_id = []
face_count = []
deepface_info = []
scene_type = []
selfie = []

for image_path in glob.glob(IMAGES_PATH + '/*.jpg'):

    image_id.append(os.path.splitext(os.path.split(image_path)[1])[0])

    # Load image dataset
    image = cv2.imread(image_path)

    # Extract Faces
    numberFaces, detected_faces_path = faceDetect(image, image_path)
    face_count.append(numberFaces)

    if numberFaces > 0 :
        face_df = deepFaceAnalysis(detected_faces_path)
        deepface_info.append(face_df)
    else:
        deepface_info.append("None")

    scene_type.append(landmarkDetect(image))

output_df = pd.DataFrame(list(zip(image_id, face_count, deepface_info, scene_type)), columns=["image id", "face count", "deepface", "scene type"])
output_df.to_csv(r'Output.csv', index = True, header=True)


