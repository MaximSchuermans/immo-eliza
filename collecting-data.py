
import requests
from bs4 import BeautifulSoup
import csv

# Set the URL 
url = "https://www.immoweb.be/fr/recherche/maison-et-appartement/a-vendre"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"
}

#  GET a request and check it 
response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.content)
else:
    print(f"Failed to retrieve content. Status code: {response.status_code}")


# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

#
with open('immoweb_properties.csv', mode='w', newline='', encoding='utf-8') as file:
        immoweb_properties = csv.writer(file)
        # Write the header row
        immoweb_properties.writerow([
            'Locality', 'Type of Property', 'Subtype of Property', 'Price', 
            'Type of Sale', 'Number of Rooms', 'Living Area', 'Fully Equipped Kitchen',
            'Furnished', 'Open Fire', 'Terrace', 'Terrace Area', 'Garden', 'Garden Area',
            'Surface of the Land', 'Surface Area of the Plot of Land', 'Number of Facades',
            'Swimming Pool', 'State of the Building'])
        

 
