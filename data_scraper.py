from selenium import webdriver
import requests 
from bs4 import BeautifulSoup 
from requests import Session
import json 
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def get_script(url):
    driver = webdriver.Chrome()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

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
    for key in keys:
        if isinstance(data, dict) and key in data:
            value = data[key]

            if value is True:
                data = 1  # If value is True, set data to 1
            elif value is False:
                data = 2  # If value is False, set data to 2
            else:
                try:
                    data = int(value)  # Try to convert value to an integer
                except:
                    data = value  # If conversion fails, return the original value
        else:
            return None  # Return None if key is missing
    return data

def extracted_data(url, json_data):
    extracted_data = { }

    extracted_data["Price"] = get_value(json_data, "price", "mainValue")
    extracted_data["Type_of_Sale"] = get_value(json_data, "flags", "isPublicSale")
    extracted_data["Locality"] = get_value(json_data, "property", "location", "locality")
    extracted_data["Type_of_Property"] = get_value(json_data, "property", "type")
    extracted_data["Subtype_of_Property"] = get_value(json_data, "property", "subtype")
    extracted_data["Number_of_Rooms"] = get_value(json_data, "property", "bedroomCount")
    extracted_data["Living_Area"] = get_value(json_data, "property", "netHabitableSurface")
    extracted_data["Fully_Equipped_Kitchen"] = get_value(json_data, "property", "kitchen", "type") == "HYPER_EQUIPPED"
    extracted_data["Furnished"] = get_value(json_data, "transaction","sale", "isFurnished")
    extracted_data["Open_fire"] = get_value(json_data, "property", "fireplaceCount"),
    extracted_data["Terrace"] = get_value(json_data, "property", "hasTerrace")
    extracted_data["Terrace_Area"] = get_value(json_data, "property", "terrace", "surface"),
    extracted_data["Garden"] = get_value(json_data, "property", "hasGarden"),
    extracted_data["Garden_Area"] = get_value(json_data, "property", "garden", "surface"),
    extracted_data["Surface_of_the_Land"] = get_value(json_data, "property", "land", "surface")
    extracted_data["Number_of_Facades"] = get_value(json_data, "property", "building", "facadeCount"),
    extracted_data["Swimming_Pool"] = get_value(json_data, "property", "hasSwimmingPool")
    extracted_data["State_of_the_Building"] = get_value(json_data, "property", "building", "condition")

    return extracted_data 


def extract_data_for_url(url):
    """Extract data for a single UR."""
    json_data = get_script(url)
    if json_data:
        return extracted_data(url, json_data)
    return None

def extracted_multiple_data(urls):
    """Extract data from multiple URLs concurrently."""
    all_data = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(extract_data_for_url, urls)

        all_data = []
        for data in results:
            if data is not None:
                all_data.append(data)

    return all_data

def create_df(all_data):
    data_properties = pd.DataFrame(all_data)
    data_properties.to_csv("properties_data.csv", index=False, encoding="utf-8")
    return data_properties

def main ():
    urls = []  
    with open('url_links', 'r') as file:
        for line in file:
            line = line.strip()  
            if line: 
                urls.append(line)

    property_data = extracted_multiple_data(urls)

    data_properties_df = create_df(property_data)
    print(data_properties_df)

if __name__ == "__main__":
    main()
