import pandas as pd
cols = pd.read_csv("Wildfire_Dataset.csv", nrows=0).columns.tolist()
print(cols)
