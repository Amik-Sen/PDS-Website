from django.shortcuts import render
import urllib.request, json 
import pandas as pd
import geopandas
import folium
import os
from django.conf import settings
from data_prep import prep
from covid_map import map_cov
# Create your views here.

# Creating paths for files 
def home(request):
    return render(request, 'base.html')

def plan(request):
    location_plan = request.get('')
    prep(location_plan)
    plan={}
    return render(request, 'plan.html',plan)

def visual(request):
    location_plan = request.get('')
    state = "West Bengal"
    prep(location_plan)
    visual={}
    return render(request, 'visual.html',visual)
def demand_rice(request):
    return

def demand_wheat(request):
    return

def demand_sugar(request):
    return