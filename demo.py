import h5pyd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.spatial import cKDTree


# Open the desired year of nsrdb data
# server endpoint, username, password is found via a config file
f = h5pyd.File("/nrel/nsrdb/nsrdb_2018.h5", 'r')
print(list(f.attrs))  # list attributes belonging to the root group
dset = f['ghi']
time_index = pd.to_datetime(f['time_index'][...].astype(str))