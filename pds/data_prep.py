import os
import urllib.request, json
from django.conf import settings
import folium
import pandas as pd

def prep(location,state):
    dis_lat_lon_dir = os.path.join(settings.BASE_DIR,'Data_files and other codes','District Lat Long',state+'_District_lat_long.xlsx')
    fps_dir = os.path.join(settings.BASE_DIR,'Data_files and other codes','FPS',state,'Fps_'+location+'.xlsx')
    whole_dir = os.path.join(settings.BASE_DIR,'Data_files and other codes','Wholesalers',state,'wholesaler_'+location+'.xlsx')
    location_df = pd.read_excel(dis_lat_lon_dir)
    location_cor = location_df.loc[location_df['District'] == location]
    location_cor = location_cor.drop(['District'], axis = 1)
    location_cor = location_cor.values.tolist()
    fps_data = pd.read_excel(fps_dir)
    fps_map_data = fps_data.loc[:,['lat','long']]
    fps_map_data = fps_map_data.dropna(subset = ['lat'], inplace=False)
    fps_location = fps_map_data.values.tolist()
    fps_map = folium.Map(location=location_cor[0],tiles='cartodbpositron',zoom_start=9.5)
    for point in range(0, len(fps_location)):
        folium.Marker(fps_location[point], popup=fps_data['FPS Code'][point], icon=folium.Icon(color='darkred', icon_color='white', icon='building', angle=0, prefix='fa')).add_to(fps_map)
    fps_map=fps_map._repr_html_() 
    wholesaler_data = pd.read_excel(whole_dir)
    wholesaler_map_data = wholesaler_data.loc[:,['lat','long']]
    wholesaler_map_data = wholesaler_map_data.dropna(subset = ['lat'], inplace=False)
    wholesaler_location = wholesaler_map_data.values.tolist()
    wholesaler_map = folium.Map(location=location_cor[0],tiles='cartodbpositron',zoom_start=10)
    for point in range(0, len(wholesaler_location)):
        folium.Marker(wholesaler_location[point], popup=location, icon=folium.Icon(color='green', icon_color='white', icon='truck', angle=0, prefix='fa')).add_to(wholesaler_map)
    wholesaler_map=wholesaler_map._repr_html_()
    fps_map_path = os.path.join(settings.BASE_DIR,'template','fps_map.html')
    whole_map_path = os.path.join(settings.BASE_DIR,'template','whole_map.html')
    wholesaler_map.save(outfile=whole_map_path)
    fps_map.save(outfile=fps_map_path)
    return fps_map,len(fps_location) ,wholesaler_map,len(wholesaler_location)
