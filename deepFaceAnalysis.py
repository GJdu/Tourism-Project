from deepface import DeepFace
from retinaface import RetinaFace

# Need to install the latest mtcnn at: https://github.com/ipazc/mtcnn

age_model = DeepFace.build_model("Age")
gender_model = DeepFace.build_model("Gender")
race_model = DeepFace.build_model("Race")
emotion_model = DeepFace.build_model("Emotion")

retina_model = RetinaFace.build_model()

models = {"age" : age_model,
          "gender" : gender_model,
          "race" : race_model,
          "emotion" : emotion_model
          }

def deepFaceAnalysis(image_path):
    age_list = {}
    gender_list = {}
    race_list = {}
    emotion_list = {}

    # Pass all images through DeepFace
    faces = RetinaFace.extract_faces(image_path, model=retina_model)

    if len(faces) > 0:
        for i, face in enumerate(faces, start=1):
            dict = "face_" + str(i)
            face_feature = DeepFace.analyze(face, actions = ['age', 'gender', 'race', 'emotion'], models=models, enforce_detection=False)
            age_list[dict] = (face_feature["age"])
            gender_list[dict] = (face_feature["gender"])
            race_list[dict] = (face_feature["dominant_race"])
            emotion_list[dict] = (face_feature["dominant_emotion"])

        return len(faces), age_list, gender_list, race_list, emotion_list
    else:
        return 0, "None", "None", "None", "None"