from django import forms
from django.conf import settings
import os
import pandas as pd

state = 'West Bengal'
dis_lat_lon_dir = os.path.join(settings.BASE_DIR,'pds','Data_files and other codes','District Lat Long',state+'_District_lat_long.xlsx')
location_df = pd.read_excel(dis_lat_lon_dir,engine='openpyxl')
data = location_df['District'].tolist()
choices = []
for d in data:
    temp_tupple = []
    temp_tupple.append(d)
    temp_tupple.append(d)
    choices.append(tuple(temp_tupple))

class StateInputForm(forms.Form):
    state= forms.CharField(label='State:', widget=forms.Select(choices=[("West Bengal","West Bengal")],attrs={'style': 'width: 20%; margin-left:2%;margin-right:20%;'}))
    district= forms.CharField(label='District:', widget=forms.Select(choices=choices,attrs={'style': 'width: 25%;margin-left:2%;'}))