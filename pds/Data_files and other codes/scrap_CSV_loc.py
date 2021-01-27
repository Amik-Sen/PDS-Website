"""
install pandas and selenium
and install chrome driver from "https://www.youtube.com/redirect?redir_token=QUFFLUhqbkVLU2tSSDh3bVUzcWFlY2ItUzBEdE1Wcl94UXxBQ3Jtc0tuT0VocHJ6VjNVMVFZR3ZUWmM3UkpwVE5yYTdLeTlJbENacnhYbENNc09qLUE5RzA3RWs3YjdCRU53V1VFODQwR0FKVmZqU0ZlV0s2bU9sYV9QajQtNGZjQ283LTMzVlpkaURTb0pSMkNLV3FNVDFTYw%3D%3D&q=https%3A%2F%2Fsites.google.com%2Fa%2Fchromium.org%2Fchromedriver%2Fdownloads&event=video_description&v=Xjv1sY630Uc"
accoring do your chrome version chose the appropriate exe. file

"""

import pandas as pd

FPS_Store = pd.read_excel("Data\\FPS_Full.xlsx")
FPS_Store.head()
FPS_Store['Shop Address'] = FPS_Store['Address'].astype(str)
FPS_Store['Village Name'] = FPS_Store['Division Name'].astype(str)
FPS_Store['Full_Address'] = FPS_Store['Shop Address'] + ", "+FPS_Store['Village Name']
FPS_Store['Full_Address'] =FPS_Store['Full_Address'].astype(str)

from selenium import webdriver
import time
Url_With_Coordinates = []

option = webdriver.ChromeOptions()
# option.add_argument("--incognito")
# option.add_argument("headless")
option.add_argument("--enable-javascript")
# prefs = {'profile.default_content_setting_values': {'images':2, 'javascript':2}}
# option.add_experimental_option('prefs', prefs)




FPS_Store['Url'] = ['https://www.google.com/maps/search/' + str(i) for i in FPS_Store['Full_Address'] ]

driver = webdriver.Chrome("C:\\Program Files (x86)\\chromedriver.exe", options=option)	#give your own location where your chrome drive is.

for url in FPS_Store.Url:
    
    driver.get(url)
    print ("url : ", driver.find_element_by_css_selector('meta[itemprop=image]').get_attribute('content'))
    Url_With_Coordinates.append(driver.find_element_by_css_selector('meta[itemprop=image]').get_attribute('content'))
driver.close()
