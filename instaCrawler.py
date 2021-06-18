# instaLooter
# https://github.com/althonos/InstaLooter
def instaLooter (hashtag, count):
    from instalooter.looters import HashtagLooter
    looter = HashtagLooter(hashtag)
    looter.download(hashtag, media_count = count)

# instagram-scraper
# https: // github.com / arc298 / instagram - scraper
def instaScapper(hashtag, count, location_file):
    import subprocess
    # Call instagram-scrapper command line application
    subprocess.run(["instagram-scraper",
                    "--tag", hashtag,
                    "--include-location",
                    "--filter-location-file", location_file,
                    "--media-types", "image",
                    "--maximum", count],
                   check=True,
                   universal_newlines=True,
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE
                   )

# https://github.com/realsirjoe/instagram-scraper
import os
import json
import urllib.request
import pandas as pd
from PIL import Image
from igramscraper.instagram import Instagram

def igramscraperAuthentication(instagram):

    import instaAuthentication
    username, passward = instaAuthentication.getLogin()
    instagram.with_credentials(username, passward, 'cache/')
    instagram.login()

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

def getImageFromLocation(instagram, location_id, count, b_top_media):
    if b_top_media:
        media = instagram.get_current_top_medias_by_location_id(location_id)
    else:
        media = instagram.get_medias_by_location_id(location_id, count)

    data = []
    columns = [
        "identifier",
        "short_code",
        "created_time",
        "type",
        "link",
        "image_low_resolution_url",
        "image_thumbnail_url",
        "image_standard_resolution_url",
        "image_high_resolution_url",
        "square_images",
        "carousel_media",
        "caption",
        "is_ad",
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
    ]

    base_path = 'insta/' + location_id + '/'
    os.makedirs(base_path, exist_ok=True)

    for i in range(0, len(media)):
        print(media[i])
        local_image_path = base_path + media[i].identifier + '.png'
        urllib.request.urlretrieve(str(media[i].image_high_resolution_url), local_image_path)
        img = Image.open(local_image_path)

        info = [
            media[i].identifier,
            media[i].short_code,
            media[i].created_time,
            media[i].type,
            media[i].link,
            media[i].image_low_resolution_url,
            media[i].image_thumbnail_url,
            media[i].image_standard_resolution_url,
            media[i].image_high_resolution_url,
            media[i].square_images,
            media[i].carousel_media,
            media[i].caption,
            media[i].is_ad,
            media[i].video_low_resolution_url,
            media[i].video_standard_resolution_url,
            media[i].video_low_bandwidth_url,
            media[i].video_views,
            media[i].video_url,
            # account object
            media[i].owner,
            media[i].likes_count,
            media[i].location_id,
            media[i].location_name,
            media[i].comments_count,
            media[i].comments,
            media[i].has_more_comments,
            media[i].comments_next_page,
            media[i].location_slug,
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

instagram = Instagram()
instagram = igramscraperAuthentication(instagram)
# instagram = igramscraperProxy(instagram)
getImageFromLocation(instagram=instagram, location_id='212913483', count=10, b_top_media=False)
# print(getLocationByID(instagram, '219558731'))

def instaloader():
    from datetime import datetime
    import instaloader

    L = instaloader.Instaloader()

