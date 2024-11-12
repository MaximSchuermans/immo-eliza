
from selenium import webdriver 
from selenium.webdriver.common.by import By
from threading import Thread
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

# Store all urls of apartment in a list
url_apartments_list = []

# Complete url with number of each page
root_url = 'https://www.immoweb.be/en/search/apartment/for-sale'
for n in range(1,5): ########Change it for 334 when solved   
    endpoint = f"?countries=BE&page={n}&orderBy=relevance"
    url = root_url + endpoint 
    driver.get(url)

    # Wait for page 
    time.sleep(2)

    # Cookie botton
    if n == 1:
        try:        
            cssSelectorForHost1 = "#usercentrics-root"
            shadow_host = driver.find_element(By.ID, 'usercentrics-root')
            shadow_root = shadow_host.shadow_root
            cookie_button = shadow_root.find_element(By.CSS_SELECTOR, "button[data-testid='uc-accept-all-button']")
            cookie_button.click()
            time.sleep(2)
        except:
            pass

    # In each page go throught each apartment listed and get url
    urls_from_each_page = []

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'card__title-link')))
    apartments = driver.find_elements(By.CLASS_NAME, 'card__title-link')

    #apartments = driver.find_elements(By.CLASS_NAME, 'card__title-link')
    
    for apartment in apartments:        
        apartment_url = apartment.get_attribute('href')      
        urls_from_each_page.append(apartment_url)

    url_apartments_list.append(urls_from_each_page)

# Store all urls in a document
with open('houses_apartments_urls.csv', 'w') as file:
    for page_apartments in url_apartments_list:  
        for url in page_apartments:
            file.write(url+'\n')