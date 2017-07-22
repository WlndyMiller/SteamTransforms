#!/usr/bin/python3

import sys
import math
import dryscrape
from bs4 import BeautifulSoup
from MaltegoTransform import *

users_per_search_page = 20


def extract_user_profile_url(search_result):
    soup = BeautifulSoup(str(search_result), 'lxml')
    url =  soup.select_one('a.searchPersonaName').get('href')
    return url

    #print(soup.prettify())

def scrape_search(username, users_to_search):
    """Searches for passed username for provided number of pages and returns list of DOMs (one for each page)"""

    pages_to_search = math.ceil(users_to_search / users_per_search_page)
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
    # Take screenshot for debugging
    return search_results

def extract_user_html(response):
    # print(searchRow)
    users = []
    soup = BeautifulSoup(response, 'lxml')
    #for user in soup.find_all("div", class_="search_row"):
    for user in soup.select('div.search_row'):
        users.append(str(user))

    return users

def main():
    if len(sys.argv) != 3:
        sys.exit("Username and number of users to search required\nSteamSearchScrape.py \"Sample User Name\" 3")
    
    username = sys.argv[1]
    try:
        no_of_users = int(sys.argv[2])
    except ValueError:
        no_of_users = 20
    
    responses = scrape_search(username, no_of_users)

    users = []
    user_urls = []
    for resp in responses:
        users.extend(extract_user_html(resp))   
        # Trim list to number of users specified
    users = users[:no_of_users]
    for user in users:
        user_urls.append(extract_user_profile_url(user))
    for url in user_urls:
        print(url)
    m = MaltegoTransform()
    print(len(users))

if __name__ == "__main__":
    main()
    