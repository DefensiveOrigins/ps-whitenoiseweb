#!/usr/bin/python3
import random
import re
import subprocess
import sys
from time import sleep
import requests
from bs4 import BeautifulSoup

ALEXA_SOURCE = "https://www.alexa.com/topsites/category/Top/Science"
ALEXASKIP = ["https://www.alexa.com/siteinfo", "/siteinfo"]
BROWSERNAME = "chromium"
DELAY = 240
SITEINFO = "siteinfo"
TIMEOUT = 30

site = ALEXA_SOURCE

links = []

print("Chose Random URL capture URL: {}".format(site))

try:
    html = requests.get(site, timeout=TIMEOUT).text
except:
    print("Can't seem to fetch {}".format(site))
    sys.exit(1)

try:
    soup = BeautifulSoup(html, features="html.parser")
except:
    print("Can't seem to parse HTML from {}".format(site))
    sys.exit(1)

for line in soup.find_all("a"):
    link = line.get("href")
    if re.search(SITEINFO, str(link)) is not None and link not in ALEXASKIP:
        links.append(link)

linknum = len(links)

if linknum > 2:
    target = random.randint(0, linknum - 1)
    print("Chose Random Link no {}".format(target))
    final = re.sub("/siteinfo/", "http://www.", links[target])
    print("Launching URL and closing {} seconds later...".format(DELAY))
    browser = subprocess.Popen(
        [BROWSERNAME, "--ssb", final],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    sleep(DELAY)
    print("Kill the process")
    browser.terminate()
