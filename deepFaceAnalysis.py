import cv2
import glob
from deepface import DeepFace
import pandas as pd
import shutil

def deepFaceAnalysis(detected_faces_path):

    age_list = []
    gender_list = []
    race_list = []
    emotion_list = []

    # Pass all images through DeepFace
    for detected_face in glob.glob(detected_faces_path + '*.jpg'):
        image_face = cv2.imread(detected_face)
        face_feature = DeepFace.analyze(image_face, actions = ['age', 'gender', 'race', 'emotion'], enforce_detection=False, )
        age_list.append(face_feature["age"])
        gender_list.append(face_feature["gender"])
        race_list.append(face_feature["dominant_race"])
        emotion_list.append(face_feature["dominant_emotion"])

    face_df = pd.DataFrame(list(zip(age_list, gender_list, race_list, emotion_list)), columns=['age', 'gender', 'race', 'emotion'])

    shutil.rmtree(detected_faces_path)

    return face_df