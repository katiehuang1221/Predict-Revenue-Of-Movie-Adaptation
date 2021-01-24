"""
Functions for webscraping:
1. get_soup(url)

"""

from bs4 import BeautifulSoup
import requests

import pandas as pd
import numpy as np


def get_soup(url):
    response = requests.get(url)
    page = response.text
    soup = BeautifulSoup(page, "lxml")
    return soup

