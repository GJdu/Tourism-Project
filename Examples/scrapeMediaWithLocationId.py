import instaCrawler
import TourismProject
from igramscraper.instagram import Instagram

instagram = Instagram(sleep_between_requests=3)

location_id='757841'
location_name = "plaza-mayor-leon"

medias = instaCrawler.getMediaFromLocationID(instagram=instagram, location_id=location_id, location_name=location_name,count=10)

output_folder_path = 'instaDataSample/'
data = []
columns = TourismProject.getColumns()

for media in medias:
    info = TourismProject.processData(media=media, output_folder_path=output_folder_path)
    data.append(info)

TourismProject.dataFrameToCSV(data=data, columns=columns, output_folder_path=output_folder_path)