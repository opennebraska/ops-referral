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



with document(title='Omaha Public Schools Referral (Disciplinary) Data Analysis') as doc:
  h1('Omaha Public Schools Referral (Disciplinary) Data Analysis')
  h2('2018-2019 School Year')
  h3('Students')
  raw(df1.to_html(index=False))
  raw('<img src="d1.png">')
  h3('Total Referrals')
  raw(df2.to_html(index=False))
  raw('<img src="d2.png">')

  # for path in photos:
  #   div(img(src=path), _class='photo')

with open('index.html', 'w') as f:
  f.write(doc.render())
