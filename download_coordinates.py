import json
import h5pyd
import numpy as np

f = h5pyd.File("/nrel/wtk-us.h5", 'r')

output = {}
for  idx in np.ndindex(f['coordinates'].shape):
    key = str(idx[0]) + "," + str(idx[1])
    value = str(f['coordinates'][idx][0]) + "," + str(f['coordinates'][idx][0])
    
    print(key, value)
    output[key] = value

with open('coordinates.json', 'w') as fp:
    json.dump(output, fp)

