# Tourism-Project

## How to install

Clone the git repository
```
  $ git clone https://github.com/GJdu/Tourism-Project.git
```
Install all dependencies
```
  $ pip install -r requirements.txt
```
Download RetinaNet weights for ImageAI.
```
  $ curl -L "https://github.com/OlafenwaMoses/ImageAI/releases/download/essentials-v5/resnet50_coco_best_v2.1.0.h5/" > ./Models/resnet50_coco_best_v2.1.0.h5
```
To login with instagram scrapper updaete the username and password of ```instaAuthentication.py```
```python
    username = 'your_username'
    password = 'your_password'
```

## Usage
Scrape Instagram with a given facebook location id
```python
import instaCrawler
import TourismProject
from igramscraper.instagram import Instagram

instagram = Instagram(sleep_between_requests=3)

location_id='757841'
location_name = "plaza-mayor-leon"

medias = instaCrawler.getMediaFromLocationID(instagram=instagram, location_id=location_id, location_name=location_name,count=5)

output_folder_path = 'instaDataSample/'
data = []
columns = TourismProject.getColumns()

for media in medias:
    info = TourismProject.processData(media=media, output_folder_path=output_folder_path)
    data.append(info)

TourismProject.dataFrameToCSV(data=data, columns=columns, output_folder_path=output_folder_path)
```

Scrape Instagram with a given list of facebook location ids in a csv file
```python
import instaCrawler
from igramscraper.instagram import Instagram
from TourismProject import processData

instagram = Instagram(sleep_between_requests=3)

medias = instaCrawler.getMediaFromLocationID(instagram=Instagram, location_id_file="León_location_ids.csv", count=10)

output_folder_path = 'instaDataSample/'
data = []
columns = getColumns()

for media in medias:
    info = processData(media=media, output_folder_path=output_folder_path)
    data.append(info)

dataFrameToCSV(data=data, columns=columns, output_folder_path=output_folder_path)
```
The given csv file should be in the following format
```csv
1751188368449980,paseo-de-la-condesa-de-sagasta
1602508106737730,plaza-de-santo-domingo-leon
858403594,prada-a-tope
880961525,plaza-de-toros-de-leon
267661857,plaza-san-marcos
1199149896866900,barrio-romantico
691728620942834,barrio-humedo-leon
```

Scrape a single Instagram post with a given url
```python
import instaCrawler
import TourismProject
from igramscraper.instagram import Instagram

instagram = Instagram(sleep_between_requests=3)
instaCrawler.igramscraperAuthentication(instagram, username='your_username', password='your_password', b_two_step_verificator=True)

media = TourismProject.getMediaFromUrl(instagram=instagram, url='https://www.instagram.com/p/SomeCode/')
TourismProject.processData(media=media, output_folder_path='instaDataSample/')
```

For more example please visit https://github.com/GJdu/Tourism-Project/tree/master/Examples
