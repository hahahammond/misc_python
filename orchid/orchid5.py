# Import libraries
import os
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import lxml.html
import requests
import re
import operator
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import urllib.parse
import json
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

page_url = 'https://orcid.org/0000-0001-6023-9062'

if 'profiles.bu.edu' in page_url:
    # Make request and extract all URLS from page and person's name
    r = requests.get(page_url)
    tree = lxml.html.fromstring(r.content)
    all_urls = tree.xpath('//span/a/@href')
    person = tree.xpath('//span[@id="ctl00_lbl_main_heading"]/text()')[0]

    # Initiate PubMed URL list
    pubmed_url_list = []

    # Find URLs pointing to PubMed articles and add to list
    for url in all_urls:
        pubmed_url = re.findall('//www.ncbi.nlm.nih.gov/pubmed/.*$', url)
        if pubmed_url:
            pubmed_url_list.append(pubmed_url[0])

    # Initiate PMID counter and PMID list
    pmid_counter = 0
    pmid_list = []

    # Find PMIDs in PubMed article URLs and update PMID counter
    for raw_pubmed_url in pubmed_url_list:
        clean_pubmed_url = raw_pubmed_url.replace('//www.ncbi.nlm.nih.gov/pubmed/', '')
        pmid_list.append(clean_pubmed_url)
        pmid_counter += 1

else:
    # Get URL for Orchid ID page you want to scrape
    if 'orchid.org' not in page_url:
        page_url = 'https://orcid.org/' + page_url + '/print'
    else:
        page_url = page_url + '/print'

    with Display():
        # we can now start Firefox and it will run inside the virtual display
        browser = webdriver.Firefox()

        # put the rest of our selenium code in a try/finally
        # to make sure we always clean up at the end
        try:
            browser.get(page_url)

            # An explicit wait is a code you define to wait for a certain condition to occur before proceeding further in the code.
            # Documentation: https://selenium-python.readthedocs.io/waits.html
            element = WebDriverWait(browser, 100).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="body-work-list"]/li[last()]')))

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
            person = tree.xpath('//*[@id="main"]/div/div[1]/div/print-id-banner-ng2/div/h2/text()')[0].strip()
            pmid_urls = tree.xpath('//a[contains(@href,"pubmed")]/@href')
            # Remove duplicate urls
            pmid_urls = list(set(pmid_urls))

            # Create list of pmids
            pmid_list = []

            for i in pmid_urls:
                pmid_list.append(i.strip('https://www.ncbi.nlm.nih.gov/pubmed/'))

            # Count pmids in list
            pmid_counter = 0

            for j in pmid_list:
                pmid_counter += 1

        finally:
            browser.quit()


