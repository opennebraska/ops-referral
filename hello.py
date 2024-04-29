import pandas as pd

pd.options.display.max_columns = None
pd.options.display.max_rows = None
pd.options.display.width = 1000

df = pd.read_excel('OPS Referral Data 2018-2019.xlsx', sheet_name=1)
print(df.head())
print("JAY0")
print(df.columns)
print("JAY1")
print(df.columns.tolist())
print("JAY2")
print(df.loc[0, :])
