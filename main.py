import instaCrawler
from igramscraper.instagram import Instagram
from TourismProject import processData

instagram = Instagram()
instagram = instaCrawler.igramscraperAuthentication(instagram, b_two_step_verificator=True)

location_id='757841'
location_name = "plaza-mayor-leon"
media = instaCrawler.getMediaFromLocationID(instagram=instagram, location_id=location_id, location_name=location_name,count=10)
processData(media=media, output_folder_path='insta/')