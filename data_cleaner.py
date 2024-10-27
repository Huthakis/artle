import pandas as pd

# URL where data is
url = 'https://raw.githubusercontent.com/georgiecoetzer/What-Makes-Art-Valuable/refs/heads/main/Clean%20Data/SothebysData_clean.csv'

# Useful columns
usecols = ['Artist', 'Title', 'Date', 'Location', 'Category', 'Auction Name',
           'Sold', 'Selling Price', 'low_estimate', 'high_estimate', 'Image']

# Load data using url
art_df = pd.read_csv(url, usecols=usecols)

# Filter for sold art with auction estimates
art_df = art_df.loc[art_df['Sold'] == True] 
art_df = art_df.loc[art_df['low_estimate'] > 0]

# Convert 'Artist' and 'Title' to title case
art_df.Artist = art_df.Artist.str.title()
art_df.Title = art_df.Title.str.title()

# Remove artists that only appear once
artist_counts = art_df['Artist'].value_counts()
artists_to_keep = artist_counts[artist_counts > 1].index
art_df = art_df[art_df['Artist'].isin(artists_to_keep)]

# Remove non-Latin characters from 'Title' and strip whitespace
art_df['Title'] = art_df['Title'].str.replace(r'[|：、・《》\u4e00-\u9fff]', '', regex=True)
art_df.Title = art_df.Title.str.strip()

# Sort dataframe by 'Artist' and 'Title'
art_df = art_df.sort_values(['Artist', 'Title'])

# Save cleaned data to csv
art_df.to_csv('art_data.csv', index=False)
