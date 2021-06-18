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

#
def instaloader():
    import instaloader

    L = instaloader.Instaloader()