# https://github.com/realsirjoe/instagram-scraper

import pandas as pd
import instaAuthentication

def igramscraperAuthentication(instagram):
    username, passward = instaAuthentication.getLogin()
    instagram.with_credentials(username, passward, 'cache/')
    instagram.login(two_step_verificator=True)

    return instagram

def igramscraperProxy(instagram):
    # Get free proxies here: https://free-proxy-list.net/
    proxies = {
        'http': 'http://193.149.225.160:80',
        'https': 'https://193.149.225.160:80',
    }
    instagram.set_proxies(proxies)
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

def getMediaFromLocationID(instagram, location_id_file = '',location_id = None, location_name = None,count=10, b_top_media=False):
    if location_id_file:
        media = []
        location_id, location_name = getLocationIdFromCSV(location_id_file)
        for ids in location_id:
            if b_top_media:
                media_obj = instagram.get_current_top_medias_by_location_id(ids)
                for i in range(0, len(media_obj)):
                    media_obj[i].location_id = location_id
                    media_obj[i].location_name = location_name
            else:
                media_obj = instagram.get_medias_by_location_id(ids, count)
                for i in range(0, len(media_obj)):
                    media_obj[i].location_id = location_id
                    media_obj[i].location_name = location_name
            media.append(media_obj)
    elif location_id:
        if b_top_media:
            media = instagram.get_current_top_medias_by_location_id(location_id)
            for i in range(0, len(media)):
                media[i].location_id = location_id
                media[i].location_name = location_name
        else:
            media = instagram.get_medias_by_location_id(location_id, count)
            for i in range(0, len(media)):
                media[i].location_id = location_id
                media[i].location_name = location_name
    else:
        media = None
    return media
