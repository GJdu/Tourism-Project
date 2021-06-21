import instaCrawler
import os
import urllib.request
import pandas as pd
import detectText
from PIL import Image
from igramscraper.instagram import Instagram
from deepFaceAnalysis import deepFaceAnalysis
from locationDetect import locationDetect
from imageAIDetect import personDetect
from detectSelfie import detectSelfie

def processData(media, location_id):
    data = []
    columns = [
        "identifier",
        "short_code",
        "created_time",
        "type",
        # image url
        "link",
        "image_low_resolution_url",
        "image_thumbnail_url",
        "image_standard_resolution_url",
        "image_high_resolution_url",
        "square_images",
        "carousel_media",
        # content
        "caption",
        "caption_language",
        "caption_mentions",
        "cpation_mentions_count",
        "caption_hashtags",
        "caption_hashtags_count",
        "is_ad",
        # video info
        "video_low_resolution_url",
        "video_standard_resolution_url",
        "video_low_bandwidth_url",
        "video_views",
        "video_url",
        # account object
        "owner",
        "likes_count",
        "location_id",
        "location_name",
        "comments_count",
        "comments",
        "has_more_comments",
        "comments_next_page",
        "location_slug",
        "number_persons",
        "number_faces",
        "age",
        "gender",
        "race",
        "emotion",
        "scene_type",
        "b_selfie",
        "image_text",
    ]

    base_path = 'insta/' + location_id + '/'
    os.makedirs(base_path, exist_ok=True)

    for i in range(0, len(media)):
        print(media[i])
        local_image_path = base_path + media[i].identifier + '.png'
        urllib.request.urlretrieve(str(media[i].image_high_resolution_url), local_image_path)

        img = Image.open(local_image_path)

        # ImageAI detect number of human within the image
        numberPersons = personDetect(local_image_path)

        # Perform deepface analysis
        numberFaces, age, gender, race, emotion = deepFaceAnalysis(local_image_path)

        # Analysis location type
        scene_type = locationDetect(img)

        # Determine wether the image is a selfie
        if numberFaces > 0:
            b_selfie = detectSelfie(image_path=local_image_path)
        else:
            b_selfie = "False"

        # Detect text within the image
        image_text = detectText.detectText(image_path=local_image_path)

        # Extract information from post caption
        mentions = detectText.extractMentions(string=media[i].caption)
        mentions_count = len(mentions)

        hashtags = detectText.extractHashtags(string=media[i].caption)
        hashtags_count = len(hashtags)

        if media[i].caption:
            language = detectText.detectLanguage(string=media[i].caption)
        else:
            language = "None"

        info = [
            media[i].identifier,
            media[i].short_code,
            media[i].created_time,
            media[i].type,
            media[i].link,
            # Image info
            media[i].image_low_resolution_url,
            media[i].image_thumbnail_url,
            media[i].image_standard_resolution_url,
            media[i].image_high_resolution_url,
            media[i].square_images,
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
            # Videos info
            media[i].video_low_resolution_url,
            media[i].video_standard_resolution_url,
            media[i].video_low_bandwidth_url,
            media[i].video_views,
            media[i].video_url,
            # Account object
            media[i].owner,
            media[i].likes_count,
            media[i].location_id,
            media[i].location_name,
            media[i].comments_count,
            media[i].comments,
            media[i].has_more_comments,
            media[i].comments_next_page,
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
            # Tessoract
            image_text,
        ]

        data.append(info)

    df = pd.DataFrame(data=data, columns=columns)

    output_path = 'insta/' + location_id + '/igramscraperOutput.csv'
    if os.path.isfile(output_path):
        media_df = pd.read_csv(output_path, index_col=False)
        media_df = media_df.append(df)
        media_df = media_df.drop_duplicates(subset=['Image Id'])
        media_df.to_csv(output_path, index=False)
    else:
        df.to_csv(output_path, index=False)

location_id='212913483'

instagram = Instagram()
instagram = instaCrawler.igramscraperAuthentication(instagram)
media = instaCrawler.getMediaFromLocationID(instagram=instagram, location_id=location_id, count=10, b_top_media=False)
processData(media=media, location_id=location_id)