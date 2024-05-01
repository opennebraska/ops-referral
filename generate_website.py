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
  SELECT raceEthnicity, count(*) total_referrals
  FROM disc
  GROUP BY 1;
"""
df = pd.read_sql_query(sqlstr, con)
print(df.head())

# Discard 0th column which is just row numbers.
# Ooops, nope, we need to change to_html() below apparently
# df = df.drop(df.columns[[0]], axis=1)

sns_plot = sns.barplot(data=df, x="total_referrals", y="RaceEthnicity")  # , hue='species', height=2.5)
plt.savefig('d1.png', bbox_inches='tight')

with document(title='Omaha Public Schools Referral (Disciplinary) Data Analysis') as doc:
  h1('Omaha Public Schools Referral (Disciplinary) Data Analysis')
  h2('2018-2019 School Year')
  h3('Total Referrals')
  raw(df.to_html(index=False))
  raw('<img src="d1.png">')

  # for path in photos:
  #   div(img(src=path), _class='photo')

with open('index.html', 'w') as f:
  f.write(doc.render())
