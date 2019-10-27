import h5pyd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pyproj import Proj
import dateutil

# Open the desired year of nsrdb data
# server endpoint, username, password is found via a config file
f = h5pyd.File("/nrel/wtk-us.h5", 'r')  
print(list(f.attrs))  # list attributes belonging to the root group
dset = f['GHI']

# Extract datetime index for datasets
dt = f["datetime"]
dt = pd.DataFrame({"datetime": dt[:]},index=range(0,dt.shape[0]))
dt['datetime'] = dt['datetime'].apply(dateutil.parser.parse)
alldata = dt.loc[(dt.datetime >= '2007-01-01') & (dt.datetime < '2014-01-01')].index

timestep = dt.loc[dt.datetime == '2012-04-01 12:00:00'].index[0]



