from django.shortcuts import render
import urllib.request, json 
import pandas as pd
import geopandas
import folium
import os
from django.conf import settings
# Create your views here.

# Creating paths for files 
def home(request):
    # Function to access API for covid 
    def live_url_req():
        with urllib.request.urlopen("https://api.covid19india.org/state_district_wise.json") as url:
            df_district_wise_case = json.loads(url.read().decode())['West Bengal']['districtData']
            return df_district_wise_case
    df_district_wise_case = live_url_req()
    # Function to get the state wise COVID data in a pd dataframe
    def district_wise_case():
        df_district_wise_case = live_url_req()
        state_district_wise_case = pd.DataFrame()
        for key, value in df_district_wise_case.items():
            for k, v in value.items():
                if k == 'confirmed':
                    temp_1 = pd.DataFrame({"Cases":[v],"District":[key]})
                    state_district_wise_case = state_district_wise_case.append(temp_1)
        state_district_wise_case. sort_values(by='Cases' , ascending= False, inplace=True)
        state_district_wise_case = state_district_wise_case.reset_index(drop=True)
        return state_district_wise_case
    # Normal codes for doing stuffs
    state_district_wise_case = district_wise_case()
    select_data_district = []
    df2 = {'Cases': state_district_wise_case.at[12,'Cases']+state_district_wise_case.at[9,'Cases'],'District': 'Barddhaman'}
    state_district_wise_case = state_district_wise_case.append(df2, ignore_index = True)
    state_district_wise_case.sort_values(by='Cases' , ascending= False, inplace=True)
    # Creating dictionary for state/ District wise Data
    for i in range(int(state_district_wise_case.shape[0])):
        temp = state_district_wise_case.iloc[i]
        select_data_district.append(dict(temp))
    # Map Data from Static files
    file_path_choropleth=os.path.join(settings.BASE_DIR,'static','IndiaStateTopojsonFiles-master','WestBengal.geojson')
    west_bengal_geojson=geopandas.read_file(file_path_choropleth)
    # Map for the COVID cases choropleth
    m = folium.Map(location=[22.9868,87.8550], tiles='cartodbpositron', zoom_start=8)
    folium.Choropleth(
        geo_data=west_bengal_geojson,
        name="choropleth",
        data=state_district_wise_case,
        columns=["District", "Cases"],
        key_on="feature.properties.Dist_Name",
        fill_color="YlGn",
        fill_opacity=0.5,
        line_opacity=0.2,
        legend_name="Active covid cases",).add_to(m)
    folium.LayerControl().add_to(m)
    m = m._repr_html_()  
    # Final context dictionary 
    context={'data':select_data_district, 'covid_map':m}


    return render(request, 'base.html',context)
