import subprocess

# Call instagram-scrapper command line application
subprocess.run(["instagram-scraper",
                "--tag", "salamanca",
                "--include-location",
                "--filter-location-file", "salamanca_locations.txt",
                "--media-types", "image",
                "--maximum", "50"],
               check=True,
               universal_newlines=True,
               stdout=subprocess.PIPE,
               stderr=subprocess.PIPE
               )