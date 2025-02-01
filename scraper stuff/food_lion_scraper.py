# Food Lion, Stop & Shop, GIANT, Giant Food, and Hannaford are all part of Ahold Delhaize and have nearly identical store locators. They are also very similar to what Safeway and Albertsons have.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from bs4 import BeautifulSoup 

# Boot up chromedriver, set up bs4
service = Service(executable_path='./chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
url = "https://stores.foodlion.com/"
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'html.parser')
time.sleep(1)

all_stores = []

def get_info_one(location):
    name = location.find(class_="LocationName--hero").get_text()
    address = location.find(class_="Address-field Address-line1").get_text() + ", " + location.find(class_="Address-field Address-city").get_text() + " " + location.find(itemprop="addressRegion").get_text() + " " + location.find(class_="Address-field Address-postalCode").get_text()
    if location.find(class_="Link Phone-link"): phone = location.find(class_="Link Phone-link").get_text()
    else: phone = ""
    print(name + " " + address + " " + phone)
    all_stores.append({"Name": name, "Address": address, "Phone": phone})

def get_info_multiple(page):
    locations = page.find_all(class_="Directory-listTeaser")
    for location in locations:
        suffix = location.find(class_="Teaser-cta Teaser-cta--directory").get('href')
        driver.get("https://stores.foodlion.com/" + suffix)
        time.sleep(1)
        get_info_one(BeautifulSoup(driver.page_source, 'html.parser'))


states = soup.find_all(class_="Directory-listItem")
for state in states: 
    suffix = state.find(class_="Directory-listLink").get('href')
    driver.get("https://stores.foodlion.com/" + suffix)
    time.sleep(1)
    
    state_locs = BeautifulSoup(driver.page_source, 'html.parser')
    cities = state_locs.find_all(class_="Directory-listLink")

    for city in cities:
        suffix = city['href']
        driver.get("https://stores.foodlion.com/" + suffix)
        time.sleep(1)
        info = BeautifulSoup(driver.page_source, 'html.parser')

        if(city['data-count'] == "(1)"):
            get_info_one(info)
        else:
            get_info_multiple(info)
        
df = pd.DataFrame(all_stores)
df.to_csv("food_lion_locations.csv", index=False)
driver.quit()