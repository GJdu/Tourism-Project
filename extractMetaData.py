import pandas as pd

def loadMetaData(file_path = "FOTOS/EXCEL FOTOS.xlsx"):
    return pd.read_excel(file_path)

def getRowFromImageId(data, image_id):
    return data.loc[data["ID FOTO EXTRAÍDO URL FOTO"] == image_id]

def getLocationFromImageId(data, image_id):
    data = getRowFromImageId(data, image_id)
    location = data.iloc[0]['query'].split('/')[6]
    return location

def getTouristStatusFromImageId(data, image_id):
    data = getRowFromImageId(data, image_id)
    if data.iloc[0]['¿ES TURISTA?'] == 'TURISTA':
        b_tourist = 1
    else:
        b_tourist = 0

    return b_tourist

def getPostIdCodeList(file_path = "FOTOS/EXCEL FOTOS.xlsx"):
    df_url_list = pd.read_excel(file_path, usecols=['postUrl'])
    return df_url_list['postUrl'].to_list()

def instaUrlToPostIdCode(url):
    # https://www.instagram.com/p/CNsLBYLFZi1/ to CNsLBYLFZi1
    return url.rsplit('/', 2)[-2]