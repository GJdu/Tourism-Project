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

## Usage
Scrape Instagram with a given facebook location id
```python
import instaCrawler
from igramscraper.instagram import Instagram
from TourismProject import processData

instagram = Instagram(sleep_between_requests=3)

location_id='757841'
location_name = "plaza-mayor-leon"
media = instaCrawler.getMediaFromLocationID(instagram=instagram, location_id=location_id, location_name=location_name,count=10)
processData(media=media, output_folder_path='insta/')
```

Scrape Instagram with a given list of facebook location id in CSV
```python
import instaCrawler
from igramscraper.instagram import Instagram
from TourismProject import processData

instagram = Instagram(sleep_between_requests=3)

media = instaCrawler.getMediaFromLocationID(instagram=Instagram, location_id_file="León_location_ids.csv", count=10)
processData(media=media, output_folder_path='insta/')
```

Scrape a single Instagram post with a given url
```python
import instaCrawler
from igramscraper.instagram import Instagram
from TourismProject import processData

instagram = Instagram(sleep_between_requests=3)
instaCrawler.igramscraperAuthentication(instagram, username='your_username', password='your_password', b_two_step_verificator=True)

media = getMediaFromUrl(instagram=instagram, url='https://www.instagram.com/p/SomeCode/')
processData(media=media, output_folder_path='insta/')
