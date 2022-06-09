import pandas as pd

df = pd.read_csv('Scovelo.csv')

print(df.columns)
# df.re

for column in df.columns:
    if "Unnamed" in column:
        df.drop(columns=column, inplace=True, axis=1)

print(df.columns)

df.to_csv('Scovelo.csv')