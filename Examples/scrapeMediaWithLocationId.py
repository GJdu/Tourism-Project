import sys
sys.path.append("..")

import instaCrawler
import TourismProject
from paths import ROOT_DIR
from igramscraper.instagram import Instagram

instagram = Instagram(sleep_between_requests=3)

location_id='757841'
location_name = "plaza-mayor-leon"

medias = instaCrawler.getMediaFromLocationID(instagram=instagram, location_ids=location_id, location_names=location_name,count=10)

output_folder_path = ROOT_DIR + '/instaDataSample/'
data = []
columns = TourismProject.getColumns()

for media in medias:
    info = TourismProject.processData(media=media, output_folder_path=output_folder_path)
    data.append(info)

TourismProject.dataFrameToCSV(data=data, columns=columns, output_folder_path=output_folder_path)