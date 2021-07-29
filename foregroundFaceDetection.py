import cv2
import numpy as np
import depthEstimation
from retinaface import RetinaFace

model = depthEstimation.setupModels()
image_path = 'FOTOS-Sample/179158308_283268670140275_6809950219086834281_n.jpg'
output_path = depthEstimation.generateDepthMap(model=model, image_path=image_path)
image = cv2.imread(output_path)

faces = RetinaFace.detect_faces(image_path)

facial_depth = []
for key in faces:
    facial_area = faces[key]['facial_area']

    # create mask with zeros
    mask = np.zeros((image.shape), dtype=np.uint8)
    pts = np.array([[[facial_area[0], facial_area[1]], [facial_area[0], facial_area[3]], [facial_area[2], facial_area[3]], [facial_area[2], facial_area[1]]]], dtype=np.int32)
    cv2.fillPoly(mask, pts, (255,255,255))

    # get color values
    values = image[np.where((mask == (255,255,255)).all(axis=2))]
    facial_depth.append(values.mean())
    print(values.mean())