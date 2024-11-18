from selenium import webdriver 
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def web_driver():
    "Create and return a new instance of a Chrome WebDriver"
    driver = webdriver.Chrome()
    return driver

def accept_cookies(driver):
    """Accept cookies"""
    try:
        shadow_host = driver.find_element(By.ID, 'usercentrics-root')
        shadow_root = shadow_host.shadow_root
        cookie_button = shadow_root.find_element(By.CSS_SELECTOR, "button[data-testid='uc-accept-all-button']")
        cookie_button.click()
        time.sleep(2)  
    except:
        pass

def extract_page_property_urls(driver, url):
    """Extract property URLs from a webpage"""
    urls_single_page = []
    driver.get(url)
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'card__title-link')))
    except:
        pass

    properties = driver.find_elements(By.CLASS_NAME, 'card__title-link')
    
    for property in properties:        
        property_url = property.get_attribute('href')
        urls_single_page.append(property_url)
    
    return urls_single_page

def scrape_all_property_urls(driver, root_url):
    """Extract properties URLs from multiple pages of a website"""

    urls_properties = [] 
    
    for n in range(1,334):
        endpoint = f"?countries=BE&page={n}&orderBy=relevance"
        url = root_url + endpoint
        
        if n == 1:
            accept_cookies(driver)
        
        urls_from_each_page = extract_page_property_urls(driver, url)
        urls_properties.extend(urls_from_each_page)
        
        print(f"Page {n}: Collected")
    
    return urls_properties

def scrape_urls_for_root(root_url):
    """Helper function to collect returns apartment URLs."""
    driver = web_driver()  
    all_links = scrape_all_property_urls(driver, root_url)
    driver.quit()  
    return all_links

def remove_duplicates():
    """Remove duplicates from the file properties_urls.txt and overwrite it"""
    with open('data/url_list.txt', 'r') as file:
        urls = file.readlines()
    
    initial_count = len(urls)
    unique_urls = set(url.strip() for url in urls)
    final_count = len(unique_urls)

    with open('data/url_list.txt', 'w') as file:
        for url in unique_urls:
            file.write(url + '\n')

    print(f"URLs before removing duplicates: {initial_count}")
    print(f"URLs after removing duplicates: {final_count}")

def main():
    """Main function to collect URLs for apartments and houses concurrently"""
    start_time = time.time()  # Start timing URL collection

    root_urls = [
        'https://www.immoweb.be/en/search/apartment/for-sale',
        'https://www.immoweb.be/en/search/house/for-sale'
    ]
    
    all_links = []
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = executor.map(scrape_urls_for_root, root_urls)
        for result in results:
            all_links.extend(result)
    
    with open('data/url_list.txt', 'w') as file:
        for url in all_links:
            file.write(url + '\n')

    remove_duplicates() 

    end_time = time.time()  # End timing URL collection
    print(f"Time taken to collect URLs: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
