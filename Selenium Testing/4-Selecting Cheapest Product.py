import pandas as pd

# Note: when saving to csv, and then reading, all datatypes get converted to STRING
# This long ass read_csv converts columns into appropriate datatypes
df = pd.read_csv("Extracted SSIM - Threshold 0.9.csv", converters={'Price': pd.eval, 'itemId': pd.eval, 'Cluster_Similarity': pd.eval})

# List comprehension: access the column name (series), what index (value), and the first item of the value
cluster_number = [df['Cluster_Similarity'][index][0] for index in df.index]
df['Cluster_Number'] = cluster_number

df = df.sort_values(by=['Cluster_Number', 'Price'])

# Ignore column 0
cheapest_df = pd.DataFrame(columns=df.columns)

# Make a list of clusters to iterate over as a condition (i.e., if Cluster_Number == cluster in list)
# Extract a subset of dataframe using the condition

cluster_set = list(set(df['Cluster_Number']))

for cluster_num in cluster_set:
    df_portion = df[df['Cluster_Number'] == cluster_num]
    # Since dataframe is sorted secondarily by price, this will always be the cheapest option
    df_portion = df_portion.iloc[0]

    cheapest_df.loc[len(cheapest_df.index)] = list(df_portion)

# Removes the unnecessary first column and saves it
cheapest_df = cheapest_df.drop(['Unnamed: 0'], axis=1)
cheapest_df.to_csv('Extracted and Cheapest Selected.csv', index=False)