
from selenium import webdriver 
from selenium.webdriver.common.by import By
from threading import Thread
import time

driver = webdriver.Chrome()

# Store all urls of apartment in a list
url_apartments_list = []

# Complete url with number of each page
for n in range(1,2): ########Change it for 334 when solved 
    root_url = 'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page='
    endpoint = f'{n}&orderBy=relevance'
    url = root_url + endpoint 

    driver.get(url)
    time.sleep(2)

    # Cookie botton   
    cssSelectorForHost1 = "#usercentrics-root"
    shadow_host = driver.find_element(By.ID, 'usercentrics-root')
    shadow_root = shadow_host.shadow_root
    cookie_button = shadow_root.find_element(By.CSS_SELECTOR, "button[data-testid='uc-accept-all-button']")
    cookie_button.click()
    time.sleep(2)

    # In each page go throught each apartment listed and get url
    houses = driver.find_elements(By.XPATH, "//li[@class='search-results__item']")

    for house in houses:            
       link_element = house.find_element(By.XPATH, ".//a[contains(@class, 'card__title-link')]")
       house_url = link_element.get_attribute('href')
       url_apartments_list.append(house_url)

print(url_apartments_list)

