import cv2
import os
from pathlib import Path

def faceDetect(file_name):

    casc_path = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(casc_path)

    img = cv2.imread(file_name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(30, 30),
    )

    # Remove images without faces
    if (len(faces) == 0):
        os.remove(file_name)

    # Crop out faces
    for i, (x, y, w, h) in enumerate(faces):
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        faces = img[y:y + h, x:x + w]
        cv2.imshow("face", faces)

        file_head = os.path.split(file_name)[0]
        file_tail = os.path.splitext(os.path.split(file_name)[1])[0]

        face_path_head = os.path.join(file_head, file_tail + '_faces/')
        face_path_tail =  file_tail + '_' + str(i) + '.jpg'

        face_path = face_path_head + face_path_tail

        Path(face_path_head).mkdir(parents=True, exist_ok=True)

        # Export cropped faces
        cv2.imwrite(face_path, faces)

