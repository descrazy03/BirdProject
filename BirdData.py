
import numpy as np
import pandas as pd
import geopandas as gpd
import contextily as cx
import matplotlib.pyplot as plt

class Data:

    data = pd.read_csv('red_parrots_observations.csv', sep='\t', low_memory=False)[['day', 'month', 'year', 'locality', 'decimalLatitude', 'decimalLongitude']]
    obsv = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.decimalLongitude,data.decimalLatitude))
    obsv = obsv.set_crs(epsg=4326)
    map = gpd.read_file('sf_neighborhoods/sf_neighborhoods.shp')
    map = map.to_crs(epsg=4326)
    nh = obsv.sjoin(map)
    con_map = map.to_crs(epsg=3857)
    basemap, basemap_extent = cx.bounds2img(*con_map.total_bounds, zoom=15, ll = False, source=cx.providers.OpenStreetMap.Mapnik)

    def __init__(self):
        self.sightings = Data.nh[['day', 'month', 'year', 'decimalLatitude', 'decimalLongitude', 'geometry', 'name']].drop_duplicates()
    
    def most_freq_loc(self):
        locs = self.sightings[['name', 'decimalLatitude', 'decimalLongitude']]
        cts = locs.value_counts().head(5).index
        head = pd.DataFrame(list(cts), columns=['name', 'decimalLatitude', 'decimalLongitude']).set_index('name')
        geo_head = gpd.GeoDataFrame(head, geometry=gpd.points_from_xy(head.decimalLongitude,head.decimalLatitude)).set_crs(epsg=4326)
        con_geo = geo_head.to_crs(epsg=3857)
        f, ax1 = plt.subplots(1, figsize= (15,15))
        ax1.set_title('Most Frequent Sightings')
        plt.imshow(Data.basemap, extent=Data.basemap_extent)
        con_geo.plot(ax=plt.gca(), marker = 'o', markersize=100, alpha=.75)
        ax1.set_axis_off()
        plt.axis()
        plt.show()
        return list(cts)
    
    def by_season(self, season: str):
        locs = self.sightings[['name', 'decimalLatitude', 'decimalLongitude', 'month']]
        if season == 'winter':
            w = locs[(locs['month'] == 12) | (locs['month'] == 1) | (locs['month'] == 2)]
            ws = w.shape[0]
            return w.drop('month', axis=1).value_counts().head(5).index, ws, (ws / self.sightings.shape[0]) * 100
        if season == 'spring':
            s = locs[(locs['month'] == 3) | (locs['month'] == 4) | (locs['month'] == 5)]
            ss = s.shape[0]
            return s.drop('month', axis=1).value_counts().head(5).index, ss, (ss / self.sightings.shape[0]) * 100
        if season == 'summer':
            su = locs[(locs['month'] == 6) | (locs['month'] == 7) | (locs['month'] == 8)]
            sus = su.shape[0]
            return su.drop('month', axis=1).value_counts().head(5).index, sus, (sus / self.sightings.shape[0]) * 100
        if season == 'fall':
            f = locs[(locs['month'] == 9) | (locs['month'] == 10) | (locs['month'] == 11)]
            fs = f.shape[0]
            return f.drop('month', axis=1).value_counts().head(5).index, fs, fs / (self.sightings.shape[0]) * 100
        
    def no_in_neighborhood(self, location: str):
        locs = self.sightings.groupby('name')
        return locs.get_group(location).shape[0]
    
    def most_at_location(self, location: str):
        locs = self.sightings[['name', 'decimalLatitude', 'decimalLongitude']]
        l = locs[locs['name'] == location]
        most = l.value_counts().head(1).index[0]
        h = pd.DataFrame(most).transpose()
        h.columns = ['name', 'decimalLatitude', 'decimalLongitude']
        h = h.set_index('name')
        p = gpd.GeoDataFrame(h, geometry=gpd.points_from_xy(h.decimalLongitude,h.decimalLatitude)).set_crs(epsg=4326)
        con_p = p.to_crs(epsg=3857)
        f, ax1 = plt.subplots(1, figsize= (15,15))
        ax1.set_title(f'Most Frequent Sightings at {location}')
        plt.imshow(Data.basemap, extent=Data.basemap_extent)
        con_p.plot(ax=plt.gca(), marker = 'o', markersize=100, alpha=.75)
        ax1.set_axis_off()
        plt.axis()
        plt.show()
        return most
    
    def print_neighborhoods(self):
        neighbor = list(self.sightings['name'])
        return sorted(list(set(neighbor)))
    
    def percent_of_sightings(self, location: str):
        total = self.sightings.shape[0]
        found = self.no_in_neighborhood(location)
        pc = (found / total) * 100
        return pc
    
    def neighborhood_distribution(self):
        n = self.sightings['name'].value_counts().index
        v = self.sightings['name'].value_counts().values
        df = pd.DataFrame({'name': n, 'count': v})
        conm = Data.con_map.copy()
        m = conm.merge(df, how='outer').fillna(0)
        f, ax1 = plt.subplots(1, figsize=(15,15))
        ax1.set_title("Sightings per Neighborhood")
        plt.imshow(Data.basemap, extent=Data.basemap_extent)
        m.plot('count', ax=plt.gca(), cmap='Wistia', alpha=.5, legend=True, legend_kwds={'orientation':"horizontal"})
        ax1.set_axis_off()
        plt.axis(m.total_bounds[[0,2,1,3]])
        plt.show()


    
if __name__ == '__main__':
    bd = Data()
    print(bd.most_at_location('Financial District'))