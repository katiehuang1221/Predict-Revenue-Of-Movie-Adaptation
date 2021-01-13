from bs4 import BeautifulSoup
import requests
from IPython.core.display import display, HTML

def loadpage(file_html):
    with open('../'+ file_html +') as page:
        test_html = page.read()
    soup = BeautifulSoup(test_html,'lxml')
    return soup