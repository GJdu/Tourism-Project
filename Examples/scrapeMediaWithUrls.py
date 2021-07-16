import instaCrawler
import TourismProject
from igramscraper.instagram import Instagram

instagram = Instagram(sleep_between_requests=3)
instaCrawler.igramscraperAuthentication(instagram, username='your_username', password='your_password', b_two_step_verificator=True)

media = TourismProject.getMediaFromUrl(instagram=instagram, url='https://www.instagram.com/p/SomeCode/')
TourismProject.processData(media=media, output_folder_path='instaDataSample/')