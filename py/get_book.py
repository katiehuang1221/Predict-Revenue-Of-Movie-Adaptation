import numpy as np
# Define function to get book data from the book page
# Try fixing missing value problem
# Try fixing first published year problem (if there's only first published year)

def get_book_data(book):
    """
    Input: book = soup in book_soup_list
    Output: book_dict
    """
    
    headers=['book_title', 'author', 'rating_value', 'rating_count', 'review_count', 'page', 'year']
    
    # Assign default value
    title, author, rating_value, rating_count, review_count, page, year = \
    np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan
    # Find book title, author, rating_value, rating_count, review_count, page
    title = book.find('h1').text.strip('\n').lstrip()
    author = book.find('a', class_="authorName").text
    rating_value = float(book.find('span', attrs={'itemprop':'ratingValue'}).text.strip('\n').lstrip())
    rating_count = int(book.find('meta', attrs={'itemprop':'ratingCount'}).get('content'))
    review_count = int(book.find('meta', attrs={'itemprop':'reviewCount'}).get('content'))
    if book.find('span', attrs={'itemprop':'numberOfPages'}) is not None:
        page = int(book.find('span', attrs={'itemprop':'numberOfPages'}).text.strip(' pages'))

    # Find year first published
    for div in book.find_all('div', attrs={'id':'details'}):
        for row in div.find_all('nobr', class_='greyText'):
            year = row.text
            year = int(''.join(i for i in year if i.isdigit())[-4:])
            
    
    
    # Find earliest year
    if div.find_all('div', class_='row') != []:
        string = div.find_all('div', class_='row')[-1].text
        str_clean = string.replace('(',' ').replace(')',' ').split()
        year_list = [int(s) for s in str_clean if s.isdigit()]
        if year_list != []:
            year = min(year_list)
    
    
    book_dict = dict(zip(headers, [title,
                                   author,
                                   rating_value,
                                   rating_count,
                                   review_count,
                                   page,
                                   year]))
    
    return book_dict




# Use selenium to search book from movie_title

from bs4 import BeautifulSoup
import requests
import time, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

chromedriver = "/Applications/chromedriver" # path to the chromedriver executable
os.environ["webdriver.chrome.driver"] = chromedriver

driver = webdriver.Chrome(chromedriver)
driver.get("https://www.goodreads.com/")

def search_goodreads(movie):
    """
    input(movie) = movie_title
    return details for individul book from the first search result
    """

    driver.get("https://www.goodreads.com/")
    
    # Set book default
    book = {'book_title': np.nan,
 'author': np.nan,
 'rating_value': np.nan,
 'rating_count': np.nan,
 'review_count': np.nan,
 'page': np.nan,
 'year': np.nan}

    # Search movie title
    search_bar = driver.find_element_by_xpath("//input[@name='query'][@type='text']")
    search_bar.clear()
    search_bar.send_keys(movie)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(5)

    actions = ActionChains(driver)
    actions.send_keys(Keys.RETURN)
    actions.perform()
    # Click on the first result
    try:
        elem = driver.find_element_by_class_name("bookTitle").click()
        # Make soup and get data
        book_soup = BeautifulSoup(driver.page_source, "lxml")
        book = get_bookdata(book_soup)
    except:
        pass
    

    return book