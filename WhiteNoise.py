#!/usr/bin/python3
import random
import re
import subprocess
import sys
from time import sleep
import requests
from bs4 import BeautifulSoup
# ALEXA_SOURCE is the webpage to pull links from 
ALEXA_SOURCE = "https://www.alexa.com/topsites/category/Top/Science"

# ALEXASKIP = list of strings/URL's to skip when assembling list of links
ALEXASKIP = ["https://www.alexa.com/siteinfo", "/siteinfo"]

# browser to launch
BROWSERNAME = "chromium"

# DELAY = seconds to wait before killing browser process
DELAY = 240

# SITEINFO = indicates desired links to choose from
SITEINFO = "siteinfo"

# TIMEOUT = URL fetch will stop trying after this many seconds
TIMEOUT = 30

site = ALEXA_SOURCE
links = []

print("Chose Random URL capture URL: {}".format(site))

try:
    html = requests.get(site, timeout=TIMEOUT).text
except:
    print("Can't fetch {}".format(site))
    sys.exit(1)

try:
    soup = BeautifulSoup(html, features="html.parser")
except:
    print("Can't parse HTML from {}".format(site))
    sys.exit(1)

for line in soup.find_all("a"): #find all anchor tags
    link = line.get("href") #find href's
    if re.search(SITEINFO, str(link)) is not None and link not in ALEXASKIP:
        links.append(link) #build list of link candidates

linknum = len(links)

if linknum > 2: # if < 2, something has gone wrong, don't try to launch browser
    target = random.randint(0, linknum - 1)
    print("Chose Random Link no {}".format(target))
    final = re.sub("/siteinfo/", "http://www.", links[target]) #rewrite link
    print("Launching URL and closing {} seconds later...".format(DELAY))
    browser = subprocess.Popen(
        [BROWSERNAME, final],
        stdout=subprocess.DEVNULL, #don't clutter screen w/ output
        stderr=subprocess.DEVNULL, #don't clutter screen w/ errors
    )
    sleep((DELAY) #wait while we load/pretend to read the page
    print("Kill the process")
    browser.terminate()
