from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
from bs4 import BeautifulSoup

# Get Chromedriver up and running
service = Service(executable_path='./chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
url = "https://www.wholefoodsmarket.com/stores"
driver.get(url)

# Function to get store locations for a specific state
def get_store_locations(state):

    # Find the search bar and enter the state name
    search_bar = driver.find_element(By.ID, "store-finder-search-bar")
    search_bar.clear()
    search_bar.send_keys(state)
    search_bar.send_keys(Keys.ENTER)
    
    # Allow time for the page to load, can be lengthened or shortened to your liking
    time.sleep(2)
    
    # Parse the page content
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    numbers = []
    addresses = []
    names = []

    # Finds phone number area, isolates phone number, adds to list
    pn_list = soup.find_all(class_="w-phone-number--link")
    for pn in pn_list:
        numbers.append(pn.find(class_="w-call-icon").get_text(strip = True))
    
    # Finds street address and city/state address, appends them together, adds to list
    address_list = soup.find_all(class_="storeAddress")
    for address in address_list:
        address_divs = address.find_all('div', class_='w-store-finder-mailing-address')
        add = ', '.join([div.get_text(strip=True) for div in address_divs])
        addresses.append(add)

    # Finds store name and adds it to list
    name_list = soup.find_all(class_="w-store-finder-store-name")
    for name in name_list:
        names.append(name.find(class_="w-link w-link--text").get_text())

    # Converts the 3 lists into a dictionary
    stores = {
        'Store Name': names,
        'Address': addresses,
        'Phone': numbers
    }
    return stores

# Iterates through all states
states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
all_stores = []
for state in states:
    print(f"Getting stores for {state}")
    stores = get_store_locations(state)
    print(stores)
    store_data = list(zip(stores['Store Name'], stores['Address'], stores['Phone']))
    all_stores.extend(store_data)

# Convert the list to a DataFrame and saves to csv
df = pd.DataFrame(all_stores, columns=['Store Name', 'Address', 'Phone'])
df.to_csv("whole_foods_locations.csv", index=False)

# Close the browser
driver.quit()