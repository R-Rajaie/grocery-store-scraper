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
url = "https://www.kroger.com/stores/grocery"
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Function to get store information from a store page using BeautifulSoup
def get_store_info(store_element):
    time.sleep(1)  # Wait for the store page to load completely
    name = store_element.find(class_="kds-Link kds-Link--inherit heading-l").get_text(strip = True) 
    address = store_element.find(class_="kds-Text--l mb-16").get_text(strip = True) 
    phone = store_element.find(class_="flex flex-col").find(class_="kds-Text--l mb-16").get_text(strip = True) 
    return {"Name": name, "Address": address, "Phone": phone}

# Initialize a list to hold all stores
all_stores = []

# Extract the list of states and cities grouped by state
state_elements = soup.find_all(class_="items-left flex flex-col")

# Iterate through each state
for state_element in state_elements:
    state_name = state_element.find(class_="kds-Link kds-Link--inherit").get_text(strip = True)

    # Extract the list of cities in the state
    city_elements = state_element.select("div.link-hub-element-link.py-16 a.kds-Link") 

    for city_element in city_elements:
        city_name = city_element.text.strip()
        city_url = city_element['href']

        # Navigate to the city page
        driver.get("https://www.kroger.com" + city_url)
        time.sleep(1)  # Wait for the page to load

        # Extract the list of stores in the city
        city_soup = BeautifulSoup(driver.page_source, 'html.parser')
        store_elements = city_soup.find_all(class_="store-card-container m-12 border rounded-large p-24 border-neutral-least-prominent flex flex-col justify-between")
        for store_element in store_elements:
            store_info = get_store_info(store_element)
            print(store_info)
            store_info["State"] = state_name
            store_info["City"] = city_name
            all_stores.append(store_info)

            time.sleep(1)

        # Navigate back to the list of cities
        driver.back()
        time.sleep(1)

# Convert list to dataframe into csv, quit chromedriver
df = pd.DataFrame(all_stores)
df.to_csv("kroger_locations.csv", index=False)
driver.quit()