#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 15:56:45 2019

@author: larkink
"""
# Import libraries
import pandas as pd

# Specify input files
DATA_FILE = 'data.csv'
DESC_FILE = 'col_desc.csv'

# Create output function
def output_func(column, column_desc, data_dictionary):
   output_str = 'Column %s describes %s.' % (column, column_desc)
   for key, value in data_dictionary.items():
       output_str += ' There are %d individuals with a value of %d.' % (value, key)
   print(output_str)
   return output_str
       
# Create list of categorical data columns
col_list = ['COL1', 'COL2', 'COL3', 'COL4']

# Load DESC_file as dataframe, then dictionary
col_desc_dict = pd.read_csv(DESC_FILE, index_col=0, squeeze=True).to_dict()

# Load DATA_FILE as dataframe
data_df = pd.read_csv(DATA_FILE)

# Loop through column list to match column name, description, and value counts, then output text file
for col in col_list:
    if col in col_desc_dict.keys():
        data_dict = data_df[col].value_counts().to_dict()
        col_desc = col_desc_dict[col]
        output = output_func(col, col_desc, data_dict)
        print(col)
        print(data_dict)
        with open('output.txt', 'a') as text_file:
            text_file.write(output + '\n' + '\n')