import requests 
from selenium import webdriver
from bs4 import BeautifulSoup 
from requests import Session
import json 
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import time
from tqdm import tqdm

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

cookie_url = "https://www.immoweb.be"
def get_cookies():
    """Accept cookies"""
    req_cookies = requests.get(cookie_url, headers=headers)
    cookies = req_cookies.cookies
    return cookies

def get_script(url):
    """Get json dictionary from a single URL"""
    with requests.Session() as session:
        response = session.get(url, cookies=get_cookies(), headers=headers)
        #driver = webdriver.Chrome()
        #driver.get(url)
        #soup = BeautifulSoup(driver.page_source, 'html.parser')
        soup = BeautifulSoup(response.content, 'html.parser')

        try:
            scripts = soup.find_all('script', attrs={"type" :"text/javascript"})
            
            for script in scripts:
                script_text = script.string
                if script_text and 'window.classified' in script_text:
                    json_str = script_text.strip().replace('window.classified = ', '').rstrip(';')
                    json_data = json.loads(json_str)
                    break
            return json_data
        except:
            pass

def get_value(data, *keys):
    """Extract a nested value from a dictionary using a sequence of keys.
       Returns None if the key or value is not found or if the value is None."""
    for key in keys:
        if isinstance(data, dict) and key in data:
            value = data[key]
            if value is None:  # Check if the value is None
                return None
            elif isinstance(value, bool):  # If it's a boolean, return 1 for True and 0 for False
                return int(value)
            else:
                data = value  
        else:
            return None  # Return None if the key is not found
    
    return data  # Return the found value if it's not None

def extracted_data(json_data):
    """Creates a dictionary for each property by extracting the required values from json_data"""
    extracted_data = { }

    extracted_data["Price"] = get_value(json_data, "price", "mainValue")
    #extracted_data["Type_of_Sale_isPubli"] = get_value(json_data, "flags", "isPublicSale") 
    #extracted_data["Type_of_Sale_isNotary"] = get_value(json_data, "flags", "isNotarySale")     
    extracted_data["Locality"] = get_value(json_data, "property", "location", "postalCode")
    extracted_data["Type_of_Property"] = get_value(json_data, "property", "type")
    extracted_data["Subtype_of_Property"] = get_value(json_data, "property", "subtype")
    extracted_data["State_of_the_Building"] = get_value(json_data, "property", "building", "condition")
    extracted_data["Number_of_Rooms"] = get_value(json_data, "property", "bedroomCount") 
    extracted_data["Living_Area"] = get_value(json_data, "property", "netHabitableSurface")
    extracted_data["Fully_Equipped_Kitchen"] = get_value(json_data, "property", "kitchen", "type") == "HYPER_EQUIPPED"
    extracted_data["Furnished"] = get_value(json_data, "transaction","sale", "isFurnished")
    extracted_data["Open_fire"] = get_value(json_data, "property", "fireplaceCount")
    extracted_data["Terrace"] = get_value(json_data, "property", "hasTerrace")
    extracted_data["Terrace_Area"] = get_value(json_data, "property", "terraceSurface")
    extracted_data["Garden"] = get_value(json_data, "property", "hasGarden")
    extracted_data["Garden_Area"] = get_value(json_data, "property", "gardenSurface")
    extracted_data["Surface_of_the_Land"] = get_value(json_data, "property", "gardenSurface")
    extracted_data["Surface_area_plot_of_land"] = get_value(json_data, "property", "land", "surface")
    extracted_data["Number_of_Facades"] = get_value(json_data, "property", "building", "facadeCount")
    extracted_data["Swimming_Pool"] = get_value(json_data, "property", "hasSwimmingPool")    

    extracted_data["Disabled_Access"] = get_value(json_data, "property", "hasDisabledAccess") 
    extracted_data["Lift"] = get_value(json_data, "property", "hasLift") 
    
    return extracted_data 

def extract_data_for_url(url):
    """Extract data for a single UR."""
    json_data = get_script(url)
    if json_data:
        return extracted_data(json_data)
    return None

def extracted_multiple_data(urls):
    """Extract data from multiple URLs concurrently."""
    all_data = []
    with ThreadPoolExecutor(max_workers=10) as executor:  
        for data in tqdm(executor.map(extract_data_for_url, urls), total=len(urls), desc="Processing URLs"):
            if data is not None:
                all_data.append(data)
    return all_data

def create_df(all_data):
    """Create a datframe with all data colleted"""
    data_properties = pd.DataFrame(all_data)
    data_properties.to_csv("data/immoweb_data.csv", index=False, encoding="utf-8")
    return data_properties

def main():
    start_time = time.time()
    urls = []  
    with open('data/url_list.txt', 'r') as file:
        for line in file:
            line = line.strip()  
            if line: 
                urls.append(line)

    property_data = extracted_multiple_data(urls)

    data_properties_df = create_df(property_data)
    print(data_properties_df)

    end_time = time.time()
    print(f"Time taken to collect URLs: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
