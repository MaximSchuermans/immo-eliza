
import requests
from bs4 import BeautifulSoup
import csv

def get_new_cookies(cookie_url):
    # Send a GET request to the given URL to retrieve cookies
    response = requests.get(cookie_url)
    
    # Extract cookies from the response and convert them into a dictionary
    cookies = response.cookies.get_dict()
    
    return cookies

# Set the URL 
url = "https://www.immoweb.be/fr/recherche/maison-et-appartement/a-vendre"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"
}
# Get cookies from a given URL
cookie_url = 'https://www.immoweb.be'
cookies = get_new_cookies(cookie_url)

#  GET a request and check it 
response = requests.get(url, headers=headers, cookies=cookies)

if response.status_code == 200:
    print(response.content)
else:
    print(f"Failed to retrieve content. Status code: {response.status_code}")


# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')
print(soup)


# Save the soup content to a .txt file
with open('page_content.txt', 'w', encoding='utf-8') as file:
    file.write(str(soup))

#
with open('immoweb_properties.csv', mode='w', newline='', encoding='utf-8') as file:
        immoweb_properties = csv.writer(file)
        # Write the header row
        immoweb_properties.writerow([
        'Locality', 'Type_of_Property', 'Subtype_of_Property', 'Price', 
        'Type_of_Sale', 'Number_of_Rooms', 'Living_Area', 'Fully_Equipped_Kitchen',
        'Furnished', 'Open_Fire', 'Terrace', 'Terrace_Area', 'Garden', 'Garden_Area',
        'Surface_of_the_Land', 'Surface_Area_of_the_Plot_of_Land', 'Number_of_Facades',
        'Swimming_Pool', 'State_of_the_Building'
    ])
proprieties = soup.find_all('div', class_='card__informations card--result__informations') 

for propriety  in proprieties :
         
        Locality = propriety.find('span', class_='classified__information--address-row')
        Type_of_Property = propriety.find('span', class_='')
        Subtype_of_Property = propriety.find('span', class_='s')
        Price = propriety.find('span', class_='sr-only')
        Type_of_Sale = propriety.find('span', class_='')
        Number_of_Rooms = propriety.find('span', class_='')
        Living_Area = propriety.find('span', class_='')
        Fully_Equipped_Kitchen = propriety.find('span', class_='')
        Furnished = propriety.find('span', class_='')
        Open_Fire = propriety.find('span', class_='')
        Terrace = propriety.find('span', class_='')
        Terrace_Area = propriety.find('span', class_='')
        Garden = propriety.find('span', class_='')
        Garden_Area = propriety.find('span', class_='')
        Surface_of_the_Land = propriety.find('span', class_='')
        Surface_Area_of_the_Plot_of_Land = propriety.find('span', class_='')
        Number_of_Facades = propriety.find('span', class_='')
        Swimming_Pool = propriety.find('span', class_='')
        State_of_the_Building = propriety.find('span', class_='')
