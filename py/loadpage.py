from bs4 import BeautifulSoup
import requests
from IPython.core.display import display, HTML

def get_soup(url):
    response = requests.get(url)
    page = response.text
    soup = BeautifulSoup(page, "lxml")
    return soup
