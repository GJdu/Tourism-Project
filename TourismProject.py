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
import extractMetaData

# Build detection models
detectSelfie_model = detectSelfie.getModel(MODEL="Models/final_detectSelfie_model")
retina_model, deepface_models = deepFaceAnalysis.buildDeepFaceModels()

def getColumns():
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
        "translated_caption",
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
        "has_more_comments",
        "location_slug",
        # ImageAI
        "number_persons",
        # DeepFace
        "number_faces",
        "age",
        "gender",
        "race",
        "emotion",
        # Place365
        "scene_type",
        # Selfie detect
        "selfie?",
    ]
    return columns

def setupInstagramScrapper(sleep_between_requests=3, b_login=True):
    instagram = Instagram(sleep_between_requests=sleep_between_requests)
    if b_login:
        return instaCrawler.igramscraperAuthentication(instagram, b_two_step_verificator=True)
    return instagram

def processData(media, output_folder_path):

    base_path = output_folder_path
    os.makedirs(base_path, exist_ok=True)

    print(media)
    local_image_path = base_path + media.identifier + '.png'
    urllib.request.urlretrieve(str(media.image_high_resolution_url), local_image_path)

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

    if media.caption:
        # Extract information from post caption
        translated_caption = detectText.googleTranslate(media.caption),
        mentions = detectText.extractMentions(string=media.caption)
        mentions_count = len(mentions)
        hashtags = detectText.extractHashtags(string=media.caption)
        hashtags_count = len(hashtags)
        language = detectText.detectLanguage(string=media.caption)
        if language == 'en':
            polarity = detectText.analysisSentimentTextBlob(string=media.caption)
        else:
            try:
                polarity = detectText.analysisSentimentTextBlob(detectText.googleTranslate(string=media.caption))
            except:
                polarity = "None"
    else:
        translated_caption = "None"
        mentions = "None"
        mentions_count = "None"
        hashtags = "None"
        hashtags_count = "None"
        language = "None"
        polarity = "None"

    info = [
        media.identifier,
        media.short_code,
        datetime.utcfromtimestamp(media.created_time).strftime('%Y-%m-%d %H:%M:%S'),
        media.type,
        media.link,
        # Image info
        media.image_high_resolution_url,
        media.carousel_media,
        # Caption NLP
        media.caption,
        language,
        translated_caption,
        mentions,
        mentions_count,
        hashtags,
        hashtags_count,
        polarity,
        # Insta Ads
        media.is_ad,
        # Account object
        media.owner,
        media.likes_count,
        media.location_id,
        media.location_name,
        media.comments_count,
        media.comments,
        media.has_more_comments,
        media.location_slug,
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

    return info

def dataFrameToCSV(data, columns, output_folder_path):

    base_path = output_folder_path
    os.makedirs(base_path, exist_ok=True)
    df = pd.DataFrame(data=data, columns=columns)

    output_csv_path = output_folder_path + 'igramscraperOutput.csv'
    if os.path.isfile(output_csv_path):
        media_df = pd.read_csv(output_csv_path, index_col=False)
        media_df = media_df.append(df)
        media_df = media_df.drop_duplicates(subset=['identifier'])
        media_df.to_csv(output_csv_path, index=False)
    else:
        df.to_csv(output_csv_path, index=False)

def getMediaFromUrl(instagram, url):
    return instagram.get_media_by_url(url)

def getMediasFromUrls(instagram, output_path, b_login_in = True, count=1):
    index = 0
    base_path = output_path

    data = []
    columns = getColumns()

    url_list = extractMetaData.getPostIdCodeList()

    for url in url_list:
        if index == count:
            dataFrameToCSV(data=data, columns=columns, output_folder_path=base_path)
            return

        index += 1

        try:
            media = getMediaFromUrl(instagram, url)
            info = processData(media, base_path)
            data.append(info)
        except:
            print("Media with given code does not exist or account is private: " + url)

instagram = Instagram(sleep_between_requests=3)
# instagram = instaCrawler.igramscraperAuthentication(instagram, b_two_step_verificator=True)

location_id='627142930969029'
location_name = "catedral-de-leon-espana-leon-cathedral-spain"
medias = instaCrawler.getMediaFromLocationID(instagram=instagram, location_id=location_id, location_name=location_name,count=10)

output_folder_path = 'instaDataSample10/'
data = []
columns = getColumns()

for media in medias:
    info = processData(media=media, output_folder_path=output_folder_path)
    data.append(info)

dataFrameToCSV(data=data, columns=columns, output_folder_path=output_folder_path)
#
# # # media = instaCrawler.getMediaFromLocationID(instagram=Instagram, location_id_file="León_location_ids.csv", count=10)