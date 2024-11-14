import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import threading
import time  # Import time module
from concurrent.futures import ThreadPoolExecutor, as_completed


# Function to get cookies for requests
def get_cookies(cookie_url):
    req_cookies = requests.get(cookie_url, headers=headers)
    return req_cookies.cookies

# Extracting data from URLs with concurrency
def extract_data(urls):
    # Create a session to reuse cookies and headers
    session = requests.Session()
    session.headers.update(headers)
    
    # Get cookies only once and set them in the session
    cookies = get_cookies(cookie_url)
    session.cookies.update(cookies)

    extracted_data_list = []

    # Function to get the value or return None if the key doesn't exist
    def get_value(data, *keys):
        for key in keys:
            if isinstance(data, dict) and key in data:
                value = data[key]
                if value is True:
                    data = 1  # If value is True, set data to 1
                elif value is False:
                    data = 0  # If value is False, set data to 2
                else:
                    data = value  # If value is something else, set data to that value
            else:
                return None  # If the key is missing, return None
        return data

    # Function to process a single URL
    def process_url(url):
        try:
            # Use the session to make the request
            response = session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract JSON from the script tag
            scripts = soup.find_all('script', attrs={"type": "text/javascript"})
           
            for script in scripts:
                script_text = script.string
                if script_text and 'window.classified' in script_text:
                    json_str = script_text.strip().replace('window.classified = ', '').rstrip(';')
                    json_data = json.loads(json_str)

                    # Extract required fields from the JSON data
                    return {
                        "Locality": get_value(json_data, "property", "location", "locality"),
                        "Type_of_Property": get_value(json_data, "property", "type"),
                        "Subtype_of_Property": get_value(json_data, "property", "subtype"),
                        "Price": get_value(json_data, "price", "mainValue"),
                        "Type_of_Sale": get_value(json_data, "flags", "isPublicSale"),
                        "Number_of_Rooms": get_value(json_data, "property", "bedroomCount"),
                        "Living_Area": get_value(json_data, "property", "netHabitableSurface"),
                        "Fully_Equipped_Kitchen": get_value(json_data, "property", "kitchen", "type") == "HYPER_EQUIPPED",
                        "Furnished": get_value(json_data, "transaction","sale", "isFurnished"),
                        "Open_Fire": get_value(json_data, "property", "fireplaceCount"),
                        "Terrace": get_value(json_data, "property", "hasTerrace"),
                        "Terrace_Area": get_value(json_data, "property", "terraceSurface"),
                        "Garden": get_value(json_data, "property", "hasGarden"),
                        "Garden_Area": get_value(json_data, "property", "gardenSurface"),
                        "Surface_of_the_Land": get_value(json_data, "property", "land", "surface"),
                        "Number_of_Facades": get_value(json_data, "property", "building", "facadeCount"),
                        "Swimming_Pool": get_value(json_data, "property", "hasSwimmingPool"),
                        "State_of_the_Building": get_value(json_data, "property", "building", "condition"),
                         }
        except Exception as e:
            print(f"Error with URL {url}: {e}")
        return None

    # Start timing data extraction
    start_time = time.time()

    # Use ThreadPoolExecutor for concurrent URL processing
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_url, url) for url in urls]
        for future in as_completed(futures):
            data = future.result()
            if data:
                extracted_data_list.append(data)

    # Convert list of dictionaries to a DataFrame
    dataframe = pd.DataFrame.from_records(extracted_data_list)
    
    # Save the DataFrame to a CSV file
    dataframe.to_csv("classified_extracted_data.csv", index=False, encoding="utf-8")
    
    end_time = time.time()  # End timing data extraction
    print(f"Time taken to extract data: {end_time - start_time:.2f} seconds")

    print(dataframe)

# Start timing the entire program
program_start_time = time.time()

def read_urls(filename):
    url_list = []
    with open(filename, 'r') as urls:
        for url in urls:
            url_list.append(url)
    return url_list

# Run the main function to get all URLs
all_urls = read_urls('properties_txt_urls.txt')

# Pass collected URLs to extract data concurrently
extract_data(all_urls)

# End timing the entire program
program_end_time = time.time()
print(f"Total program execution time: {program_end_time - program_start_time:.2f} seconds")
