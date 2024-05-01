# https://stackoverflow.com/questions/2301163/creating-html-in-python
# https://github.com/Knio/dominate
import glob
from dominate import document
from dominate.tags import *
from dominate.util import raw
import pandas as pd
import matplotlib.pyplot as plt   # https://pandas.pydata.org/docs/user_guide/visualization.html#basic-plotting-plot

# For prettier plots: https://pandas.pydata.org/community/ecosystem.html
import seaborn as sns  # https://seaborn.pydata.org

import sqlite3

raceEthnicity = ['African American', 'Asian', 'Hispanic', 'Multi Racial', 'Native American', 'Pacific Islander', 'White']

con = sqlite3.connect("ops.sqlite3")

sqlstr = """
  SELECT raceEthnicity, sum(students) students
  FROM membership
  GROUP BY 1;
"""
df1 = pd.read_sql_query(sqlstr, con)
print(df1.head())
sns_plot = sns.barplot(data=df1, x="students", y="RaceEthnicity")
plt.savefig('d1.png', bbox_inches='tight')
plt.clf()  # https://stackoverflow.com/questions/741877/how-do-i-tell-matplotlib-that-i-am-done-with-a-plot

sqlstr = """
  SELECT raceEthnicity, count(*) total_referrals
  FROM disc
  GROUP BY 1;
"""
df2 = pd.read_sql_query(sqlstr, con)
print(df2.head())
sns_plot = sns.barplot(data=df2, x="total_referrals", y="RaceEthnicity")
plt.savefig('d2.png', bbox_inches='tight')
plt.clf()

sqlstr = """
  WITH repeat_referrals AS (
    SELECT RaceEthnicity, count(*) referral_count
    FROM disc
    GROUP BY "w"
  )
  SELECT referral_count, RaceEthnicity, count(*) students
  FROM repeat_referrals
  GROUP BY 1,2;
"""
df3 = pd.read_sql_query(sqlstr, con)
print(df3.head())
df3 = df3.pivot_table(index='referral_count', columns='RaceEthnicity', values='students')
print(df3.head())

# Hmmm... can't seem to do what cluster.pl does. Give up and use that instead...?
# df3['bucket'] = df3.qcut(
#      ... https://practicaldatascience.co.uk/machine-learning/how-to-bin-or-bucket-customer-data-using-pandas
#   df3['referral_count'],
#   q=[pivot_table(index='referral_count', columns='RaceEthnicity', values='students')
# print(df3.head())

sns_plot = sns.lineplot(data=df3)
sns_plot.set_xlabel("Referral Count")
sns_plot.set_ylabel("Students")
sns_plot.set_xscale("log")
sns_plot.set_yscale("log")
plt.savefig('d3.png', bbox_inches='tight')
plt.clf()

sqlstr = """
  SELECT *
  FROM disc_cluster
"""
df4 = pd.read_sql_query(sqlstr, con)
print(df4.head())
df4 = df4.pivot_table(index='referral_count', columns='RaceEthnicity', values='students')
print(df4.head())
print(df4.columns)
# Change to Pandas int to get rid of all the ".0"s
for r in raceEthnicity:
  df4[r] = df4[r].astype('Int64')  # capital I
print(df4.head())
sns_plot = sns.lineplot(data=df4)
sns_plot.set_xlabel("Referral Count")
sns_plot.set_ylabel("Students")
plt.savefig('d4.png', bbox_inches='tight')
plt.clf()



with document(title='Omaha Public Schools Referral (Disciplinary) Data 2018-2019') as doc:
  h1('Omaha Public Schools 2018-2019')
  raw('Referral (disciplinary) data analysis. <a href="https://github.com/opennebraska/ops-referral">[Source code]</a>')
  h2('Students')
  raw(df1.to_html(index=False))
  raw('<img src="d1.png">')
  h2('Total Referrals')
  raw(df2.to_html(index=False))
  raw('<img src="d2.png">')
  h2('Number of referrals > 0')
  # raw(df3.to_html())
  raw(df4.to_html())
  raw('<img src="d4.png">')
  raw('<img src="d3.png">')

  # for path in photos:
  #   div(img(src=path), _class='photo')

with open('index.html', 'w') as f:
  f.write(doc.render())
