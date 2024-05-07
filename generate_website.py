# https://stackoverflow.com/questions/2301163/creating-html-in-python
# https://github.com/Knio/dominate
import glob
from dominate import document
from dominate.tags import *
from dominate.util import raw
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt   # https://pandas.pydata.org/docs/user_guide/visualization.html#basic-plotting-plot

# For prettier plots: https://pandas.pydata.org/community/ecosystem.html
import seaborn as sns  # https://seaborn.pydata.org

import sqlite3

raceEthnicity = ['African American', 'Asian', 'Hispanic', 'Multi Racial', 'Native American', 'Pacific Islander', 'White']

con = sqlite3.connect("ops.sqlite3")

# ======== OVERALL DISCIPLINE PICTURE ============

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
# print(df3.head())
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
df4 = df4.pivot_table(index='referral_count', columns='RaceEthnicity', values='students')
print(df4.head())
# print(df4.columns)
# Change to Pandas int to get rid of all the ".0"s
for r in raceEthnicity:
  df4[r] = df4[r].astype('Int64')  # capital I
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

# -------------- Pre-K through 3 -------------------

sqlstr = """
  WITH referrals AS (
    SELECT count(*) total_referrals
    FROM disc
    WHERE grade IN ('PK', 'KG', 1, 2, 3)
  ),
  repeat_referrals AS (
    SELECT count(*) unique_students
    FROM disc
    WHERE grade IN ('PK', 'KG', 1, 2, 3)
    GROUP BY "w"
  ),
  unique_repeat_referrals AS (
    SELECT count(unique_students) one_or_more
    FROM repeat_referrals
  )
  SELECT sum(students) students, r.total_referrals, urr.one_or_more
  FROM membership m
  JOIN referrals r
  JOIN unique_repeat_referrals urr
  WHERE grade IN ('PK', 'KG', 1, 2, 3)
"""
df10 = pd.read_sql_query(sqlstr, con)
print(df10.head())

sqlstr = """
  WITH referrals AS (
    SELECT RaceEthnicity, count(*) total_referrals
    FROM disc
    WHERE grade IN ('PK', 'KG', 1, 2, 3)
    GROUP BY 1
  ),
  repeat_referrals AS (
    SELECT RaceEthnicity, count(*) unique_students
    FROM disc
    WHERE grade IN ('PK', 'KG', 1, 2, 3)
    GROUP BY "w"
  ),
  unique_repeat_referrals AS (
    SELECT RaceEthnicity, count(unique_students) one_or_more
    FROM repeat_referrals
    GROUP BY 1
  )
  SELECT m.raceEthnicity, sum(students) students, r.total_referrals, urr.one_or_more
  FROM membership m
  JOIN referrals r ON (r.RaceEthnicity = m.RaceEthnicity)
  JOIN unique_repeat_referrals urr ON (urr.RaceEthnicity = m.RaceEthnicity)
  WHERE grade IN ('PK', 'KG', 1, 2, 3)
  GROUP BY 1;
"""
df11 = pd.read_sql_query(sqlstr, con)
print(df11.head())

sqlstr = """
  SELECT referral_count, RaceEthnicity, sum(students) students
  FROM disc_cluster
  WHERE grade IN ('PK', 'KG', 1, 2, 3)
  GROUP BY 1, 2
"""
df12 = pd.read_sql_query(sqlstr, con)
df12 = df12.pivot_table(index='referral_count', columns='RaceEthnicity', values='students')
print(df12.head())
sns_plot = sns.lineplot(data=df12)
sns_plot.set_xlabel("Referral Count")
sns_plot.set_ylabel("Students")
plt.savefig('d12.png', bbox_inches='tight')
plt.clf()

sqlstr = """
  WITH mem AS (
    SELECT RaceEthnicity, sum(students) students
    FROM membership
    WHERE grade IN ('PK', 'KG', 1, 2, 3)
    GROUP BY 1
  )
  SELECT dc.referral_count, dc.RaceEthnicity, ROUND(sum(dc.students) * 1.0 / mem.students * 100, 2) percent
  FROM disc_cluster dc
  JOIN mem ON (dc.RaceEthnicity = mem.RaceEthnicity)
  WHERE grade IN ('PK', 'KG', 1, 2, 3)
  GROUP BY 1, 2
"""
df13 = pd.read_sql_query(sqlstr, con)
df13 = df13.pivot_table(index='referral_count', columns='RaceEthnicity', values='percent')
print(df13.head())
sns_plot = sns.lineplot(data=df13)
sns_plot.set_xlabel('Referral Count')
sns_plot.set_ylabel("% of students")
plt.savefig('d13.png', bbox_inches='tight')
plt.clf()

# -------------- Grades 4,5,6 -------------------

sqlstr = """
  WITH referrals AS (
    SELECT count(*) total_referrals
    FROM disc
    WHERE grade IN (4, 5, 6)
  ),
  repeat_referrals AS (
    SELECT count(*) unique_students
    FROM disc
    WHERE grade IN (4, 5, 6)
    GROUP BY "w"
  ),
  unique_repeat_referrals AS (
    SELECT count(unique_students) one_or_more
    FROM repeat_referrals
  )
  SELECT sum(students) students, r.total_referrals, urr.one_or_more
  FROM membership m
  JOIN referrals r
  JOIN unique_repeat_referrals urr
  WHERE grade IN (4, 5, 6)
"""
df20 = pd.read_sql_query(sqlstr, con)
print(df20.head())

sqlstr = """
  WITH referrals AS (
    SELECT RaceEthnicity, count(*) total_referrals
    FROM disc
    WHERE grade IN (4, 5, 6)
    GROUP BY 1
  ),
  repeat_referrals AS (
    SELECT RaceEthnicity, count(*) unique_students
    FROM disc
    WHERE grade IN (4, 5, 6)
    GROUP BY "w"
  ),
  unique_repeat_referrals AS (
    SELECT RaceEthnicity, count(unique_students) one_or_more
    FROM repeat_referrals
    GROUP BY 1
  )
  SELECT m.raceEthnicity, sum(students) students, r.total_referrals, urr.one_or_more
  FROM membership m
  JOIN referrals r ON (r.RaceEthnicity = m.RaceEthnicity)
  JOIN unique_repeat_referrals urr ON (urr.RaceEthnicity = m.RaceEthnicity)
  WHERE grade IN (4, 5, 6)
  GROUP BY 1;
"""
df21 = pd.read_sql_query(sqlstr, con)
print(df21.head())

sqlstr = """
  SELECT referral_count, RaceEthnicity, sum(students) students
  FROM disc_cluster
  WHERE grade IN (4, 5, 6)
  GROUP BY 1, 2
"""
df22 = pd.read_sql_query(sqlstr, con)
df22 = df22.pivot_table(index='referral_count', columns='RaceEthnicity', values='students')
sns_plot = sns.lineplot(data=df22)
sns_plot.set_xlabel("Referral Count")
sns_plot.set_ylabel("Students")
plt.savefig('d22.png', bbox_inches='tight')
plt.clf()

sqlstr = """
  WITH mem AS (
    SELECT RaceEthnicity, sum(students) students
    FROM membership
    WHERE grade IN (4, 5, 6)
    GROUP BY 1
  )
  SELECT dc.referral_count, dc.RaceEthnicity, ROUND(sum(dc.students) * 1.0 / mem.students * 100, 2) percent
  FROM disc_cluster dc
  JOIN mem ON (dc.RaceEthnicity = mem.RaceEthnicity)
  WHERE grade IN (4, 5, 6)
  GROUP BY 1, 2
"""
df23 = pd.read_sql_query(sqlstr, con)
df23 = df23.pivot_table(index='referral_count', columns='RaceEthnicity', values='percent')
print(df23.head())
sns_plot = sns.lineplot(data=df23)
sns_plot.set_xlabel('Referral Count')
sns_plot.set_ylabel("% of students")
plt.savefig('d23.png', bbox_inches='tight')
plt.clf()

# ======== REASONS FOR REFERRALS ============

sqlstr = """
  SELECT eventName, count(*)
  FROM disc
  WHERE Grade IN ('PK', 'KG', 1, 2, 3)
  GROUP BY 1
  ORDER BY 2 DESC
  LIMIT 10;
"""
df100 = pd.read_sql_query(sqlstr, con)
print(df100.head())

sqlstr = """
  SELECT raceEthnicity, eventName, occurrences
  FROM reasons
  WHERE grades = '''PK'', ''KG'', 1, 2, 3'
"""
df101 = pd.read_sql_query(sqlstr, con)
print(df101.head())

sqlstr = """
  SELECT eventName, count(*)
  FROM disc
  WHERE grade IN (4, 5, 6)
  GROUP BY 1
  ORDER BY 2 DESC
  LIMIT 10;
"""
df110 = pd.read_sql_query(sqlstr, con)
print(df110.head())

sqlstr = """
  SELECT raceEthnicity, eventName, occurrences
  FROM reasons
  WHERE grades = '4, 5, 6'
"""
df111 = pd.read_sql_query(sqlstr, con)
print(df111.head())

# ======== RESOLUTIONS ============

sqlstr = """
  SELECT rc.category, count(*)
  FROM disc
  JOIN resolution_categories rc ON (disc.resolutionName = rc.resolutionName)
  AND Grade IN ('PK', 'KG', 1, 2, 3)
  GROUP BY 1
"""
df200 = pd.read_sql_query(sqlstr, con)
print(df200.head())

sqlstr = """
  SELECT rc.category, raceEthnicity, count(*) count
  FROM disc
  JOIN resolution_categories rc ON (disc.resolutionName = rc.resolutionName)
  AND Grade IN ('PK', 'KG', 1, 2, 3)
  GROUP BY 1, 2
"""
df201 = pd.read_sql_query(sqlstr, con)
print(df201.head())
df201 = df201.pivot_table(index='category', columns='RaceEthnicity', values='count')
for r in raceEthnicity:
  df201[r] = df201[r].astype('Int64')  # capital I

sqlstr = """
  WITH total_by_race AS (
    SELECT raceEthnicity, count(*) count
    FROM disc
    JOIN resolution_categories rc ON (disc.resolutionName = rc.resolutionName)
    AND Grade IN ('PK', 'KG', 1, 2, 3)
    GROUP BY 1
  )
  SELECT rc.category, disc.raceEthnicity, count(*) * 1.0 / tbr.count * 100 count
  FROM disc
  JOIN resolution_categories rc ON (disc.resolutionName = rc.resolutionName)
  JOIN total_by_race tbr ON (disc.raceEthnicity = tbr.raceEthnicity)
  AND Grade IN ('PK', 'KG', 1, 2, 3)
  GROUP BY 1, 2
"""
df202 = pd.read_sql_query(sqlstr, con)
df202 = df202.pivot_table(index='category', columns='RaceEthnicity', values='count')
print(df202.head())
# nope, no stacking, I get error bars
#   sns_plot = sns.barplot(data=df201)  # , x="category", y="RaceEthnicity")
# nope, no stacking, I get error bars
#   df202.plot(kind='bar', stacked=True)
# nope set_index part fails
#   df202.set_index('category').T.plot(kind='bar', stacked=True)
df202.T.plot(kind='barh', stacked=True, xlabel="%")
plt.savefig('d202.png', bbox_inches='tight')
plt.clf()

sqlstr = """
SELECT resolutionName, count(*)
FROM disc
WHERE Grade IN ('PK', 'KG', 1, 2, 3)
AND resolutionName like '%refer%'
COLLATE NOCASE
GROUP BY 1;
"""
df203 = pd.read_sql_query(sqlstr, con)
print(df203.head())

sqlstr = """
SELECT resolutionName, raceEthnicity, count(*) count
FROM disc
WHERE Grade IN ('PK', 'KG', 1, 2, 3)
AND resolutionName like '%refer%'
COLLATE NOCASE
GROUP BY 1, 2;
"""
df204 = pd.read_sql_query(sqlstr, con)
print(df204.head())
df204 = df204.pivot_table(index='resolutionName', columns='RaceEthnicity', values='count')
for r in raceEthnicity:
  if r == "Pacific Islander":
    df204.insert(5, "Pacific Islander", [np.nan] * 10)  # short version of [np.nan, np.nan, np.nan, ...]

sqlstr = """
  SELECT rc.category, count(*)
  FROM disc
  JOIN resolution_categories rc ON (disc.resolutionName = rc.resolutionName)
  AND Grade IN (4, 5, 6)
  GROUP BY 1
"""
df210 = pd.read_sql_query(sqlstr, con)
print(df210.head())

sqlstr = """
  SELECT rc.category, raceEthnicity, count(*) count
  FROM disc
  JOIN resolution_categories rc ON (disc.resolutionName = rc.resolutionName)
  AND Grade IN (4, 5, 6)
  GROUP BY 1, 2
"""
df211 = pd.read_sql_query(sqlstr, con)
df211 = df211.pivot_table(index='category', columns='RaceEthnicity', values='count')
for r in raceEthnicity:
  df211[r] = df211[r].astype('Int64')  # capital I
print(df211.head())

sqlstr = """
  WITH total_by_race AS (
    SELECT raceEthnicity, count(*) count
    FROM disc
    JOIN resolution_categories rc ON (disc.resolutionName = rc.resolutionName)
    AND Grade IN (4, 5, 6)
    GROUP BY 1
  )
  SELECT rc.category, disc.raceEthnicity, count(*) * 1.0 / tbr.count * 100 count
  FROM disc
  JOIN resolution_categories rc ON (disc.resolutionName = rc.resolutionName)
  JOIN total_by_race tbr ON (disc.raceEthnicity = tbr.raceEthnicity)
  AND Grade IN (4, 5, 6)
  GROUP BY 1, 2
"""
df212 = pd.read_sql_query(sqlstr, con)
df212 = df212.pivot_table(index='category', columns='RaceEthnicity', values='count')
print(df212.head())
df212.T.plot(kind='barh', stacked=True, xlabel="%")
plt.savefig('d212.png', bbox_inches='tight')
plt.clf()

sqlstr = """
SELECT resolutionName, count(*)
FROM disc
WHERE Grade IN (4, 5, 6)
AND resolutionName like '%refer%'
COLLATE NOCASE
GROUP BY 1;
"""
df213 = pd.read_sql_query(sqlstr, con)
print(df213.head())

sqlstr = """
SELECT resolutionName, raceEthnicity, count(*) count
FROM disc
WHERE Grade IN (4, 5, 6)
AND resolutionName like '%refer%'
COLLATE NOCASE
GROUP BY 1, 2;
"""
df214 = pd.read_sql_query(sqlstr, con)
print(df214.head())
df214 = df214.pivot_table(index='resolutionName', columns='RaceEthnicity', values='count')
# print("JAY1:", type(df214.at["Referral to Community Agency", "Asian"]))  # NaN is <class 'numpy.float64'>

# ======== PARENT ENGAGEMENT ============

sqlstr = """
SELECT resolutionName, count(*) count
FROM disc
WHERE Grade IN ('PK', 'KG', 1, 2, 3)
AND resolutionName like '%parent%'
COLLATE NOCASE
GROUP BY 1;
"""
df300 = pd.read_sql_query(sqlstr, con)
print(df300.head())

sqlstr = """
SELECT resolutionName, raceEthnicity, count(*) count
FROM disc
WHERE Grade IN ('PK', 'KG', 1, 2, 3)
AND resolutionName like '%parent%'
COLLATE NOCASE
GROUP BY 1, 2;
"""
df301 = pd.read_sql_query(sqlstr, con)
df301 = df301.pivot_table(index='resolutionName', columns='RaceEthnicity', values='count')
for r in raceEthnicity:
  df301[r] = df301[r].astype('Int64')  # capital I
print(df301.head())

sqlstr = """
SELECT resolutionName, count(*) count
FROM disc
WHERE Grade IN (4, 5, 6)
AND resolutionName like '%parent%'
COLLATE NOCASE
GROUP BY 1;
"""
df310 = pd.read_sql_query(sqlstr, con)
print(df310.head())

sqlstr = """
SELECT resolutionName, raceEthnicity, count(*) count
FROM disc
WHERE Grade IN (4, 5, 6)
AND resolutionName like '%parent%'
COLLATE NOCASE
GROUP BY 1, 2;
"""
df311 = pd.read_sql_query(sqlstr, con)
print(df311.head())
df311 = df311.pivot_table(index='resolutionName', columns='RaceEthnicity', values='count')
for r in raceEthnicity:
  df311[r] = df311[r].astype('Int64')  # capital I

# ======== SUSPENSIONS / EXPULSIONS / EXCLUSION ============

sqlstr = """
SELECT resolutionName, RaceEthnicity, count(*) count
FROM disc
WHERE (
  resolutionName like '%suspen%' OR
  resolutionName like '%expelled%' OR
  resolutionName like '%emergency%' OR
  resolutionName like '%law enfor%'
)
COLLATE NOCASE
GROUP BY 1, 2
"""
df400 = pd.read_sql_query(sqlstr, con)
df400 = df400.pivot_table(index='resolutionName', columns='RaceEthnicity', values='count')
print("JAY2:", type(df400.at["Emergency Exclusion", "Asian"]))  # <NA> is <class 'numpy.float64'>
print(df400.head())

sqlstr = """
WITH all_disc AS (
  SELECT RaceEthnicity, count(*) all_cnt
  FROM disc
  GROUP BY 1
)
SELECT resolutionName, disc.RaceEthnicity,
  round(count(*) * 1.0 / all_cnt * 100, 2) perc
FROM disc
JOIN all_disc ON (disc.RaceEthnicity = all_disc.RaceEthnicity)
WHERE (
  resolutionName like '%suspen%' OR
  resolutionName like '%expelled%' OR
  resolutionName like '%emergency%' OR
  resolutionName like '%law enfor%'
)
COLLATE NOCASE
GROUP BY 1, 2
"""
df401 = pd.read_sql_query(sqlstr, con)
df401 = df401.pivot_table(index='resolutionName', columns='RaceEthnicity', values='perc')
print(df401.head())

sqlstr = """
  SELECT referral_count, RaceEthnicity, sum(students) students
  FROM disc_cluster2
  GROUP BY 1, 2
"""
df402 = pd.read_sql_query(sqlstr, con)
df402 = df402.pivot_table(index='referral_count', columns='RaceEthnicity', values='students')
print(df402.head())
sns_plot = sns.lineplot(data=df402)
sns_plot.set_xlabel("Referral Count")
sns_plot.set_ylabel("Students")
plt.savefig('d402.png', bbox_inches='tight')
plt.clf()

sqlstr = """
  WITH mem AS (
    SELECT RaceEthnicity, sum(students) students
    FROM membership
    GROUP BY 1
  )
  SELECT dc.referral_count, dc.RaceEthnicity, ROUND(sum(dc.students) * 1.0 / mem.students * 100, 2) percent
  FROM disc_cluster2 dc
  JOIN mem ON (dc.RaceEthnicity = mem.RaceEthnicity)
  GROUP BY 1, 2
"""
df403 = pd.read_sql_query(sqlstr, con)
df403 = df403.pivot_table(index='referral_count', columns='RaceEthnicity', values='percent')
print(df403.head())
sns_plot = sns.lineplot(data=df403)
sns_plot.set_xlabel('Referral Count')
sns_plot.set_ylabel("% of students")
plt.savefig('d403.png', bbox_inches='tight')
plt.clf()

sqlstr = """
SELECT eventName, RaceEthnicity, count(*) count
FROM disc
WHERE (
  resolutionName like '%suspen%' OR
  resolutionName like '%expelled%' OR
  resolutionName like '%emergency%' OR
  resolutionName like '%law enfor%'
)
AND Grade IN ('PK', 'KG', 1, 2, 3)
COLLATE NOCASE
GROUP BY 1, 2
"""
df410 = pd.read_sql_query(sqlstr, con)
df410 = df410.pivot_table(index='eventName', columns='RaceEthnicity', values='count')
print(df410.head())

sqlstr = """
SELECT eventName, RaceEthnicity, count(*) count
FROM disc
WHERE (
  resolutionName like '%suspen%' OR
  resolutionName like '%expelled%' OR
  resolutionName like '%emergency%' OR
  resolutionName like '%law enfor%'
)
AND Grade IN (4, 5, 6)
COLLATE NOCASE
GROUP BY 1, 2
"""
df420 = pd.read_sql_query(sqlstr, con)
df420 = df420.pivot_table(index='eventName', columns='RaceEthnicity', values='count')
print(df420.head())


make_zero_empty = lambda x: '{0:.0f}'.format(x) if x > 0 else ''
make_zero_empty_two_digits = lambda x: '{0:.2f}'.format(x) if x > 0 else ''

with document(title='Omaha Public Schools Referral (Disciplinary) Data 2018-2019') as doc:
  h1('Omaha Public Schools 2018-2019')
  raw('Referral (disciplinary) data analysis. <a href="https://github.com/opennebraska/ops-referral">[Source code]</a>')

  # uhh... can't get this working...
  # with doc.add(ul()):
  #   for h2 in ['Students', 'Overall Discipline Picture', 'Reasons for Referrals', 'Resolutions', 'Parent Engagement', 'Suspension, Expulsion, Exclusion']:
  #     li(h2)
  # do we'll do it raw
  raw("""
    <ul>
      <li><a href="#students"   >Students</a></li>
      <li><a href="#overall"    >Overall Discipline Picture</a></li>
      <ul>
        <li><a href="#overall-prek">Pre-K through 3</a></li>
        <li><a href="#overall-4"   >Grades 4 through 6</a></li>
      </ul>
      <li><a href="#reasons"    >Reasons for Referrals</a></li>
      <ul>
        <li><a href="#reasons-prek">Pre-K through 3</a></li>
        <li><a href="#reasons-4"   >Grades 4 through 6</a></li>
      </ul>
      <li><a href="#resolutions">Resolutions</a></li>
      <ul>
        <li><a href="#resolutions-prek">Pre-K through 3</a></li>
        <li><a href="#resolutions-4"   >Grades 4 through 6</a></li>
      </ul>
      <li><a href="#parent"     >Parent Engagement</a></li>
      <ul>
        <li><a href="#parent-prek">Pre-K through 3</a></li>
        <li><a href="#parent-4"   >Grades 4 through 6</a></li>
      </ul>
      <li><a href="#suspension" >Suspension</a></li>
      <ul>
        <li><a href="#suspension-prek">Pre-K through 3</a></li>
        <li><a href="#suspension-4"   >Grades 4 through 6</a></li>
      </ul>
    </ul>
  """)

  div(id='students')
  h2('Students')
  raw(df1.to_html(index=False))
  raw('<img src="d1.png">')

  div(id='overall')
  h2('Overall Discipline Picture')
  raw(df2.to_html(index=False))
  raw('<img src="d2.png">')
  # raw(df3.to_html())
  raw(df4.to_html())
  raw('<img src="d4.png">')
  raw('<img src="d3.png">')
  p('Percentage of students')
  raw(df5.to_html())
  raw('<img src="d5.png">')

  div(id='overall-prek')
  h3('Pre-K through 3')
  raw(df10.to_html(index=False))
  p(raw(df11.to_html(index=False)))
  raw(df12.to_html(na_rep='', float_format=make_zero_empty))
  raw('<img src="d12.png">')
  p('Percentage of students')
  raw(df13.to_html(na_rep='', float_format=make_zero_empty_two_digits))
  raw('<img src="d13.png">')

  div(id='overall-4')
  h3('Grades 4 through 6')
  raw(df20.to_html(index=False))
  p(raw(df21.to_html(index=False)))
  raw(df22.to_html(na_rep='', float_format=make_zero_empty))
  raw('<img src="d22.png">')
  p('Percentage of students')
  raw(df23.to_html(na_rep='', float_format=make_zero_empty_two_digits))
  raw('<img src="d23.png">')

  div(id='reasons')
  h2('Reasons for Referrals')
  div(id='reasons-prek')
  h3('Pre-K through 3')
  raw(df100.to_html(index=False))
  p(raw(df101.to_html(index=False)))
  div(id='reasons-4')
  h3('Grades 4 through 6')
  raw(df110.to_html(index=False))
  p(raw(df111.to_html(index=False)))

  div(id='resolutions')
  h2('Resolutions')
  div(id='resolutions-prek')
  h3('Pre-K through 3')
  raw(df200.to_html(index=False))
  p(raw(df201.to_html()))
  raw('<img src="d202.png">')
  p(raw(df203.to_html(index=False)))
  # raw(df204.to_html(na_rep=""))
  raw(df204.to_html(na_rep="", float_format=make_zero_empty))

  div(id='resolutions-4')
  h3('Grades 4 through 6')
  raw(df210.to_html(index=False))
  p(raw(df211.to_html()))
  raw('<img src="d212.png">')
  p(raw(df213.to_html(index=False)))
  raw(df214.to_html(na_rep="", float_format=make_zero_empty))

  div(id='parent')
  h2('Parent Engagement')
  div(id='parent-prek')
  h3('Pre-K through 3')
  raw(df300.to_html(na_rep='', index=False))
  p(raw(df301.to_html(na_rep='', float_format=make_zero_empty)))

  div(id='parent-4')
  h3('Grades 4 through 6')
  raw(df310.to_html(na_rep='', index=False))
  p(raw(df311.to_html(na_rep='', float_format=make_zero_empty)))

  div(id='suspension')
  h2('Suspension, Expulsion, Exclusion')
  p('Count of referrals:')
  raw(df400.to_html(na_rep='', float_format=make_zero_empty))
  p('Percentage of referrals:')
  p(raw(df401.to_html(na_rep='', float_format=make_zero_empty_two_digits)))
  p('Student count:')
  raw(df402.to_html(na_rep='', float_format=make_zero_empty))
  raw('<img src="d402.png">')
  p('Percentage of students:')
  p(raw(df403.to_html(na_rep='', float_format=make_zero_empty_two_digits)))
  raw('<img src="d403.png">')

  div(id='suspension-prek')
  h3('Pre-K through 3')
  raw(df410.to_html(na_rep='', float_format=make_zero_empty))
  div(id='suspension-4')
  h3('Grades 4 through 6')
  raw(df420.to_html(na_rep='', float_format=make_zero_empty))

  # for path in photos:
  #   div(img(src=path), _class='photo')

with open('index.html', 'w') as f:
  f.write(doc.render())
