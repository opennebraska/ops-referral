import pandas as pd
import sqlite3

pd.options.display.max_columns = None
pd.options.display.max_rows = None
pd.options.display.width = 1000

# https://stackoverflow.com/a/61473956/4656035
conn = sqlite3.connect("data/ops.sqlite3")

df1 = pd.read_excel('data/OPS Referral Data 2018-2019.xlsx', sheet_name=1)
print(df1.head())
# print(df1.columns.tolist())
print(df1.loc[0, :])
# Create a database table and write all the dataframe data into it
df1.to_sql("disc", conn, if_exists="replace")

df2 = pd.read_excel(
  'data/SchoolLevel_RaceGenderGradeMembership_1718to1920.xlsx',
  sheet_name=1,
  usecols="A:W",
  header=None,
  skiprows=3,    # Drop the 3 header rows, the human-friendly formatting is confusing
  skipfooter=1,  # Also drop grand total row at the bottom
)
# print(df2.head())
# Drop Total columns
df2 = df2.drop([22], axis=1)
df2 = df2.drop([19], axis=1)
df2 = df2.drop([16], axis=1)
df2 = df2.drop([13], axis=1)
df2 = df2.drop([10], axis=1)
df2 = df2.drop([7], axis=1)
df2 = df2.drop([4], axis=1)
# Provide new column names because we just deleted all the human-friendly ones
columns = ['AA-F', 'AA-M', 'A-F', 'A-M', 'H-F', 'H-M', 'MR-F', 'MR-M', 'NA-F', 'NA-M', 'PA-F', 'PA-M', 'W-F', 'W-M']
df2.columns = ['school', 'grade', *columns]
# Change to Pandas int to keep NaNs. NOT Numpy int, which fails on NaN
# We can't do dataframe ranges for this (explodes)?
#   df2['AA-F':'W-M'] = df2['AA-F':'W-M'].astype('Int64')  # capital I
for column in columns:
  df2[column] = df2[column].astype('Int64')  # capital I
# Drop all rows with "Total" in the school name
df2 = df2[~df2["school"].str.contains("Total", na=False)]
# They didn't re-state the school every time, which is convenient for humans, but terrible
# for data processing. Luckily Pandas can fill the missing data back in for us:
df2["school"] = df2["school"].ffill()

print("Final dataframe:")
print(df2.head())

# Reverse their crosstab https://stackoverflow.com/questions/69550812/pandas-reverse-of-a-crosstab
# s = df2.stack([0, 1, 2, 3, 4])
# print("Our stack:")
# print(s)
# Uhh... ya, I can't figure this out. I'll just do it in Perl

# Create a database table and write all the dataframe data into it
df2.to_sql("membership_raw", conn, if_exists="replace")

conn.commit()
conn.close()
