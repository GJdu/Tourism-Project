import sys
sys.path.append("..")

import instaCrawler
import TourismProject
from paths import ROOT_DIR
from igramscraper.instagram import Instagram

instagram = Instagram(sleep_between_requests=3)

output_folder_path = ROOT_DIR + '/instaDataSample/'
location_id_file_path = ROOT_DIR + "/León_location_ids.csv"

medias = instaCrawler.getMediaFromLocationID(instagram=instagram, location_id_file=location_id_file_path, count=10)

data = []
columns = TourismProject.getColumns()

for media in medias:
    info = TourismProject.processData(media=media, output_folder_path=output_folder_path)
    data.append(info)

TourismProject.dataFrameToCSV(data=data, columns=columns, output_folder_path=output_folder_path)