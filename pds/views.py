from django.shortcuts import render
import urllib.request, json 
import pandas as pd
import geopandas
import folium
import os
from django.conf import settings
from data_prep import prep
from covid_map import map_cov,district_wise_case
from .forms import StateInputForm
from json import dumps 
from rest_framework.views import APIView 
from rest_framework.response import Response 
# Create your views here.

# Creating paths for files 
def home(request):
    return render(request, 'base.html')

def plan(request):
    #location_plan = request.get('')
    #prep(location_plan)
    plan={}
    return render(request, 'plan.html',plan)

def visual(request):
    state = 'West Bengal'
    district = 'Bankura'
    dis_lat_lon_dir = os.path.join(settings.BASE_DIR,'pds','Data_files and other codes','District Lat Long',state+'_District_lat_long.xlsx')
    location_df = pd.read_excel(dis_lat_lon_dir,engine='openpyxl')
    location = location_df['District'].tolist()
    fps_map,num_fps,ws_map,num_ws = prep(district,state)
    cov_map = map_cov(district,state)
    visual={"location": location,"district":district,"fps_map":fps_map,"ws_map":ws_map,"cov_map":cov_map,"num_fps":num_fps,"num_ws":num_ws}
    return render(request, 'visual.html',visual)
class ChartData(APIView): 
    authentication_classes = [] 
    permission_classes = [] 
   
    def get(self, request, format = None): 
        state = 'West Bengal'
        district = 'Bankura'
        demand_path = os.path.join(settings.BASE_DIR,'pds','Data_files and other codes','Demand',state,district+'.xlsx')
        demand = pd.read_excel(demand_path,engine='openpyxl')
        data = []
        label= []
        for i in range(0,len(demand)):
            label_ =  demand['Date'][i]
            Demand = demand['Demand_Rice'][i]
            data.append(str(Demand))
            label.append(label_)
        data ={ 
                     "labels":label, 
                     "data":data, 
             } 
        return Response(data)