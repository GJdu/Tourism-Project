# https://github.com/realsirjoe/instagram-scraper

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

def getMediaFromLocationID(instagram, location_id, count, b_top_media):
    if b_top_media:
        media = instagram.get_current_top_medias_by_location_id(location_id)
    else:
        media = instagram.get_medias_by_location_id(location_id, count)
    return media