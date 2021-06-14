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
import urllib.request
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

    location = getLocationByID(instagram, location_id)
    media = instagram.get_medias_by_location_id(location_id, count)

    for i in range(0, len(media)):
        print(media[i])
        image_path =  'temp/' + str(media[i].identifier) + '.png'
        urllib.request.urlretrieve(str(media[i].image_high_resolution_url), image_path)
        img = Image.open(image_path)
        img.show()
        # os.remove('temp.png')

instagram = Instagram()
getImageFromLocation(instagram, '219558731', 1)
# print(getLocationByID(instagram, '219558731'))