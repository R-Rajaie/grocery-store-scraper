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
driver.get("https://www.wegmans.com/stores/")
soup = BeautifulSoup(driver.page_source, 'html.parser')
time.sleep(1)

all_stores = []

links = soup.find(id="block-stores-landing-listing").find_all('a', href = True)
for link in links:
    link = link.get('href')
    if(link[0] == '/'):
        driver.get("https://www.wegmans.com" + link)
    else: 
        driver.get(link)
    time.sleep(1)
    store = BeautifulSoup(driver.page_source, 'html.parser')
    name = store.find(id="storeTitle").find('h1').get_text(strip = True)
    address = store.find(class_="store-address").get_text(separator =' ')
    address = ' '.join(address.split())
    address_parts = address.split(', ')
    address_parts[0] = address_parts[0].title()
    capitalized_address = ', '.join(address_parts)
    address = capitalized_address
    phone = store.find(class_="col-lg-6 order-lg-1 col-md-12 order-md-2 order-first store-phone").get_text(strip = True)
    print(name + " " + address + " " + phone)
    all_stores.append({"Name": name, "Address": address, "Phone": phone})
    driver.back()
    time.sleep(1)

df = pd.DataFrame(all_stores)
df.to_csv("wegmans.csv", index=False)
driver.quit()