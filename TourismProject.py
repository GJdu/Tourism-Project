import instaCrawler
import os
import urllib.request
import pandas as pd
import detectText
from PIL import Image
from igramscraper.instagram import Instagram
import deepFaceAnalysis
from locationDetect import locationDetect
from imageAIDetect import personDetect
import detectSelfie
from datetime import datetime

def processData(media, output_folder_path):
    data = []
    columns = [
        "identifier",
        "short_code",
        "created_time",
        "type",
        # image url
        "link",
        "image_high_resolution_url",
        "carousel_media",
        # content
        "caption",
        "caption_language",
        "caption_mentions",
        "cpation_mentions_count",
        "caption_hashtags",
        "caption_hashtags_count",
        "caption_polarity",
        "is_ad",
        # account object
        "owner",
        "likes_count",
        "location_id",
        "location_name",
        "comments_count",
        "comments",
        "location_slug",
        "number_persons",
        "number_faces",
        "age",
        "gender",
        "race",
        "emotion",
        "scene_type",
        "selfie?",
    ]

    base_path = output_folder_path
    os.makedirs(base_path, exist_ok=True)

    # Build detection models
    detectSelfie_model = detectSelfie.getModel(MODEL="Models/final_detectSelfie_model")
    retina_model, deepface_models = deepFaceAnalysis.buildDeepFaceModels()

    for i in range(0, len(media)):
        print(media[i])
        local_image_path = base_path + media[i].identifier + '.png'
        urllib.request.urlretrieve(str(media[i].image_high_resolution_url), local_image_path)

        img = Image.open(local_image_path)

        # ImageAI detect number of human within the image
        numberPersons = personDetect(local_image_path)

        # Perform deepface analysis
        numberFaces, age, gender, race, emotion = deepFaceAnalysis.deepFaceAnalysis(retina_model, deepface_models, local_image_path)

        # Analysis location type
        scene_type = locationDetect(img)

        # Determine wether the image is a selfie
        if numberFaces > 0:
            b_selfie = detectSelfie.detectSelfie(model=detectSelfie_model, image_path=local_image_path)
        else:
            b_selfie = "False"

        # # Detect text within the image
        # image_text = detectText.detectText(image_path=local_image_path)

        if media[i].caption:
            # Extract information from post caption
            mentions = detectText.extractMentions(string=media[i].caption)
            mentions_count = len(mentions)
            hashtags = detectText.extractHashtags(string=media[i].caption)
            hashtags_count = len(hashtags)
            language = detectText.detectLanguage(string=media[i].caption)
        else:
            mentions = "None"
            mentions_count = "None"
            hashtags = "None"
            hashtags_count = "None"
            language = "None"

        info = [
            media[i].identifier,
            media[i].short_code,
            datetime.utcfromtimestamp(media[i].created_time).strftime('%Y-%m-%d %H:%M:%S'),
            media[i].type,
            media[i].link,
            # Image info
            media[i].image_high_resolution_url,
            # media[i].square_images,
            media[i].carousel_media,
            # Caption NLP
            media[i].caption,
            language,
            mentions,
            mentions_count,
            hashtags,
            hashtags_count,
            # Insta Ads
            media[i].is_ad,
            # Account object
            media[i].owner,
            media[i].likes_count,
            media[i].location_id,
            media[i].location_name,
            media[i].comments_count,
            media[i].comments,
            media[i].location_slug,
            # ImageAI
            numberPersons,
            # DeepFace
            numberFaces,
            age,
            gender,
            race,
            emotion,
            # Place365
            scene_type,
            # Selfie detect
            b_selfie,
        ]

        data.append(info)

    df = pd.DataFrame(data=data, columns=columns)

    output_csv_path = output_folder_path + 'igramscraperOutput.csv'
    if os.path.isfile(output_csv_path):
        media_df = pd.read_csv(output_csv_path, index_col=False)
        media_df = media_df.append(df)
        media_df = media_df.drop_duplicates(subset=['Image Id'])
        media_df.to_csv(output_csv_path, index=False)
    else:
        df.to_csv(output_csv_path, index=False)

instagram = Instagram()
# instagram = instaCrawler.igramscraperAuthentication(instagram, b_two_step_verificator=True)

location_id='757841'
location_name = "plaza-mayor-leon"
media = instaCrawler.getMediaFromLocationID(instagram=instagram, location_id=location_id, location_name=location_name,count=10)
#
# # # media = instaCrawler.getMediaFromLocationID(instagram=Instagram, location_id_file="León_location_ids.csv", count=10)
# processData(media=media, output_folder_path='insta/')