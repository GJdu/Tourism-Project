import cv2
import glob
import pandas as pd
from faceDetect import faceDetect
from deepface import DeepFace


def deepFaceAnalysis(image_path):
    # Filter images with faces and store into a new folder
    for file_name in glob.glob(image_path + '/*.jpg'):
        faceDetect(file_name)

    face_list = []

    # Pass all images through DeepFace
    for image_name in glob.glob(image_path + '/*/*.jpg'):
        img = cv2.imread(image_name)

        face = DeepFace.analyze(img, actions = ['age', 'gender', 'race', 'emotion'], enforce_detection=False, )
        face_list.append([face["age"], face["gender"], face["dominant_race"],face["dominant_emotion"]])

    # Store results in DataFrame
    face_df = pd.DataFrame(face_list, columns=['age', 'gender', 'race', 'emotion'])

    # Export to CSV
    face_df.to_csv(r'face_dataframe.csv', index = True, header=True)