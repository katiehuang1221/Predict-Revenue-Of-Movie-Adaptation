import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import time, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

chromedriver = "/Applications/chromedriver" # path to the chromedriver executable
os.environ["webdriver.chrome.driver"] = chromedriver

# Open automated Chrome with fictionDB webpage
driver = webdriver.Chrome(chromedriver)
driver.get("https://www.fictiondb.com/search/search.htm")

def search(author):
    author_dict={}

    driver.get("https://www.fictiondb.com/search/search.htm")
    search_bar = driver.find_element_by_xpath("//input[@name='author'][@type='text']")
    search_bar.clear()
    search_bar.send_keys(author)
    search_bar.send_keys(Keys.RETURN)
    
    # Click on the author link
    try:

        author_r = ", ".join(author.split()[::-1])
        elem = driver.find_element_by_link_text(author_r)
        elem.click()
    except:
        print("can't find author")
        pass

    try:
        publication = driver.find_elements_by_xpath("//a[@itemprop='datePublished']")
        dates = [s.text.split('-') for s in publication]
        years = [int(y[-1]) for y in dates]
    except:
        print("can't find publication")
        pass
    
    author_dict[author] = years

    return author_dict


def find_years():
    # Find publications and create list of year
    publication = driver.find_elements_by_xpath("//a[@itemprop='datePublished']")
    dates = [s.text.split('-') for s in publication]
    years = [int(y[-1]) for y in dates]

    return years


# Added sleep time in between actions
def search(author):
    author_dict={}

    driver.get("https://www.fictiondb.com/search/search.htm")
    search_bar = driver.find_element_by_xpath("//input[@name='author'][@type='text']")
    search_bar.clear()
    search_bar.send_keys(author)
    search_bar.send_keys(Keys.RETURN)
    
    # Rest for 3 seconds
    time.sleep(3)
    # Press enter in case there's pop up ad
    actions = ActionChains(driver)
    actions.send_keys(Keys.RETURN)
    actions.perform()
    
    # Search for publications first
    # If error (multiple authors page), pass
    try:
        time.sleep(1)
        actions = ActionChains(driver)
        actions.send_keys(Keys.RETURN)
        actions.perform()
        time.sleep(3)
        publication = driver.find_elements_by_xpath("//a[@itemprop='datePublished']")
        dates = [(s.text+'0').split('-') for s in publication]
        years = [int(y[-1])//10 for y in dates if int(y[-1])//10 != 0]
    except:
        print("multiple search results of author")
        pass    
    
    # Click on the author link
    try:
        author_r = ", ".join(author.split()[::-1])
        elem = driver.find_element_by_link_text(author_r)
        elem.click()
    except:
        print("can't find author")
        pass

    try:
        time.sleep(1)
        actions = ActionChains(driver)
        actions.send_keys(Keys.RETURN)
        actions.perform()
        time.sleep(2)
        publication = driver.find_elements_by_xpath("//a[@itemprop='datePublished']")
        dates = [(s.text+'0').split('-') for s in publication]
        years = [int(y[-1])//10 for y in dates if int(y[-1])//10 != 0]
    except:
        print("can't find publication")
        pass
    
    author_dict[author] = years

    return author_dict





def google(keyword,date):
    driver.get("https://www.google.com")
    search_bar = driver.find_element_by_xpath("//input[@name='q'][@type='text']")
    search_bar.clear()
    search_bar.send_keys(keyword + ' before:' + date)
#     print(keyword + ' before:' + date)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(2)
    
    
    # Set default value of result
    result = np.nan
    # Find search stats before the given date
    try:
        for element in driver.find_elements_by_xpath("//div[@id='result-stats']"):
            result = (int(element.text.split()[1].replace(',','')))
    except:
        pass
#     print(result)
    return result

# Added sleep time in between actions
def book_google(book,author,date):
    
    title = book
    date = date
    
    book_dict={}
    
    headers = ["title","release_date","title_search","search_fiction_book","book_popularity",\
               "author_search","search_fiction_author","author_popularity"]

    book_result = google(book + ' ' + author, date)
    novel_result = google("novel recommendation", date)
    book_pop = round(book_result / novel_result,2)
    
    author_result = google(author,date)
    authors_result = google("fiction author", date)
    author_pop = round(author_result / authors_result,4)
    
    book_dict = dict(zip(headers,[title,date,book_result,novel_result,book_pop,author_result,authors_result,author_pop]))
    

    return book_dict


def book_google2(book,author,date,genre):
    
    title = book
    
    book_dict={}
    
    headers = ["title","release_date","genre","title_search","search_fiction_book",\
               "author_search","search_fiction_author","book_popularity","author_popularity"]

    book_result = google(book + ' ' + author, date)
    novel_result = google("novel " + ' '.join(genre), date)
    book_pop = round(book_result / novel_result,2)
    
    author_result = google(author,date)
    authors_result = google("fiction author", date)
    author_pop = round(author_result / authors_result,4)
    
    book_dict = dict(zip(headers,[title,date,genre, book_result,novel_result,author_result,authors_result,book_pop,author_pop]))
    

    return book_dict