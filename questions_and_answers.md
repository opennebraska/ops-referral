# Questions and Answers

2018-19 School Year

Overall Discipline Picture:

1) Total number of referrals for Pre-K through 3.

```
sqlite3 ops.sqlite3

sqlite> .schema disc
CREATE TABLE IF NOT EXISTS "disc" (
"index" INTEGER,
  "w" INTEGER,
  "EnrSchoolName" TEXT,
  "Grade" TEXT,
  "Gender" TEXT,
  "RaceEthnicity" TEXT,
  "Lunch" TEXT,
  "specialedstatus" TEXT,
  "section504" INTEGER,
  "EventDate" TIMESTAMP,
  "EventID" INTEGER,
  "eventName" TEXT,
  "role" TEXT,
  "resolutionName" TEXT,
  "resolutionEndDate" TIMESTAMP,
  "resolutionEndTimeStamp" TIMESTAMP,
  "resolutionStartDate" TIMESTAMP,
  "resolutionStartTimestamp" TIMESTAMP
);
CREATE INDEX "ix_disc_index"ON "disc" ("index");

sqlite> select count(*) from disc;
122,758

sqlite> select grade, count(*) from disc group by 1 order by 1;
1|4741
10|10238
11|7979
12|3986
2|4914
3|6613
4|6310
5|8645
6|15342
7|20769
8|18257
9|11243
HS|56     # ?
KG|3540   # Kindergarten
PK|125    # Pre-K

SELECT count(*)
FROM disc
WHERE Grade IN ('PK', 'KG', 1, 2, 3);
19,933
```

2) Total number of referral for Pre-K through 3 by race.

```
SELECT RaceEthnicity, count(*)
FROM disc
WHERE Grade IN ('PK', 'KG', 1, 2, 3)
GROUP BY 1;

African American|10652
Asian|237
Hispanic|2307
Multi Racial|1966
Native American|146
Pacific Islander|16
White|4609
```

3) Total number of 4th through 6 students referred.

```
SELECT count(*)
FROM disc
WHERE Grade IN (4, 5, 6);
30,297
```

4) Total number of 4th through 6 students referred by race.

```
SELECT RaceEthnicity, count(*)
FROM disc
WHERE Grade IN (4, 5, 6)
GROUP BY 1;

African American|18451
Asian|306
Hispanic|4291
Multi Racial|2406
Native American|240
Pacific Islander|128
White|4475
```

5) Total number of repeat of referrals by race (2 or more, 5 or more, 10 or more, 20 or more, 30 or more). 

```
✗ perl cluster.pl | sort
02 or more|African American|5177
02 or more|Asian|213
02 or more|Hispanic|2818
02 or more|Multi Racial|784
02 or more|Native American|138
02 or more|Pacific Islander|14
02 or more|White|2151
05 or more|African American|3313
05 or more|Asian|77
05 or more|Hispanic|1410
05 or more|Multi Racial|479
05 or more|Native American|76
05 or more|Pacific Islander|8
05 or more|White|1070
10 or more|African American|2055
10 or more|Asian|30
10 or more|Hispanic|706
10 or more|Multi Racial|284
10 or more|Native American|44
10 or more|Pacific Islander|7
10 or more|White|551
20 or more|African American|1057
20 or more|Asian|6
20 or more|Hispanic|262
20 or more|Multi Racial|123
20 or more|Native American|20
20 or more|Pacific Islander|3
20 or more|White|208
30 or more|African American|557
30 or more|Asian|1
30 or more|Hispanic|118
30 or more|Multi Racial|53
30 or more|Native American|10
30 or more|Pacific Islander|2
30 or more|White|107
```


