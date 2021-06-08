import cv2
import os
import glob
import numpy as np
from pathlib import Path
from PIL import Image

casc_path = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(casc_path)

def faceDetect(image, image_path):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
    )

    file_head = os.path.split(image_path)[0]
    file_tail = os.path.splitext(os.path.split(image_path)[1])[0]
    face_folder_path = os.path.join(file_head, file_tail + '_faces/')

    face_count = 0
    face_box = []

    if len(faces) > 0 :
        # Extract faces

        Path(face_folder_path).mkdir(parents=True, exist_ok=True)

        for i, (x, y, w, h) in enumerate(faces):
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            faces = image[y:y + h, x:x + w]

            face_path_tail =  file_tail + '_' + str(i) + '.jpg'

            face_path = face_folder_path + face_path_tail

            # Export cropped faces
            cv2.imwrite(face_path, faces)
            face_count = face_count + 1

            # Store contour box of faces
            face_box.append(np.array([x, y, w, h]))


    return face_count, face_folder_path, face_box

def personRatio (image_path):

    original_image = Image.open(image_path)
    original_image_width, original_image_height = original_image.size
    original_image_size = original_image_width * original_image_height

    img_list = []
    ratio_list = []

    detected_image_path = "Detected_" + image_path + "-objects" + "/*.jpg"
    for image in glob.glob(detected_image_path):
        if 'person' in image:
            img = Image.open(image)
            img_list.append(img)

    for image in img_list:
        width, height = image.size
        ratio = width * height / original_image_size
        ratio_list.append(ratio)

    return ratio_list