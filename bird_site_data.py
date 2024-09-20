import pandas as pd
import geopandas as gpd


data = pd.read_csv('red_parrots_observations.csv', sep='\t', low_memory=False)[['day', 'month', 'year', 'locality', 'decimalLatitude', 'decimalLongitude']]
obsv = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.decimalLongitude,data.decimalLatitude))
obsv = obsv.set_crs(epsg=4326)
#obsv = obsv.to_crs(epsg=3857)

print(obsv)