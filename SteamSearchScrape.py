#!/usr/bin/python3

import sys
import dryscrape
from bs4 import BeautifulSoup

def parse_search_result(search_result):
    soup = BeautifulSoup(search_result, 'lxml')
    url = soup.select_one('a.searchPersonaName').get('href')
    print("\nURL:" + url)

    #print(soup.prettify())

def scrape_search(username, pages):
    """Searches for passed username for provided number of pages and returns list of DOMs (one for each page)"""
    try:
        pages_to_search = int(pages)
    except ValueError:
        pages_to_search = 1
    search_results = []
    session = dryscrape.Session(base_url = 'https://steamcommunity.com')
    for i in range(1, pages_to_search+1):
        if i == 1:
            session.visit('/search/users/#text=' + username)
        else:
            session.visit('/search/users/#page=' + str(i) + '&text=' + username)
        
    # Wait for search results to load
        session.wait_for(lambda: session.at_css("div.search_row"))
        search_results.append(session.body())
        #session.render('steam'+ str(i) +'.png')
        session.reset()
    # Take screenshot for debugging
    return search_results

def parse_search(response):
    # print(searchRow)
    usernames = []
    soup = BeautifulSoup(response, 'lxml')
    #for user in soup.find_all("div", class_="search_row"):
    for user in soup.select('div.search_row'):
        print("\n\n=====================\n\n")
        parse_search_result(str(user))

def main():
    if len(sys.argv) != 3:
        sys.exit("Username and number of pages to search required\nSteamSearchScrape.py \"Sample User Name\" 3")
    
    responses = scrape_search(sys.argv[1], sys.argv[2])
    for resp in responses:
        parse_search(resp)
    print(len(responses))
if __name__ == "__main__":
    main()
    