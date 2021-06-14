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
from igramscraper.instagram import Instagram
def igramscraperAuthentication():
    instagram = Instagram()
    instagram.with_credentials('username', 'password', 'path/to/cache/folder')
    instagram.login()
    return instagram

def getLocationID(location):
    instagram = igramscraperAuthentication()

    # Location id from facebook
    location_id = instagram.get_location_by_id(location)
    return location_id

def getImageFromLocation(location, count):
    instagram = Instagram()
    location_id = getLocationID(location)
    media = instagram.get_medias_by_location_id(location_id, count)