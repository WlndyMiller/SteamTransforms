#!/usr/bin/python3

import sys
import math
import dryscrape
from bs4 import BeautifulSoup
from MaltegoTransform import *

USERS_PER_SEARCH_PAGE = 20
MALTEGO = MaltegoTransform()

def extract_user_profile_url(search_result):
    '''Extracts profile URL from individual search result DOM'''
    soup = BeautifulSoup(str(search_result), 'lxml')
    url = soup.select_one('a.searchPersonaName').get('href')
    return url

def extract_user_profile_img_url(search_result):
    '''Extracts profile image url from search result'''
    soup = BeautifulSoup(str(search_result), 'lxml')
    url = soup.select_one('img').get('src')
    return url

def extract_user_html(response):
    '''Extracts each user result from page DOM'''
    users = []
    soup = BeautifulSoup(response, 'lxml')
    for user in soup.select('div.search_row'):
        users.append(str(user))

    return users

def scrape_search(username, users_to_search):
    """Searches for passed username for pages and returns list of DOMs"""

    pages_to_search = math.ceil(users_to_search / USERS_PER_SEARCH_PAGE)
    search_results = []
    session = dryscrape.Session(base_url = 'https://steamcommunity.com')
    for i in range(1, pages_to_search+1):
        if i == users_to_search + 1:
            break
        if i == 1:
            session.visit('/search/users/#text=' + username)
        else:
            session.visit('/search/users/#page=' + str(i) + '&text=' + username)
        
    # Wait for search results to load
        session.wait_for(lambda: session.at_css("div.search_row"))
        search_results.append(session.body())
        # Reset session to load new page
        session.reset()
    return search_results

def scrape_profile(url):
    ''' Returns DOM of profile URL'''

    session = dryscrape.Session()
    session.visit(url)
    return session.body()

def output_to_maltego(url, img_url):
    ''' Adds maltego entities from url '''

    split_url = url.split('/')
    profile_id = split_url[-1]
    web_entity = MALTEGO.addEntity("WindyMiller.SteamAccount", url)
    web_entity.setType("WindyMiller.SteamAccount")
    web_entity.addAdditionalFields("url", "URL", True, url)
    web_entity.addAdditionalFields("title", "Title", True, url)
    web_entity.addAdditionalFields("short-title", "Short Title", True, profile_id)
    web_entity.setIconURL(img_url)

def main():
    if len(sys.argv) <= 2:
        sys.exit("Username and number of users to search required\nSteamSearchScrape.py \"Sample User Name\" 3")
    username = sys.argv[1]
    try:
        no_of_users = int(sys.argv[2])
    except ValueError:
        # Defaults to 12 for benefit of Maltego community users (me) as it seems to take last 12 results
        no_of_users = 12
    responses = scrape_search(username, no_of_users)
    users = []
    user_urls = []
    user_img_urls = []
    for resp in responses:
        users.extend(extract_user_html(resp))
    # Trim list to number of users specified
    users = users[:no_of_users]
    for user in users:
        user_urls.append(extract_user_profile_url(user))
        user_img_urls.append(extract_user_profile_img_url(user))
    if len(user_urls) == 0:
        MALTEGO.addUIMessage("No profiles found for " + username)
    else:
        for url, img_url in zip(user_urls, user_img_urls):
            output_to_maltego(url, img_url)
    MALTEGO.returnOutput()
    
if __name__ == "__main__":
    main()
    