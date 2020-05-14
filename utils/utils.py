import numpy as np
import pandas as pd
import geopandas as gpd
import folium
from PIL import Image, ExifTags
from os import walk
import matplotlib.pyplot as plt

colors = [
    'red',
    'blue',
    'gray',
    'darkred',
    'orange',
    'beige',
    'green',
    'darkgreen',
    'lightgreen',
    'darkblue',
    'lightblue',
    'purple',
    'darkpurple',
    'pink',
    'cadetblue',
    'lightgray',
    'black'
]

def get_folders(path):
    for path,folders,files in walk(path):
        paths = [path+'/'+i+'/' for i in folders if i != 'Segmented']
        break
    try:
    	paths.sort()
    except:
    	print('Invalid or empty database path:')
    	print('\t'+path+'/')
    	exit()
    return paths

def get_files_in_path(path):
    files = []
    for _,_,file in walk(path):
        files.extend(file)
        break
    files = [f for f in files if '.JPG' in f]
    files.sort()
    return files

def get_files_in_paths(paths):
    files = {}
    for path in paths:
        files[path] = get_files_in_path(path)
    return files

def get_exif_full(path,file):
    img = Image.open(path+file)
    exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }
    return exif

def get_exif(path,file):
    exif = get_exif_full(path,file)
    Lat =(exif['GPSInfo'][2][0][0]/exif['GPSInfo'][2][0][1]+
          exif['GPSInfo'][2][1][0]/(exif['GPSInfo'][2][1][1]*60)+
          exif['GPSInfo'][2][2][0]/(exif['GPSInfo'][2][2][1]*3600))
    if exif['GPSInfo'][1][0][0] == 'S':
        Lat = -Lat
    Lon =(exif['GPSInfo'][4][0][0]/exif['GPSInfo'][4][0][1]+
          exif['GPSInfo'][4][1][0]/(exif['GPSInfo'][4][1][1]*60)+
          exif['GPSInfo'][4][2][0]/(exif['GPSInfo'][4][2][1]*3600))
    if exif['GPSInfo'][3][0][0] == 'W':
        Lon = -Lon
    LatT =(exif['GPSInfo'][1][0][0],
          exif['GPSInfo'][2][0][0]/exif['GPSInfo'][2][0][1],
          exif['GPSInfo'][2][1][0]/exif['GPSInfo'][2][1][1],
          exif['GPSInfo'][2][2][0]/exif['GPSInfo'][2][2][1])
    LonT =(exif['GPSInfo'][3][0][0],
          exif['GPSInfo'][4][0][0]/exif['GPSInfo'][4][0][1],
          exif['GPSInfo'][4][1][0]/exif['GPSInfo'][4][1][1],
          exif['GPSInfo'][4][2][0]/exif['GPSInfo'][4][2][1])
    H = exif['GPSInfo'][6][0]/exif['GPSInfo'][6][1]
    DateTime = exif['DateTimeOriginal']
    data = [path,file,DateTime,H,Lat,Lon,LatT,LonT]
    return data

def get_df(path,files):
    datas = [get_exif(path,f) for f in files]
    col_names = ['Folder','File','TimeStamp','Height','Latitude','Longitude','LatitudeDMS','LongitudeDMS']
    datas = pd.DataFrame(datas,columns=col_names)
    return datas

def add_rows_direction(datas):

    row_i=1
    rows = []
    di = []
    rows_i = 1
    d = 'N'
    if datas.iloc[2]['Longitude'] > datas.iloc[0]['Longitude']:
        d = 'E'
    else:
        d = 'W'
    vr = [(datas.iloc[0]['LatitudeDMS'][3],d,1)]
    for i in range(len(datas.index)):
        f = False
        for value,d2,row in vr:
            if abs(datas.iloc[i]['LatitudeDMS'][3]-value)<0.2:
                f = True
                rows.append(row)
                di.append(d2)
                break
        if not f:
            row_i += 1
            rows.append(row_i)
            if datas.iloc[i+2]['Longitude'] > datas.iloc[i]['Longitude']:
                d = 'E'
            else:
                d = 'W'
            vr.append((datas.iloc[i]['LatitudeDMS'][3],d,row_i))
            di.append(d)
    datas['Row']=rows
    datas['Dir']=di
    
    return datas