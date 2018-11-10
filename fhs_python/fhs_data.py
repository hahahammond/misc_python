import pandas as pd
import os

# Define txt file stitch function
def stitch(root, output_name):
    files = [f for f in os.listdir(root)]
    merged = []
    
    for f in files:
        if not f.startswith('.') and os.path.isfile(os.path.join(root, f)):
            filename, ext = os.path.splitext(f)
            if ext == '.txt':
                print(f)
                read = pd.read_csv((os.path.join(root, f)), sep='\t', header=0)
                merged.append(read)
    
    result = pd.concat(merged)
    result.to_csv(output_name, index=False)

# Clean up data for Top 25 Journal Titles of Publications Citing FHS Publications
top_journals = pd.read_csv("top_journals.txt",delimiter="	")
print(top_journals)
top_journals.to_csv("top_journals.csv", index=False)

# Calculate Average FHS documents per year
pub_years=pd.read_csv("pub_years.txt",delimiter="	")
avg_num_pubs = pub_years.records.mean()
print(avg_num_pubs)

# Extract PMIDs for 2018 FHS publications
all_pubs_2018 = pd.read_csv("all_pubs_2018.txt", delimiter='\t',index_col=False, low_memory=False)
print(all_pubs_2018)
all_pubs_2018.to_csv("all_pubs_2018.csv", index=False)
all_pubs_2018.PM.dropna().to_csv("pmids_2018.csv", index=False)

# Stitch together tsvs for all publications by FHS fellows in batches of <= 500
stitch('all_fellows_pubs_files', 'all_fellows_pubs_data.csv')

# Extract PMIDs for all publications by FHS fellows 
fellows_data = pd.read_csv("all_fellows_pubs_data.csv",index_col=False, low_memory=False)
print(fellows_data)
fellows_data.PM.dropna().to_csv("all_fellows_pubs_pmids.csv", index=False)

# Stitch together tsvs for 2012-2017 publications by FHS fellows in batches of <= 500
stitch('fellows_pubs_2012_to_2017_files', 'fellows_pubs_2012_to_2017.csv')

## Extract PMIDs for 2012-2017 publications by FHS fellows 
fellows_pubs_2012_to_2017_data = pd.read_csv("fellows_pubs_2012_to_2017.csv",index_col=False, low_memory=False)
print(fellows_pubs_2012_to_2017_data)
fellows_pubs_2012_to_2017_data.PM.dropna().to_csv("fellows_pubs_2012_to_2017_pmids.csv", index=False)

## Extract PMIDs for 2017 publications by FHS fellows 
fellows_pubs_2017_data = pd.read_csv("fellows_pubs_2012_to_2017_files/fellows_pubs_2017.txt",delimiter='\t',index_col=False, low_memory=False)
print(fellows_pubs_2017_data)
fellows_pubs_2017_data.PM.dropna().to_csv("fellows_pubs_2017_pmids.csv", index=False)

