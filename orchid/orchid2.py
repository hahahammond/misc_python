#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 09:05:10 2019

@author: larkink
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

# Get URL for Orchid ID page you want to scrape
orchid_id = '0000-0001-6023-9062'
orchid_url = 'https://orcid.org/'+ orchid_id + '/print'

# To launch chrome browser using ChromeDriver you need to pass executable chromedriver location with executable itself into executable_path.
# Code based  on source: https://stackoverflow.com/questions/39428042/use-selenium-with-chromedriver-on-mac
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")

# Load in your browser (I use chrome)
browser = webdriver.Chrome(executable_path = DRIVER_BIN)

# An implicit wait tells WebDriver to poll the DOM for a certain amount of time when trying to find any element (or elements) not immediately available.
# I should experiment with using an explicit wait instead, based on whether the PMIDs have loaded or not
# Documentation: https://selenium-python.readthedocs.io/waits.html
browser.implicitly_wait(100)

# Get the url with Selenium
browser.get(orchid_url)

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

# Xpath for all DOIs and PMIDs together
# //*[@id="body-work-list"]/li/div/ul/li/div/div/ul/li/ul/li/span/ext-id-popover-ng2/a

# Xpath for individual DOI
#//*[@id="body-work-list"]/li[134]/div/ul/li/div[2]/div/ul/li/ul/li[1]/span/ext-id-popover-ng2/a
# Xpath for all DOIs
#//*[@id="body-work-list"]/li/div/ul/li/div/div/ul/li/ul/li[1]/span/ext-id-popover-ng2/a

# Xpath for individual PMID
#//*[@id="body-work-list"]/li[134]/div/ul/li/div[2]/div/ul/li/ul/li[2]/span/ext-id-popover-ng2/a
# Xpath for all PMIDs
#//*[@id="body-work-list"]/li/div/ul/li/div/div/ul/li/ul/li[2]/span/ext-id-popover-ng2/a


pmids= tree.xpath('//*[@id="body-work-list"]/li/div/ul/li/div/div/ul/li/ul/li[2]/span/ext-id-popover-ng2/a/text()')

pmid_counter = 0

for i in pmids:
    pmid_counter += 1

# Close the browser
browser.quit()

# Print results
print('Name: ' + person )
print('URL for Orchid ID page: ' + orchid_url )
print('Number of PMIDs found: ', pmid_counter )
#print('List of PMIDS: ')
#print(pmid_list)