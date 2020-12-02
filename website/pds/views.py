from django.shortcuts import render
import urllib.request, json 
import pandas as pd
# Create your views here.
def home(request):
    def live_url_req():
        with urllib.request.urlopen("https://api.covid19india.org/state_district_wise.json") as url:
            df_district_wise_case = json.loads(url.read().decode())['West Bengal']['districtData']
            return df_district_wise_case
    df_district_wise_case = live_url_req()
    def district_wise_case():
        df_district_wise_case = live_url_req()
        state_district_wise_case = pd.DataFrame()
        for key, value in df_district_wise_case.items():
            for k, v in value.items():
                if k == 'confirmed':
                    temp_1 = pd.DataFrame({"B":[v],"A":[key], })
                    state_district_wise_case = state_district_wise_case.append(temp_1)
        state_district_wise_case. sort_values(by='B' , ascending= False, inplace=True)
        state_district_wise_case = state_district_wise_case.reset_index(drop=True)
        return state_district_wise_case
    state_district_wise_case = district_wise_case()
    table_data_1 = []
    for i in range(int(state_district_wise_case.shape[0])):
        temp = state_district_wise_case.iloc[i]
        table_data_1.append(dict(temp))
    context={'data':table_data_1[:12]}
    return render(request, 'base.html',context)