import os
import numpy as np
import requests
import pandas as pd
import time
import zipfile
from pandas import DataFrame, Series


SOURCE_URL = 'https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r00/access/shapefile/'
wp_wind = 'IBTrACS.since1980.list.v04r00.lines.zip'

if os.path.exists(r'./data'):
    print("File is already exists")
else:
    os.mkdir(r'./data')

print("Starting query for download...")
response = requests.get(SOURCE_URL+wp_wind)
print("Over query!")

filename = wp_wind
chartname = 'IBTrACS.since1980.list.v04r00.lines.dbf'

filepath = os.path.join("./data/", filename)
chartpath = os.path.join("./data/", chartname)

print("Download is beginning!")
start_time = time.time()

if(os.path.exists(filename)):
    print("File is exist, filepath is: %s" %filepath)
else:
    with open(filename, 'wb') as output_file:
        output_file.write(response.content)
    print("File download")

os.chmod("./data/"+wp_wind, 0o777)

if(os.path.exists(chartname)):
    print("Chart is exist, path is %s" %chartpath)
else:
    with zipfile.ZipFile(filename, 'r') as zipObject:
        zipObject.extractall()
    print("Chart is prepared")

end_time = time.time()
print("Download is over, spent time is %.2fs"%(end_time - start_time))
