import urllib.request, json 
import time
import schedule
from geopy.geocoders import Nominatim
#nom = Nominatim(user_agent="http")
import pandas as pd
import os
from matplotlib import cm
from mpl_toolkits.basemap import Basemap  
import matplotlib.pyplot as plt 
import matplotlib as mpl
from mpl_toolkits.axes_grid.inset_locator import zoomed_inset_axes, mark_inset

def live_url_req():
	with urllib.request.urlopen("https://api.covid19india.org/state_district_wise.json") as url:
		df_district_wise_case = json.loads(url.read().decode())['West Bengal']['districtData']
    	#print(df_district_wise_case)
		return df_district_wise_case


def lat_long_(city):
    geolocator = Nominatim(user_agent="http")
#     city ="W.Dinajpur"
    country ="India"
    loc = geolocator.geocode(city+','+ country, timeout=10000)
    try:
        lat = loc.latitude
        long = loc.longitude
    except:
        lat = ""
        long = ""
    print("latitude is :-" ,lat,"\nlongtitude is:-" ,long)
    return lat, long

def district_wise_case():
	df_district_wise_case = live_url_req()
	state_district_wise_case = pd.DataFrame()
	
	for key, value in df_district_wise_case.items():
    	#print ("\n",key)
		lat, long = lat_long_(key)
		for k, v in value.items():
			if k == 'confirmed':
            	#print (k, " : ", v)
				temp_1 = pd.DataFrame({"District":[key], "Cases":[v], "Lattitude": lat, "Longitude": long})
				state_district_wise_case = state_district_wise_case.append(temp_1)
    
    
   # time.sleep(5)
	state_district_wise_case. sort_values(by='Cases' , ascending= False, inplace=True)
	state_district_wise_case = state_district_wise_case.reset_index(drop=True)
	return state_district_wise_case


def covid_map_plot():
	state_district_wise_case = district_wise_case()
	fig, ax = plt.subplots(figsize=(10,8))
	# map = Basemap(width=1200000,height=900000,projection='merc',resolution='l',
	#                     llcrnrlon=67,llcrnrlat=5,urcrnrlon=99,urcrnrlat=37,lat_0=28,lon_0=77)
	path1 = os.path.join("static","heatmap")
	path2 = os.path.join("static","img")
	map = Basemap(width=1200000,height=900000,projection='mill',resolution='h',
                    llcrnrlon=85.5,llcrnrlat=21.5,urcrnrlon=90,urcrnrlat=28,lat_0=28,lon_0=77)

	map.bluemarble()
	map.drawmapboundary ()
	map.drawcountries ()
	map.drawcoastlines ()
	map.drawstates()
	map.readshapefile(os.path.join(path1,"west_bengal_administrative"), '')

	lg=list(state_district_wise_case['Longitude'])
	lt=list(state_district_wise_case['Lattitude'])
	pt_label = list(state_district_wise_case['Cases'])
	temp = state_district_wise_case['Cases'].apply(lambda x: x)
	pt=list(temp)
	nc=list(state_district_wise_case['District'])


	cmap = mpl.colors.ListedColormap(['red','green', 'black', 'yellow', 'blue', 'cyan'])
	x, y = map(lg, lt)
	print ("\n\nx : ", x, "\n y : ", y)
	plt.scatter(x, y, s=pt, marker="o", c=pt_label, cmap=cmap, alpha=0.7)

	map.colorbar(location="right")

	fig.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
	fig.gca().xaxis.set_major_locator(plt.NullLocator())
	fig.gca().yaxis.set_major_locator(plt.NullLocator())
	save_file = os.path.join(path2,"6.jpg")
	if os.path.isfile(save_file):
		os.remove(save_file)
	fig.savefig(save_file, bbox_inches = 'tight',pad_inches = 0)

schedule.every().day.at("12:30").do(covid_map_plot)

while True:
    schedule.run_pending()
    time.sleep(1)