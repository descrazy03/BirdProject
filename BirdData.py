
import numpy as np
import pandas as pd
import geopandas as gpd

class Data:

    #import DataFrame with parrot information 
    data = pd.read_csv('red_parrots_observations.csv', sep='\t', low_memory=False)[['day', 'month', 'year', 'locality', 'decimalLatitude', 'decimalLongitude']]
    data = data.rename(columns={'decimalLatitude': 'latitude', 'decimalLongitude': 'longitude'})

    #convert to GeoDataFrame and set projection
    obsv = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.longitude,data.latitude))
    obsv = obsv.set_crs(epsg=4326)

    #import SF Neighborhood Map shape file and set projection
    map = gpd.read_file('sf_neighborhoods/sf_neighborhoods.shp')
    map = map.to_crs(epsg=4326)

    #spatial join parrot data and neighborhood map
    nh = obsv.sjoin(map)

    #reproject map to fit base map
    con_map = map.to_crs(epsg=3857)

    def __init__(self):
        self.sightings = Data.nh[['day', 'month', 'year', 'latitude', 'longitude', 'geometry', 'name']].drop_duplicates()
    
    def most_freq_loc(self):
        """returns locations parrots are most sighted at and prints map with those coordinates"""

        locs = self.sightings[['name', 'latitude', 'longitude']]
        cts = locs.value_counts().head(5)
        df = pd.DataFrame(cts).reset_index()
        df = df.rename(columns={'name': 'Neighborhood', 'count': 'Sighting Count'})
        return df
    
    def by_season(self, season: str):
        """returns locations parrots are most sighted at during a season passed as parameter as well as percentage of total sightings"""

        locs = self.sightings[['name', 'latitude', 'longitude', 'month']]

        sea = {
            'winter':locs[(locs['month'] == 12) | (locs['month'] == 1) | (locs['month'] == 2)],
            'spring': locs[(locs['month'] == 3) | (locs['month'] == 4) | (locs['month'] == 5)],
            'summer': locs[(locs['month'] == 6) | (locs['month'] == 7) | (locs['month'] == 8)],
            'fall': locs[(locs['month'] == 9) | (locs['month'] == 10) | (locs['month'] == 11)]
        }

        recs_season = sea[season.lower()]
        n = recs_season.shape[0]
        df = pd.DataFrame(recs_season.drop('month', axis=1).value_counts().reset_index())
        df = df.rename(columns={'name': 'Neighborhood', 'count': 'Sighting Count'})
        return  df, n, ((n/self.sightings.shape[0]) * 100)
        
        
    def no_in_neighborhood(self, location: str):
        """returns number of sightings in a neighborhood passed as parameter"""

        locs = self.sightings.groupby('name')
        return locs.get_group(location)
    
    def most_at_location(self, location: str):
        """returns location parrots are most sighted at in a neighborhood passed as parameter"""

        locs = self.sightings[['name', 'latitude', 'longitude']]
        l = locs[locs['name'] == location]
        most = l.value_counts()
        df = pd.DataFrame(most).reset_index()
        df = df.rename(columns={'name': 'Neighborhood', 'count': 'Sighting Count'})
        return df.sort_values('Sighting Count', ascending=False)
    
    def print_neighborhoods(self):
        """returns a list of neighborhoods parrots have been sighted in"""

        neighbor = list(self.sightings['name'])
        return sorted(list(set(neighbor)))
    
    def percent_of_sightings(self, location: str):
        """returns percentage of total sightings that are reported in neighborhood passed as parameter"""

        total = self.sightings.shape[0]
        found = self.no_in_neighborhood(location).shape[0]
        pc = (found / total) * 100
        return pc
    
if __name__ == '__main__':
    bd = Data()
    data = bd.by_season('spring')
    print(data)