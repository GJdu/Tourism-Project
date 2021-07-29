from deepface import DeepFace
from retinaface import RetinaFace

# Need to install the latest mtcnn at: https://github.com/ipazc/mtcnn

def buildDeepFaceModels():
    age_model = DeepFace.build_model("Age")
    gender_model = DeepFace.build_model("Gender")
    race_model = DeepFace.build_model("Race")
    emotion_model = DeepFace.build_model("Emotion")

    deepface_models = {"age" : age_model,
              "gender" : gender_model,
              "race" : race_model,
              "emotion" : emotion_model
              }

    return deepface_models

def buildRetinaModel():
    retina_model = RetinaFace.build_model()

    return retina_model

def removeBackgroundFaces(faces, threshold=0.2):
    size = []
    for face in faces:
        size.append(face.size)

    max_size = max(size)

    discard_list =[]

    for i, face in enumerate(faces):
        if face.size < max_size * threshold:
            discard_list.append(i)

    for i in reversed(discard_list):
        faces.pop(i)
    return faces

def deepFaceAnalysis(retina_model, deepface_models, image_path):
    age_list = {}
    gender_list = {}
    race_list = {}
    emotion_list = {}

    # Pass all images through DeepFace
    faces = RetinaFace.extract_faces(image_path, model=retina_model)

    if len(faces) > 0:
        if len(faces) > 1:
            removeBackgroundFaces(faces)

        for i, face in enumerate(faces, start=1):
            dict = "face_" + str(i)
            face_feature = DeepFace.analyze(face, actions = ['age', 'gender', 'race', 'emotion'], models=deepface_models, enforce_detection=False)
            age_list[dict] = (face_feature["age"])
            gender_list[dict] = (face_feature["gender"])
            race_list[dict] = (face_feature["dominant_race"])
            emotion_list[dict] = (face_feature["dominant_emotion"])

        return len(faces), age_list, gender_list, race_list, emotion_list
    else:
        return 0, "None", "None", "None", "None"
