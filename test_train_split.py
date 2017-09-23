import numpy as np
import geopandas
import sklearn

data = geopandas.read_file('flooded_streets.geojson')
verts =[]
for item in data['geometry']:
    try:
        verts.append(np.array(item))
    except TypeError:
        verts.extend([np.array(segment) for segment in item])

verts = np.concatenate(verts)
np.save('raw_verts.npy', verts)
