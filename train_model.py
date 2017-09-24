import sklearn
import sklearn.pipeline
from sklearn import preprocessing, ensemble
import pandas as pd
import geopandas

data = pd.read_csv('features_and_class.csv', na_values=['--'])
features = list(data.columns)[1:-1]
obs_class = data['flooded']

pipeline = sklearn.pipeline.Pipeline([
    ('Replace NaNs', preprocessing.Imputer(strategy='mean')),
    ('Scale data', preprocessing.StandardScaler()),
    ('Classification', ensemble.RandomForestClassifier(
                                            n_estimators=100,
                                            n_jobs=-1,
                                            )),
    ])

pipeline.fit(data[features].values, obs_class.values)

df = geopandas.read_file('prediction_features.geojson', driver='GeoJSON')
pred = pipeline.predict(df[features].values)

df['prediction'] = pred
df.to_file('prediction.geojson', driver='GeoJSON')

grid = pred.reshape(78, 69)

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.imshow(grid)
fig.savefig('prediction.png')


