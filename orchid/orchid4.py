#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 15:33:17 2019

@author: khlarkin
"""

# Import libraries
import os
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import lxml.html
import requests
import re
import operator
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Get URL for Orchid ID page you want to scrape
orchid_id = '0000-0001-6023-9062'  # Michael Holick
#orchid_id = '0000-0003-4076-2336'  # Emelia Benjamin
#orchid_id = '0000-0001-9890-0653'  # random

orchid_url = 'https://orcid.org/' + orchid_id + '/print'

# To launch chrome browser using ChromeDriver you need to pass executable chromedriver location with executable itself into executable_path.
# Code based  on source: https://stackoverflow.com/questions/39428042/use-selenium-with-chromedriver-on-mac
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")

# Load in your browser (I use chrome)
browser = webdriver.Chrome(executable_path=DRIVER_BIN)

# Get the url with Selenium
browser.get(orchid_url)

# An explicit wait is a code you define to wait for a certain condition to occur before proceeding further in the code.
# Documentation: https://selenium-python.readthedocs.io/waits.html
element = WebDriverWait(browser, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="body-work-list"]/li[last()]')))

# Get the innerhtml from the rendered page
innerHTML = browser.execute_script("return document.body.innerHTML")

# Use lxml to parse the page
tree = lxml.html.fromstring(innerHTML)

# Print tree elements to make sure that the scrape worked
for elem in tree:
    print(lxml.html.tostring(elem))

# Print scraped html from page
with open('scraped_page.txt', 'wb') as f:
    for elem in tree:
        f.write(lxml.html.tostring(elem))

# Get elements with xpath
test_links = tree.xpath('//a/text()')
person = tree.xpath('//*[@id="main"]/div/div[1]/div/print-id-banner-ng2/div/h2/text()')[0].strip()
pmid_urls = tree.xpath('//a[contains(@href,"pubmed")]/@href')
# Remove duplicate urls
pmid_urls = list(set(pmid_urls))

# Create list of pmids
pmids = []

for i in pmid_urls:
    pmids.append(i.strip('https://www.ncbi.nlm.nih.gov/pubmed/'))

# Count pmids in list
pmid_counter = 0

for j in pmids:
    pmid_counter += 1

# Print results
print('Name: ' + person)
print('URL for Orchid ID page: ' + orchid_url.strip('/print'))
print('Number of PMIDs found: ', pmid_counter)
# print('List of PMIDS: ')
# print(pmids)

# Close the browser
browser.quit()
