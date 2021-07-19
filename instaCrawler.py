# https://github.com/realsirjoe/instagram-scraper

import pandas as pd
import instaAuthentication
from paths import ROOT_DIR

def igramscraperAuthentication(instagram, username='', password='', b_two_step_verificator = False):
    if not username or password:
        username, password = instaAuthentication.getLogin()
    instagram.with_credentials(username, password, ROOT_DIR + '/cache/')
    instagram.login(two_step_verificator=b_two_step_verificator)

    return instagram

def getLocationByID(instagram, location_id):
    location = instagram.get_location_by_id(location_id).slug
    return location


def getLocationIdFromCSV(file):
    location_df = pd.read_csv(file)
    location_df.columns = ["location_id", "location_name"]

    location_id = location_df["location_id"].tolist()
    location_name = location_df["location_name"].tolist()

    return location_id, location_name

def getMediaFromLocationID(instagram, location_id_file = '', location_ids = None, location_names = None, count=10, b_top_media=False):
    if location_id_file:
        media = []
        location_ids, location_names = getLocationIdFromCSV(location_id_file)
        for id in location_ids:
            if b_top_media:
                try:
                    media_obj = instagram.get_current_top_medias_by_location_id(id)
                    for i in range(0, len(media_obj)):
                        media_obj[i].location_id = location_ids
                        media_obj[i].location_name = location_names
                    media = media + media_obj
                except:
                    print("Can't not find location id: " + str(id))
            else:
                try:
                    media_obj = instagram.get_medias_by_location_id(id, count)
                    for i in range(0, len(media_obj)):
                        media_obj[i].location_id = location_ids
                        media_obj[i].location_name = location_names
                    media = media + media_obj
                except:
                    print("Can't not find location id: " + str(id))
    elif location_ids:
        if b_top_media:
            media = instagram.get_current_top_medias_by_location_id(location_ids)
            for i in range(0, len(media)):
                media[i].location_id = location_ids
                media[i].location_name = location_names
        else:
            media = instagram.get_medias_by_location_id(location_ids, count)
            for i in range(0, len(media)):
                media[i].location_id = location_ids
                media[i].location_name = location_names
    else:
        media = None
    return media
