#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 15:07:49 2019

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

# Get URL for Orchid ID

orchid_id = '0000-0001-6023-9062'
orchid_url = 'https://orcid.org/'+ orchid_id + '/print'
print(orchid_url)

# Make request and extract all URLS from page and person's name
r = requests.get(orchid_url)
tree = lxml.html.fromstring(r.content)
#all_urls = tree.xpath('//span/a/@href')
#person = tree.xpath('//span[@id="ctl00_lbl_main_heading"]/text()')[0]

nameo = tree.xpath('//*[contains(@class,’foo’)]')

# xpath
#//*[@id="body-work-list"]/li[1]/div/ul/li/div[2]/div/ul/li/ul/li[1]/span/ext-id-popover-ng2/a

# element
#<a class="truncate-anchor inline" target="orcid.blank" href="https://www.ncbi.nlm.nih.gov/pubmed/24023320">24023320</a>

test= tree.xpath('//*[@id="body-work-list"]/li[2]/div/ul/li/div[2]/div/ul/li/ul/li[2]/span/ext-id-popover-ng2/a')


for i in test:
    print(i)

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

print('Name: ' + person )
print('URL for Orchid ID page: ' + orchid_url )
print('Number of PMIDs found: ' + pmid_counter )
print('List of PMIDS: ')
print(pmid_list)