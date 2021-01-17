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