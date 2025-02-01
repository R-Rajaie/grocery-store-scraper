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
driver.get("https://www.target.com/store-locator/store-directory")
soup = BeautifulSoup(driver.page_source, 'html.parser')
time.sleep(1)

all_stores = []

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas' 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New-Hampshire', 'New-Jersey', 'New-Mexico', 'New-York', 'North-Carolina', 'North-Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode-Island', 'South-Carolina', 'South-Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West-Virginia', 'Wisconsin', 'Wyoming']

for state in states:

    driver.get("https://www.target.com/store-locator/store-directory/" + state)
    time.sleep(0.5)
    locations = BeautifulSoup(driver.page_source, 'html.parser').find_all(class_="view_cityName__0wH8j")

    for location in locations:
        if(location.get('data-city')):
            # Case where there are multiple stores and it shows sidebar
            city = location.find(class_='styles_cityNameButton__0L0dl').get_text()
            link_element = driver.find_element(By.XPATH, f"//button[@class='styles_cityNameButton__0L0dl' and text()='{city}']")
            link_element.click()
            time.sleep(0.5)
            
            for location in BeautifulSoup(driver.page_source, 'html.parser').find_all(class_="styles_card__2hscu"):
                name = location.find(class_="styles_storeCardTitle__4tfVK").get_text().replace("store details", "")
                address = location.find(class_="styles_storeCardLink__i0HD4").get_text()
                location = location.find(class_="h-display-inline-block")
                phone = location.find(attrs={'data-test': '@store-locator/StorePhoneNumberLink'}).get_text()
                print(name + ": " + address + ", " + phone)
                all_stores.append({"Name": name, "Address": address, "Phone": phone})
        else:
            # Case where there is only one store and it links directly to the page 
            a = location.find('a', class_='view_cityNameLink__0zEsC')
            driver.get("https://www.target.com" + a['href'])

            store = BeautifulSoup(driver.page_source, 'html.parser')
            while not store.find('h1', class_='styles_storeNameHeading__jHgh9'): time.sleep(0.25)

            name = store.find('h1', class_='styles_storeNameHeading__jHgh9').get_text()
            info_block = store.find(class_='styles_storeInfo__6U4g_').decode_contents().split('<br/>')
            address = info_block[0].strip() + ", " + info_block[1].strip()
            phone = info_block[2].replace('Phone: ', '').strip()
            print(name + ": " + address + ", " + phone)
            all_stores.append({"Name": name, "Address": address, "Phone": phone})

            driver.back()
            
        driver.get("https://www.target.com/store-locator/store-directory/" + state)
        time.sleep(0.25)
        
    driver.back()


df = pd.DataFrame(all_stores)
df.to_csv("target_locations.csv", index=False)
driver.quit()