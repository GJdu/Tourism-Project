from google.cloud import vision
import io
import os

# https://cloud.google.com/docs/authentication/getting-started#command-line
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="tourism-project-image-268ecc2e54b5.json"

# Detects landmarks in the file.
def detect_landmarks(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations
    print('Landmarks:')

    for landmark in landmarks:
        print(landmark.description)
        for location in landmark.locations:
            lat_lng = location.lat_lng
            print('Latitude {}'.format(lat_lng.latitude))
            print('Longitude {}'.format(lat_lng.longitude))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return landmarks[0].description

detect_landmarks('../FOTOS-Sample/180760937_221298752666578_9215985169661169087_n.jpg')