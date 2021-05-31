import cv2
import os
from pathlib import Path

casc_path = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(casc_path)

def faceDetect(image, image_path):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(30, 30),
    )

    file_head = os.path.split(image_path)[0]
    file_tail = os.path.splitext(os.path.split(image_path)[1])[0]
    face_path_head = os.path.join(file_head, file_tail + '_faces/')

    face_count = 0

    if len(faces) > 0 :
        # Extract faces

        Path(face_path_head).mkdir(parents=True, exist_ok=True)

        for i, (x, y, w, h) in enumerate(faces):
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            faces = image[y:y + h, x:x + w]

            face_path_tail =  file_tail + '_' + str(i) + '.jpg'

            face_path = face_path_head + face_path_tail

            # Export cropped faces
            cv2.imwrite(face_path, faces)
            face_count = face_count + 1

    return face_count, face_path_head