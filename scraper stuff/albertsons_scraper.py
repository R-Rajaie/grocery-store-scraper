from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
from bs4 import BeautifulSoup 

# Boot up chromedriver, set up bs4
service = Service(executable_path='./chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
url = "https://local.albertsons.com/"
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'html.parser')
time.sleep(1)

all_stores = []

def add_info(location):
    name = location.find(class_="RedesignHero-subtitle Heading--lead").get_text(strip = True)
    address = location.find(class_="c-address-street-1").get_text(strip = True) + ", " + location.find(class_="c-address-city").get_text(strip = True) + " " + location.find(class_="c-address-state").get_text(strip = True) + " " + location.find(class_="c-address-postal-code").get_text(strip = True)
    phone = location.find(class_="Phone-link").get_text(strip = True)
    print(name + " " + address + " " + phone)
    all_stores.append({"Name": name, "Address": address, "Phone": phone})

states = soup.find_all(class_="Directory-listLink")
for state in states:
    driver.get("https://local.albertsons.com/" + state.get('href'))
    
    if state.get('data-count') == '(1)':
        add_info(BeautifulSoup(driver.page_source, 'html.parser'))
        driver.back()
    else:
        time.sleep(1)
        cities_soup = BeautifulSoup(driver.page_source, 'html.parser')

        cities = cities_soup.find_all(class_="Directory-listLink")

        for city in cities:
            driver.get("https://local.albertsons.com/" + city['href'])

            if city.get('data-count') == '(1)':
                add_info(BeautifulSoup(driver.page_source, 'html.parser'))
                driver.back()
            else:
                time.sleep(1)
                locations_soup = BeautifulSoup(driver.page_source, 'html.parser')
                
                locations = locations_soup.find_all(class_="Teaser Teaser--ace Teaser--directory")

                for location in locations:
                    driver.get("https://local.albertsons.com/" + location.find(class_="Teaser-titleLink").get('href'))
                    add_info(BeautifulSoup(driver.page_source, 'html.parser'))
                    
                    driver.back()
                    time.sleep(1)
                
                driver.back()
                time.sleep(1)
            time.sleep(1)

df = pd.DataFrame(all_stores)
df.to_csv("albertsons_locations.csv", index=False)
driver.quit()