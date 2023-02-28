import requests
from bs4 import BeautifulSoup

url = 'https://basketball.realgm.com/international/league/1/Euroleague/team/142/ALBA-Berlin/schedule'
req = requests.get(url)
soup = BeautifulSoup(req, 'html.parser')
