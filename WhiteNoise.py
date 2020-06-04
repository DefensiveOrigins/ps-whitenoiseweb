#!/usr/bin/env/python3
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

links = []

print("Chose Random URL capture URL: {}".format(ALEXA_SOURCE))

try:
    html = requests.get(ALEXA_SOURCE, timeout=TIMEOUT).text
except:
    print("Can't fetch {}".format(ALEXA_SOURCE))
    sys.exit(1)

try:
    soup = BeautifulSoup(html, features="html.parser")
except:
    print("Can't parse HTML from {}".format(ALEXA_SOURCE))

for line in soup.find_all("a"):  # find all anchor tags
    link = line.get("href")  # find href's
    if re.search(SITEINFO, str(link)) is not None and link not in ALEXASKIP:
        links.append(link)  # build list of link candidates

if len(links) > 2:  # if < 2, something has gone wrong, don't try to launch browser
    target = random.randint(0, len(links) - 1)
    print("Chose Random Link no {}".format(target))
    final = re.sub("/siteinfo/", "http://www.", links[target])  # rewrite link
    random.seed()  # initialize RNG
    delay = (
        DELAY * 2 * random.random()
    )  # wait random # of seconds approx equal to DELAY
    print("Launching URL and closing {} seconds later...".format(delay))
    browser = subprocess.Popen(  # launch browser
        [BROWSERNAME, final],
        stdout=subprocess.DEVNULL,  # don't clutter screen w/ output
        stderr=subprocess.DEVNULL,  # don't clutter screen w/ errors
    )
    sleep(delay)
    print("Kill the process")
    browser.terminate()
