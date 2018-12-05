# Import libraries
import pandas as pd

# Read csv into df
rayyan_data = pd.read_csv("raw_rayyan.csv",index_col=False)

# Split 'notes' column into 'notes' and 'rayyan inclusion' columns
rayyan_data[['notes', 'rayyan inclusion']] = rayyan_data['notes'].str.split(pat='RAYYAN-INCLUSION:', n=1, expand=True)

# Split 'rayyan inclusion' column into 'rayyan inclusion' and 'rayan exclusion reasons' columns
rayyan_data[['rayyan inclusion', 'rayyan exclusion reasons']] = rayyan_data['rayyan inclusion'].str.split(pat='RAYYAN-EXCLUSION-REASONS:',n=1, expand=True)

# Clean up formatting of values in 'rayyan inclusion' column
for index, row in rayyan_data.iterrows():
    if(pd.isnull(row['rayyan inclusion'])) == False:
        if 'true' in row['rayyan inclusion']:
            rayyan_data.loc[index, 'rayyan inclusion'] = 'true'
        else:
            rayyan_data.loc[index, 'rayyan inclusion'] = 'false'

# Export df as csv        
rayyan_data.to_csv("clean_rayyan.csv", index=False)

