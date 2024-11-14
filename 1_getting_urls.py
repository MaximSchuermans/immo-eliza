from selenium import webdriver 
from selenium.webdriver.common.by import By
from threading import Thread
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def web_driver():
    driver = webdriver.Chrome()
    return driver

def accept_cookies(driver):
    """Accept cookies"""
    try:
        cssSelectorForHost1 = "#usercentrics-root"
        shadow_host = driver.find_element(By.ID, 'usercentrics-root')
        shadow_root = shadow_host.shadow_root
        cookie_button = shadow_root.find_element(By.CSS_SELECTOR, "button[data-testid='uc-accept-all-button']")
        cookie_button.click()
        time.sleep(2)  # Wait for page
    except:
        pass

def get_aparment_urls(driver, url):
    """Get url"""
    urls_from_each_page = []
    driver.get(url)
    
    # Wait for apartments to load
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'card__title-link')))

    apartments = driver.find_elements(By.CLASS_NAME, 'card__title-link')
    
    for apartment in apartments:        
        apartment_url = apartment.get_attribute('href')
        urls_from_each_page.append(apartment_url)
    
    return urls_from_each_page

def collect_urls(driver, root_url):
    """Get apartments urls"""

    # Store all urls of apartment in a list
    url_apartments_list = []
    
    for n in range(1,334):
        endpoint = f"?countries=BE&page={n}&orderBy=relevance"
        url = root_url + endpoint
        
        # Cookie botton
        if n == 1:
            accept_cookies(driver)
        
        # Get URLs from the page
        urls_from_each_page = get_aparment_urls(driver, url)
        url_apartments_list.extend(urls_from_each_page)
        
        print(f"Page {n}: Collected")
    
    return url_apartments_list

def main():
    links = []
    driver = web_driver()
    root_url = 'https://www.immoweb.be/en/search/apartment/for-sale'
    
    try:
        url_apartments_list = collect_urls(driver, root_url)
        links.append(url_apartments_list)
        
    finally:
        driver.quit()
    
    driver = web_driver()
    root_url = 'https://www.immoweb.be/en/search/house/for-sale'
    
    try:
        url_apartments_list = collect_urls(driver, root_url)
        links.append(url_apartments_list)
    finally:
        driver.quit()

    flat_links = [url for sublist in links for url in sublist]

    with open('properties_cvs_urls.csv', 'w') as file:
        for url in flat_links:
            file.write(url + '\n')

if __name__ == "__main__":
    main()