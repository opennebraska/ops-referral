import pandas as pd
import sqlite3

pd.options.display.max_columns = None
pd.options.display.max_rows = None
pd.options.display.width = 1000

df = pd.read_excel('data/OPS Referral Data 2018-2019.xlsx', sheet_name=1)
print(df.head())
print("JAY0")
print(df.columns)
print("JAY1")
print(df.columns.tolist())
print("JAY2")
print(df.loc[0, :])

# https://stackoverflow.com/a/61473956/4656035
# connect to database
conn = sqlite3.connect("data/ops.sqlite3")

# Create a database table and write all the dataframe data into it
df.to_sql("disc", conn, if_exists="replace")
conn.commit()
conn.close()

# create the table
# conn.execute(
#     """
#     DROP TABLE IF EXISTS disc;
#     CREATE TABLE disc AS
#     SELECT * FROM disc_df
#     """)
