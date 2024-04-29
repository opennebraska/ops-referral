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
