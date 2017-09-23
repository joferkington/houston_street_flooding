import os

import pandas as pd
import numpy as np
import geopandas

data = []
for dirpath, dirnames, filenames in os.walk('../uflood/'):
    if 'houston.geojson' in filenames:
        fname = os.path.join(dirpath, 'houston.geojson')
        data.append(geopandas.read_file(fname))

flattened = pd.concat(data).groupby('id')['geometry'].agg('min')
geopandas.GeoSeries(flattened).to_file('flooded_streets.geojson',
                                       driver='GeoJSON')



