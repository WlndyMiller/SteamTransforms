#!/usr/bin/python3

import sys
import math
import re
import dryscrape
from bs4 import BeautifulSoup
from MaltegoTransform import *

MALTEGO = MaltegoTransform()

def output_to_maltego(location_line):

    # Split location out
    location_line_elements = re.split(r'\s{2,}', location_line)
    location_line_elements = list(filter(None, location_line_elements))
    location = location_line_elements[-1]

    location_entity = MALTEGO.addEntity("maltego.Location", location)
    location_entity.setType("maltego.Location")

def scrape_profile(url):
    ''' Returns DOM of profile URL'''

    session = dryscrape.Session()
    session.visit(url)
    return session.body()

def extract_location_line(response):
    soup = BeautifulSoup(response, 'lxml')
    try:
        location_line = soup.select_one('div.header_real_name').getText()
        return location_line
    except AttributeError:
        MALTEGO.addUIMessage("No public profile")

def output():
    MALTEGO.returnOutput()

def main():
    url = str(sys.argv[1])
    response = scrape_profile(url)
    location = extract_location_line(response)
    if location:
        output_to_maltego(location)
    output()


if __name__ == "__main__":
    main()