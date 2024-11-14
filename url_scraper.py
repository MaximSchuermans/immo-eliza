from concurrent.futures import ThreadPoolExecutor, as_completed 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import threading
import time  # Import time module

# Define headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

cookie_url = "https://www.immoweb.be"

def web_driver():
    """Initialize and return a Selenium WebDriver"""
    driver = webdriver.Chrome()
    return driver

def accept_cookies(driver):
    """Accept cookies if the pop-up is present"""
    try:
        shadow_host = driver.find_element(By.ID, 'usercentrics-root')
        shadow_root = shadow_host.shadow_root
        cookie_button = shadow_root.find_element(By.CSS_SELECTOR, "button[data-testid='uc-accept-all-button']")
        cookie_button.click()
        WebDriverWait(driver, 2).until(EC.staleness_of(cookie_button))  # Wait until the cookie banner disappears
    except Exception:
        pass

def get_apartment_urls(driver, url):
    """Get apartment URLs from a given page"""
    driver.get(url)
    
    # Wait for apartments to load
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'card__title-link')))
    
    apartments = driver.find_elements(By.CLASS_NAME, 'card__title-link')
    return [apartment.get_attribute('href') for apartment in apartments]

def collect_urls(driver, root_url, start_page=1, end_page=100):
    """Collect apartment URLs across multiple pages"""
    all_urls = []
    
    for n in range(start_page, end_page + 1):
        endpoint = f"?countries=BE&page={n}&orderBy=relevance"
        url = root_url + endpoint
        
        # Accept cookies on the first page
        if n == start_page:
            accept_cookies(driver)
        
        # Collect URLs from the current page
        urls_from_page = get_apartment_urls(driver, url)
        all_urls.extend(urls_from_page)
        
        print(f"Page {n}: Collected {len(urls_from_page)} URLs")
    
    return all_urls

def main():
    """Main function to collect URLs for apartments and houses concurrently"""
    start_time = time.time()  # Start timing URL collection

    driver = web_driver()
    root_urls = [
        'https://www.immoweb.be/en/search/apartment/for-sale',
        'https://www.immoweb.be/en/search/house/for-sale'
    ]
    
    all_links = []

    def collect_for_url(root_url):
        """Helper function to collect URLs for a specific root URL"""
        urls = collect_urls(driver, root_url)
        all_links.extend(urls)

    # Start threads for apartment and house URL collection
    threads = []
    for url in root_urls:
        thread = threading.Thread(target=collect_for_url, args=(url,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    
    driver.quit()  # Close the driver after all URL collection is done

    end_time = time.time()  # End timing URL collection
    print(f"Time taken to collect URLs: {end_time - start_time:.2f} seconds")

    return all_links

if __name__ == '__main__':
    print("Starting scraping of urls")
    main()
