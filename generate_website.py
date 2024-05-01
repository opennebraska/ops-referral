# https://stackoverflow.com/questions/2301163/creating-html-in-python
# https://github.com/Knio/dominate
import glob
from dominate import document
from dominate.tags import *
from dominate.util import raw
import pandas as pd
import matplotlib.pyplot as plt   # https://pandas.pydata.org/docs/user_guide/visualization.html#basic-plotting-plot

# For prettier plots: https://pandas.pydata.org/community/ecosystem.html
import seaborn as sns  # Seaborn https://seaborn.pydata.org

import sqlite3

con = sqlite3.connect("ops.sqlite3")

sqlstr = """
  SELECT raceEthnicity, count(*)
  FROM disc
  GROUP BY 1;
"""
df = pd.read_sql_query(sqlstr, con)

sns_plot = sns.pairplot(df)  # , hue='species', height=2.5)
plt.savefig('d1.png')

# plt = df.plot(kind="bar")
# plt.savefig("d1.png")
# plt.show()

with document(title='Omaha Public Schools Referral (Disciplinary) Data Analysis') as doc:
  h1('Omaha Public Schools Referral (Disciplinary) Data Analysis')
  h2('2018-2019 School Year')
  raw(df.to_html())
  raw('<img src="d1.png">')
  # for path in photos:
  #   div(img(src=path), _class='photo')

with open('index.html', 'w') as f:
  f.write(doc.render())
