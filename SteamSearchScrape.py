#!/usr/bin/python3

import sys
import dryscrape
from bs4 import BeautifulSoup

def parse_search_result(searchResult):
    soup = BeautifulSoup(searchResult, 'lxml')
    url = soup.select_one('a.searchPersonaName').get('href')
    print("\nURL:" + url)

    print(soup.prettify())

def scrape_search(username):
    session = dryscrape.Session(base_url = 'https://steamcommunity.com')
    session.visit('/search/users/#text=' + username)
    # Wait for search results to load
    session.wait_for(lambda: session.at_css("div.search_row"))
    # Take screenshot for debugging
    session.render('steam.png')
    return session.body()

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
    
    response = scrape_search(sys.argv[1])
    parse_search(response)

if __name__ == "__main__":
    main()
    