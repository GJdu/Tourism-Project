import sys
sys.path.append("..")

import instaCrawler
import TourismProject
from paths import ROOT_DIR
from igramscraper.instagram import Instagram

instagram = Instagram(sleep_between_requests=3)
instaCrawler.igramscraperAuthentication(instagram, b_two_step_verificator=True)

data = []
columns = TourismProject.getColumns()
output_folder_path = ROOT_DIR + '/instaDataSample/'

media = TourismProject.getMediaFromUrl(instagram=instagram, url='https://www.instagram.com/p/CRbOnd0hZHg/')
data.append(TourismProject.processData(media=media, output_folder_path=output_folder_path))
TourismProject.dataFrameToCSV(data=data, columns=columns, output_folder_path=output_folder_path)