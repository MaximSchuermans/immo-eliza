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

def extracted_mutiple_data(urls):
    all_data = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []  
        for url in urls:
            future = executor.submit(get_script, url)  
            futures.append(future) 

        for future, url in zip(futures, urls):
            json_data = future.result()
            if json_data:
                property_data = extracted_data(url, json_data)
                all_data.append(property_data)
            else:
                pass
    
    return all_data

def create_df(all_data):
    data_properties = pd.DataFrame(all_data)
    data_properties.to_csv("properties_data.csv", index=False, encoding="utf-8")


# Call the function to test
urls = ["https://www.immoweb.be/en/classified/house/for-sale/deurne/2100/20316323",
        "https://www.immoweb.be/en/classified/house/for-sale/ans/4430/20305771",
        "https://www.immoweb.be/en/classified/house/for-sale/ans/4430/20305771",
        "https://www.immoweb.be/en/classified/apartment/for-sale/ixelles/1050/20313791",
        "https://www.immoweb.be/en/classified/apartment/for-sale/wommelgem/2160/20313380",
        'https://www.immoweb.be/en/classified/new-real-estate-project-apartments/for-sale/anderlecht/1070/20313048',
        'https://www.immoweb.be/en/classified/new-real-estate-project-apartments/for-sale/gent/9000/20314083',
        'https://www.immoweb.be/en/classified/apartment/for-sale/boom/2850/20310616',
        "https://www.immoweb.be/en/classified/apartment/for-sale/anderlecht/1070/20313783", 
        "https://www.immoweb.be/en/classified/bungalow/for-sale/zelzate/9060/20309509", 
        "https://www.immoweb.be/en/classified/exceptional-property/for-sale/sint-katelijne-waver/2860/20309293", 
        "https://www.immoweb.be/en/classified/apartment/for-sale/knocke-heyst/8301/20207350",
        "https://www.immoweb.be/en/classified/ground-floor/for-sale/spa/4900/20181510",
        "https://www.immoweb.be/en/classified/apartment/for-sale/cadzand/4506%20JH/20118396",
        "https://www.immoweb.be/en/classified/flat-studio/for-sale/de-haan/8420/20255430",
        "https://www.immoweb.be/en/classified/house/for-sale/verviers/4800/20128649",
        "https://www.immoweb.be/en/classified/house/for-sale/waimes/4950/20281071",
        "https://www.immoweb.be/en/classified/house/for-sale/flemalle/4400/20316175",
        "https://www.immoweb.be/en/classified/house/for-sale/flemalle/4400/20316175",
        "https://www.immoweb.be/en/classified/mixed-use-building/for-sale/pittem/8740/20308501",
        "https://www.immoweb.be/en/classified/duplex/for-sale/woluwe-saint-lambert/1200/20280691"
        
        ]

property_data = extracted_mutiple_data(urls)
data_properties_df = create_df(property_data)
print(data_properties_df)