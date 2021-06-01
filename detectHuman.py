import cv2
import imutils

HOGCV = cv2.HOGDescriptor()
HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

def detect(image):
    bounding_box_cordinates, weights = HOGCV.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.03)

    person = 1
    for x, y, w, h in bounding_box_cordinates:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, f'person {person}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        person += 1

    cv2.putText(image, 'Status : Detecting ', (40, 40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)
    cv2.putText(image, f'Total Persons : {person - 1}', (40, 70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)
    cv2.imshow('output', image)

    return image

def detectByPathImage(path, output_path):
    image = cv2.imread(path)

    image = imutils.resize(image, width = min(800, image.shape[1]))

    result_image = detect(image)

    if output_path is not None:
        cv2.imwrite(output_path, result_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

# detectByPathImage("FOTOS-Sample/179945954_298786348383573_8009489283757952249_n.jpg", "Test/test.jpg")
detectByPathImage("FOTOS-Sample/180166436_1345601032491136_7463974967916427671_n.jpg", "Test/test.jpg")