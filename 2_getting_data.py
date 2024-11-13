import requests 
from bs4 import BeautifulSoup 
from requests import Session
import json 


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

            #with open("classified_data.json", "w") as file: 
                #json.dump(json_data, file, ensure_ascii=False, indent=4)
                #  
            return json_data
        except:
            pass
            
def extracted_dat(url, json_data):
    property = {   } #initial dictionary




    property["URL"] = url
    property["ID"] = json_data["id"]
    property["Locality"] = json_data["property"]["location"]["province"]
    property["Type of property"] = json_data 
    property["Subtype of property"] = json_data 
    property["Type of sale"] = json_data 
    property["Number of rooms"] = json_data 
    property["Living Area"] = json_data 
    property["Fully equipped kitchen"] = json_data 
    property["Furnished"] = json_data 
    property["Open fired"] = json_data 
    property["Terrace"] = json_data 
    property["Land surface"] = json_data 
    property["Plot of land surface"] = json_data  
    property["Number of facades"] = json_data  
    property["Swimming pool"] = json_data  
    property["State of the building"] = json_data  












# Call the function to test
url = "https://www.immoweb.be/en/classified/apartment/for-sale/wommelgem/2160/20313380"
get_script(url)

