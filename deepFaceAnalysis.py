import cv2
import glob
from deepface import DeepFace
import pandas as pd
import shutil


age_model = DeepFace.build_model("Age")
gender_model = DeepFace.build_model("Gender")
race_model = DeepFace.build_model("Race")
emotion_model = DeepFace.build_model("Emotion")

models = {"age" : age_model,
          "gender" : gender_model,
          "race" : race_model,
          "emotion" : emotion_model
}

def deepFaceAnalysis(detected_faces_path):

    age_list = []
    gender_list = []
    race_list = []
    emotion_list = []

    # Pass all images through DeepFace
    for detected_face in glob.glob(detected_faces_path + '*.jpg'):
        image_face = cv2.imread(detected_face)
        face_feature = DeepFace.analyze(image_face, actions = ['age', 'gender', 'race', 'emotion'], models=models, enforce_detection=False)
        age_list.append(face_feature["age"])
        gender_list.append(face_feature["gender"])
        race_list.append(face_feature["dominant_race"])
        emotion_list.append(face_feature["dominant_emotion"])

    face_df = pd.DataFrame(list(zip(age_list, gender_list, race_list, emotion_list)), columns=['age', 'gender', 'race', 'emotion'])

    shutil.rmtree(detected_faces_path)

    return face_df