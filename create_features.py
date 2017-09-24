import pyproj
import numpy as np
import rasterio as rio
import rasterio.features
import geopandas
import shapely.geometry as geom
import pandas as pd

# For some reason gdal isn't picking up the state plane projection correctly
DEM_PROJECTION = ('+proj=lcc +lat_1=28.38333333333333 +lat_2=30.28333333333334'
                  ' +lat_0=27.83333333333333 +lon_0=-99 +x_0=600000.0000000001'
                  ' +y_0=4000000 +datum=NAD83 +units=us-ft +no_defs')

def main():
    lidar = 'data/merged_dem.vrt'
    df = geopandas.read_file('data/test_reprojection.geojson')
    funcs = dict(relief=relief, avg_slope=avg_slope, planar_slope=planar_slope,
                 local_height=local_height, local_relief=local_relief)

    features = []
    columns = sorted(funcs.keys())
    for _, point in df.iterrows():
        row = [funcs[key](point.geometry, lidar) for key in columns]
        row.append(point['flooded'])
        features.append(row)

    output = pd.DataFrame(features, columns=columns + ['flooded'])
    output.to_csv('features_and_class.csv')

    pred_features = generate_prediction_points(lidar)
    pred_features.to_file('prediction_features.geojson', driver='GeoJSON')

def relief(point, lidar_filename):
    region = geom.mapping(point.buffer(300))
    return read(lidar_filename, region).ptp()

def avg_slope(point, lidar_filename):
    region = geom.mapping(point.buffer(100))
    elev = read(lidar_filename, region)
    dy, dx = np.gradient(elev)
    return np.hypot(dy, dx).mean()

def planar_slope(point, lidar_filename):
    region = geom.mapping(point.buffer(100))
    elev = read(lidar_filename, region)
    dy, dx = np.gradient(elev)
    return np.hypot(dy.mean(), dx.mean())

def local_height(point, lidar_filename):
    region = geom.mapping(point.buffer(500))
    elev = read(lidar_filename, region)
    ny, nx = elev.shape
    z0 = elev[ny // 2, nx // 2]
    return z0 - elev.min()

def local_relief(point, lidar_filename):
    region = geom.mapping(point.buffer(200))
    elev = read(lidar_filename, region)
    ny, nx = elev.shape
    z0 = elev[ny // 2, nx // 2]
    return z0 - elev.mean()

def generate_prediction_points(lidar):
    xmin, ymin, xmax, ymax = 3117065.,13860840., 3137630., 13884230.
    cellsize = 300.0

    funcs = dict(relief=relief, avg_slope=avg_slope, planar_slope=planar_slope,
                 local_height=local_height, local_relief=local_relief)
    columns = sorted(funcs.keys())

    output = []
    geoms = []
    yy, xx = np.mgrid[ymin:ymax:cellsize, xmin:xmax:cellsize]

    with open('grid_shape.txt', 'w') as outfile:
        outfile.write('{}, {}\n'.format(*yy.shape))

    for i, (x, y) in enumerate(zip(xx.flat, yy.flat)):
        print '{:0.2f}% done'.format(100.0 * i / xx.size)
        point = geom.Point(x, y)
        row = [funcs[key](point, lidar) for key in columns]
        geoms.append(point)
        output.append(row)

    return geopandas.GeoDataFrame(output, columns=columns, geometry=geoms)

def read(filename, poly, cellsize=None):
    with rio.open(filename, 'r') as src:
        if cellsize is None:
            # Assume squre and axis aligned -- True for this dataset...
            cellsize = src.affine[0]

        xmin, ymin, xmax, ymax = rio.features.bounds(poly)
        width = int((xmax - xmin) / float(cellsize)) + 1
        height = int((ymax - ymin) / float(cellsize)) + 1

        out_shape = (height, width)
        window = src.window(xmin, ymin, xmax, ymax)

        data = src.read(1, window=window, out_shape=out_shape, masked=True)

    return data

def reproject(point):
    """Not working on aws instance... Not sure why... Works on laptop.
    Probably a PROJ.4 configuration issue."""
    wgs84 = pyproj.Proj('+init=epsg:4326')
    native = pyproj.Proj(DEM_PROJECTION)
    x, y = pyproj.transform(wgs84, native, point.x, point.y)
    return geom.Point(x, y)

main()
