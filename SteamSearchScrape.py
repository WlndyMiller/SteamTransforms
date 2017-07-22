#!/usr/bin/python3

import sys
import dryscrape
from bs4 import BeautifulSoup


def main():
    if len(sys.argv) != 3:
        sys.exit("Username and number of pages to search required\nSteamSearchScrape.py \"Sample User Name\" 3")
    session = dryscrape.Session(base_url = 'https://steamcommunity.com')
    session.visit('/search/users/#text=' + sys.argv[1])
    # Wait for search results to load
    session.wait_for(lambda: session.at_css("div.search_row"))
    # Take screenshot for debugging
    session.render('steam.png')
    response = session.body()
    soup = BeautifulSoup(response)

    for user in soup.find_all("div", class_="search_row"):
        print(user)

if __name__ == "__main__":
    main()
    