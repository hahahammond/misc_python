# Import libraries
import pandas as pd

# Read csv into df
lindsay_data = pd.read_csv("raw_lindsay.csv",index_col=False)

# Split 'notes' column into 'notes' and 'rayyan inclusion' columns
lindsay_data[['notes', 'rayyan inclusion']] = lindsay_data['notes'].str.split(pat='RAYYAN-INCLUSION:', n=1, expand=True)

# Split 'rayyan inclusion' column into 'rayyan inclusion' and 'rayan exclusion reasons' columns
lindsay_data[['rayyan inclusion', 'rayyan exclusion reasons']] = lindsay_data['rayyan inclusion'].str.split(pat='RAYYAN-EXCLUSION-REASONS:',n=1, expand=True)

# Clean up formatting of values in 'rayyan inclusion' column
for index, row in lindsay_data.iterrows():
    if(pd.isnull(row['rayyan inclusion'])) == False:
        if 'true' in row['rayyan inclusion']:
            lindsay_data.loc[index, 'rayyan inclusion'] = 'true'
        else:
            lindsay_data.loc[index, 'rayyan inclusion'] = 'false'

# Export df as csv        
lindsay_data.to_csv("clean_lindsay_data.csv", index=False)

