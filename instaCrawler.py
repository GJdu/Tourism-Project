from instalooter.looters import HashtagLooter

def instaCrawler (Hashtag, count):

    looter = HashtagLooter(Hashtag)
    looter.download(Hashtag, media_count = count)