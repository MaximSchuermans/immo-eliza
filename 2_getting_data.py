import requests 
from bs4 import BeautifulSoup 
from requests import Session
import json 
from concurrent.futures import ThreadPoolExecutor
import pandas as pd


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

cookie_url = "https://www.immoweb.be"
def get_cookies():
    req_cookies = requests.get(cookie_url, headers=headers)
    cookies = req_cookies.cookies
    return cookies

def get_script(url):
     with requests.Session() as session:
        response = session.get(url, cookies=get_cookies(), headers=headers)
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
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return None  # If the key is not found, return None
    return data

def extracted_data(url, json_data):
    extracted_data = {
                    "Price": get_value(json_data, "price", "mainValue"),
                    "Type_of_Sale": get_value(json_data, "flags", "isPublicSale"),
                    "Locality": get_value(json_data, "property", "location", "locality"),
                    "Type_of_Property": get_value(json_data, "property", "type"),
                    "Subtype_of_Property": get_value(json_data, "property", "subtype"),
                    "Number_of_Rooms": get_value(json_data, "property", "bedroomCount"),
                    "Living_Area": get_value(json_data, "property", "netHabitableSurface"),
                    "Fully_Equipped_Kitchen": get_value(json_data, "property", "kitchen", "type") == "HYPER_EQUIPPED",
                    "Furnished": get_value(json_data, "property", "isFurnished"),
                    "Open_Fire": get_value(json_data, "property", "hasOpenFire"),
                    "Terrace": get_value(json_data, "property", "hasTerrace"),
                    "Number_of_Facades": get_value(json_data, "property", "building", "facadeCount"),
                    "Swimming_Pool": get_value(json_data, "property", "hasSwimmingPool"),
                    #"Surface_of_the_Land": get_value(json_data, "property", "land", "surface"),
                    "State_of_the_Building": get_value(json_data, "property", "building", "condition"),
                }

    return extracted_data

def extracted_mutiple_data(urls):
    all_data = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_script, url) for url in urls]

        # Process each future as it completes
        for future, url in zip(futures, urls):
            json_data = future.result()
            if json_data:
                property_data = extracted_data(url, json_data)
                all_data.append(property_data)
            else:
                print(f"No data retrieved for {url}")

    return all_data

def get_dataframe(all_data):
    data_properties = pd.DataFrame.from_records(all_data)

    with open("classified_extracted_data.json", "w", encoding="utf-8") as file:
        json.dump(data_properties, file, ensure_ascii=False, indent=4)
        

def get_dataframe(all_data):
    # Convert the list of dictionaries into a pandas DataFrame
    data_properties = pd.DataFrame(all_data)

    # Save the DataFrame to a JSON file
    with open("classified_extracted_data.json", "w", encoding="utf-8") as file:
        json.dump(data_properties.to_dict(orient="records"), file, ensure_ascii=False, indent=4)
    
    return data_properties





# Call the function to test

urls = [
    "https://www.immoweb.be/en/classified/apartment/for-sale/ixelles/1050/20313791",
    "https://www.immoweb.be/en/classified/apartment/for-sale/wommelgem/2160/20313380",
    'https://www.immoweb.be/en/classified/new-real-estate-project-apartments/for-sale/anderlecht/1070/20313048',
    'https://www.immoweb.be/en/classified/new-real-estate-project-apartments/for-sale/gent/9000/20314083',
    'https://www.immoweb.be/en/classified/new-real-estate-project-apartments/for-sale/mons/7000/20314330',
]

property_data = extracted_mutiple_data(urls)
print(property_data)
