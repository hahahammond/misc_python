import pandas as pd

lindsay_data = pd.read_csv("raw_lindsay.csv",index_col=False, low_memory=False)
#print(lindsay_data)

lindsay_data[['notes', 'rayyan inclusion']] = lindsay_data['notes'].str.split(pat='RAYYAN-INCLUSION:', n=1, expand=True)

lindsay_data[['rayyan inclusion', 'rayyan exclusion reasons']] = lindsay_data['rayyan inclusion'].str.split(pat='RAYYAN-EXCLUSION-REASONS:',n=1, expand=True)

#lindsay_data['rayyan inclusion'].astype(str)

for index, row in lindsay_data.iterrows():
    if 'true' in row['rayyan inclusion']:
        lindsay_data.loc[index, 'rayyan inclusion'] = 'true'
    else:
        lindsay_data.loc[index, 'rayyan inclusion'] = 'false'
        
lindsay_data.to_csv("clean_lindsay_data.csv", index=False)

