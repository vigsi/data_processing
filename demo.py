import h5py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pyproj import Proj
import dateutil
import geojson
from datetime import datetime
import json
import boto3
import time
from multiprocessing import Pool

s3 = boto3.client('s3')

def generate_polygon(pair):
    lon = pair[0]
    lat = pair[1]

    #1 degree latitude = 111,111 meters, 2,000 meters is 1.8% of 111,111, 1.8% of 1 = .018000018

    return [[lon - 2000/(np.cos(np.deg2rad(lat))), lat - .018000018], [lon + 2000/(np.cos(np.deg2rad(lat))), lat + .018000018], [lon - 2000/(np.cos(np.deg2rad(lat))), lat + .018000018], [lon + 2000/(np.cos(np.deg2rad(lat))), lat - .018000018]]

def upload_measured(dset):
    fileset = set()
    GeoJson = {}
    for idx in np.ndindex(dset.shape):
        timestamp = f["datetime"][idx[0]].decode('UTF-8')
        fileobj = datetime.strptime(timestamp, "%Y%m%d%H%M%S")
        filekey = fileobj.strftime("%Y%m%d%H")


        if filekey not in fileset:
            #Initialize GeoJson object
            #if len(fileset) > 0: 
                #s3.put_object(
                #        Bucket='vigsi-data-processed',
                #        Body=json.dumps(GeoJson),
                #        Key="{}-{}-{}/measured/{}-{}-{}T{}0000.000Z.json".format(GeoJson["year"], GeoJson["month"], GeoJson["day"], GeoJson["year"], GeoJson["month"], GeoJson["day"], GeoJson["hour"])
                #)
            print(json.dumps(GeoJson, indent=4))
            GeoJson = {"points": [], "year": fileobj.strftime("%Y"), "month": fileobj.strftime("%m"), "day": fileobj.strftime("%d"), "hour": fileobj.strftime("%H")}
            

            fileset.add(filekey)
        


        coordinates = [idx[1],idx[2]]
        ghi = dset[idx].item()
        
        GeoJson["points"].append({'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [coordinates[0], coordinates[1]]}, 'properties': {'ghi': ghi}})


if __name__ == '__main__':
    # Open the desired year of nsrdb data
    # server endpoint, username, password is found via a config file
    f = h5py.File("/mnt/data/vigsi-data/2013-01.h5", 'r')
    print(list(f.keys()))  # list attributes belonging to the root group
    dset = f['GHI']

    upload_measured(dset)
