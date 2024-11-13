import requests 
from bs4 import BeautifulSoup 
#import re 
#import json 


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

cookie_url = "https://www.immoweb.be"
def get_cookies(cookie_url):
    req_cookies = requests.get(cookie_url, headers=headers)
    cookies = req_cookies.cookies
    return cookies

url = "https://www.immoweb.be/en/classified/apartment/for-sale/wommelgem/2160/20313380"
response = requests.get(url, cookies=get_cookies(cookie_url), headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

content = soup.find_all('script', attrs={"type" :"text/javascript"})

