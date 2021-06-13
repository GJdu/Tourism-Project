import pandas as pd

meta_data = pd.read_excel("FOTOS/EXCEL FOTOS.xlsx")

def getRow(image_id):
    return meta_data.loc[meta_data["ID FOTO EXTRAÍDO URL FOTO"] == image_id]

def getLocation(image_id):
    data = getRow(image_id)
    location = data.iloc[0]['query'].split('/')[6]
    return location

def getTouristStatus(image_id):
    data = getRow(image_id)
    if data.iloc[0]['¿ES TURISTA?'] == 'TURISTA':
        b_tourist = 1
    else:
        b_tourist = 0

    return b_tourist