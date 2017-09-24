import numpy as np
from shapely.geometry import Point
import geopandas

# We're going to cheat a bit...
did_not_flood = np.loadtxt('data/did_not_flood.txt')
all_flooded = np.load('data/raw_verts.npy')

# This is the cheating part. Get a random subset of the flooded vertices the
# same size as our manually picked did_no_flood points. We won't really have a
# true "test" dataset at all, but that's okay-ish in this case...
n = len(did_not_flood)
idx = np.random.randint(0, len(all_flooded), n)
train_flooded = all_flooded[idx, :]

flooded = np.hstack([np.zeros(n), np.ones(n)])
xy = np.vstack([did_not_flood, train_flooded])

points = [Point(x, y) for y, x in xy]
df = geopandas.GeoDataFrame(dict(flooded=flooded), geometry=points)
df.to_file('data/training_data.geojson', driver='GeoJSON')
np.savetxt('data/train_xy.txt', xy)
np.savetxt('data/train_class.txt', flooded)
