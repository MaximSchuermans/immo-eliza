from selenium import webdriver 
from selenium.webdriver.common.by import By
import threading 
from concurrent.futures import ThreadPoolExecutor
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
    """Get property URLs from a single page"""
    urls_from_each_page = []
    driver.get(url)
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'card__title-link')))
    except:
        pass

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

def collect_for_url(root_url):
    """Helper function to collect URLs for a specific root URL"""
    driver = web_driver()  # Create a new driver instance for each thread
    all_links = collect_urls(driver, root_url)
    driver.quit()  # Close the driver after the URL collection is done
    return all_links

def main():
    """Main function to collect URLs for apartments and houses concurrently"""
    start_time = time.time()  # Start timing URL collection

    root_urls = [
        'https://www.immoweb.be/en/search/apartment/for-sale',
        'https://www.immoweb.be/en/search/house/for-sale'
    ]
    
    # Use ThreadPoolExecutor to handle threads
    all_links = []
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = executor.map(collect_for_url, root_urls)
        for result in results:
            all_links.extend(result)
    
    # Write URLs to CSV file
    with open('properties_urls.csv', 'w') as file:
        for url in all_links:
            file.write(url + '\n')

    end_time = time.time()  # End timing URL collection
    print(f"Time taken to collect URLs: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()



