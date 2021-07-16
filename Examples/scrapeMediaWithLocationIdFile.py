import instaCrawler
import TourismProject
from igramscraper.instagram import Instagram

instagram = Instagram(sleep_between_requests=3)

medias = instaCrawler.getMediaFromLocationID(instagram=Instagram, location_id_file="León_location_ids.csv", count=10)

output_folder_path = 'instaDataSample/'
data = []
columns = TourismProject.getColumns()

for media in medias:
    info = TourismProject.processData(media=media, output_folder_path=output_folder_path)
    data.append(info)

TourismProject.dataFrameToCSV(data=data, columns=columns, output_folder_path=output_folder_path)