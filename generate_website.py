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
  SELECT referral_count, RaceEthnicity, sum(students) students
  FROM disc_cluster
  GROUP BY 1, 2
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

sqlstr = """
  WITH mem AS (
    SELECT RaceEthnicity, sum(students) students FROM membership GROUP BY 1
  )
  SELECT dc.referral_count, dc.RaceEthnicity, ROUND(sum(dc.students) * 1.0 / mem.students * 100, 2) percent
  FROM disc_cluster dc
  JOIN mem ON (dc.RaceEthnicity = mem.RaceEthnicity)
  GROUP BY 1, 2
"""
df5 = pd.read_sql_query(sqlstr, con)
df5 = df5.pivot_table(index='referral_count', columns='RaceEthnicity', values='percent')
# Change to Pandas int to get rid of all the ".0"s
# for r in raceEthnicity:
#   df4[r] = df4[r].astype('Int64')  # capital I
print(df5.head())
sns_plot = sns.lineplot(data=df5)
sns_plot.set_xlabel('Referral Count')
sns_plot.set_ylabel("% of students")
plt.savefig('d5.png', bbox_inches='tight')
plt.clf()

sqlstr = """
  SELECT referral_count, RaceEthnicity, sum(students) students
  FROM disc_cluster
  WHERE grade IN ('PK', 'KG', 1, 2, 3)
  GROUP BY 1, 2
"""
df11 = pd.read_sql_query(sqlstr, con)
print(df11.head())
df11 = df11.pivot_table(index='referral_count', columns='RaceEthnicity', values='students')
print(df11.head())
print(df11.columns)
# Change to Pandas int to get rid of all the ".0"s
for r in raceEthnicity:
  df11[r] = df11[r].astype('Int64')  # capital I
print(df11.head())
sns_plot = sns.lineplot(data=df11)
sns_plot.set_xlabel("Referral Count")
sns_plot.set_ylabel("Students")
plt.savefig('d11.png', bbox_inches='tight')
plt.clf()

sqlstr = """
  SELECT referral_count, RaceEthnicity, sum(students) students
  FROM disc_cluster
  WHERE grade IN (4, 5, 6)
  GROUP BY 1, 2
"""
df21 = pd.read_sql_query(sqlstr, con)
print(df21.head())
df21 = df21.pivot_table(index='referral_count', columns='RaceEthnicity', values='students')
print(df21.head())
print(df21.columns)
# Change to Pandas int to get rid of all the ".0"s
for r in raceEthnicity:
  df21[r] = df21[r].astype('Int64')  # capital I
print(df21.head())
sns_plot = sns.lineplot(data=df21)
sns_plot.set_xlabel("Referral Count")
sns_plot.set_ylabel("Students")
plt.savefig('d21.png', bbox_inches='tight')
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
  h2('Count of referrals')
  # raw(df3.to_html())
  raw(df4.to_html())
  raw('<img src="d4.png">')
  raw('<img src="d3.png">')
  h2('Percentage of students with referrals')
  raw(df5.to_html())
  raw('<img src="d5.png">')
  h2('Pre-K through 3: Referrals')
  raw(df11.to_html())
  raw('<img src="d11.png">')
  h2('Grades 4 through 6: Referrals')
  raw(df21.to_html())
  raw('<img src="d21.png">')

  # for path in photos:
  #   div(img(src=path), _class='photo')

with open('index.html', 'w') as f:
  f.write(doc.render())
