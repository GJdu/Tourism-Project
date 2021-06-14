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
def igramscraperSetup(instagram):

    import instaAuthentication
    username, passward = instaAuthentication.getLogin()
    instagram.with_credentials(username, passward, 'cache/')
    instagram.login()

    return instagram

def igramscraperProxy(instagram):
    proxies = {
        'http': 'http://123.45.67.8:1087',
        'https': 'http://123.45.67.8:1087',
    }
    instagram.set_proxies(proxies)
    return instagram

def getLocationByID(instagram, location_id):
    instagram = igramscraperSetup(instagram)

    location = instagram.get_location_by_id(location_id).slug
    return location

def getImageFromLocation(instagram, location_id, count):

    media = instagram.get_medias_by_location_id(location_id, count)

    data = []

    columns = [
        "Image Id",
        "Likes Count",
        "Image High Resolution Url",
        "Instagram Link",
        "Location Id",
        "Location Name"
    ]

    base_path = 'insta/' + location_id + '/'
    os.makedirs(base_path, exist_ok=True)

    for i in range(0, len(media)):
        print(media[i])
        local_image_path = base_path + media[i].identifier + '.png'
        urllib.request.urlretrieve(str(media[i].image_high_resolution_url), local_image_path)
        img = Image.open(local_image_path)
        img.show()

        info = [
            media[i].identifier,
            media[i].likes_count,
            media[i].image_high_resolution_url,
            media[i].link,
            media[i].location_id,
            media[i].location_name
        ]

        data.append(info)

    df = pd.DataFrame(data=data, columns=columns)

    output_path = 'insta/' + location_id + '/igramscraperOutput.csv'
    if os.path.isfile(output_path):
        media_df = pd.read_csv(output_path)
        media_df = media_df.append(df, ignore_index=True)
        media_df.to_csv(output_path, index_label=False)
    else:
        df.to_csv(output_path, index_label=False)

instagram = Instagram()
getImageFromLocation(instagram, '219558731', 2)
# print(getLocationByID(instagram, '219558731'))