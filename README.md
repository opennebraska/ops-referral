# Omaha Public Schools Referral (Disciplinary) Data Analysis

This repository does not contain the data, only all our source code for processing
the data. The data is not included in this repository due to privacy concerns.

Feel free to [create an Issue](https://github.com/opennebraska/ops-referral/issues) in this
respository to request the source data (we'll put you in contact with our source), and/or
if you find any errors, or have any questions, about our data processing.

The remainder of this document intends to show all the recreation steps for running the
analysis we performed, from scratch (.xlsx). Hopefully this work is useful for future
years of updated data.

## Step 1: Turn .xlsx files into a SQLite database

We don't have Microsoft Excel, so can't natively attempt a CSV export of the spreadsheets.
We work from macOS, and Numbers.app CSV export is broken: it drops the time portion out of
datetime fields, regardless of how we format them in Numbers.app. So we're going to use Python
Pandas to export .xlsx into SQLite. Locally we have a bunch of Pythons, and Pandas won't
install, so let's use Docker:

    Dockerfile
    xlsx_to_sqlite.py

    docker build . -t pandas
    docker run -it --mount type=bind,source="$(pwd)",target=/home/data pandas

Now we have a SQLite database containing sheet 1 of "OPS Referral Data 2018-2019.xlsx".

It also contains sheet 1 of "SchoolLevel_RaceGenderGradeMembership_1718to1920.xlsx", because
at the end of the list of questions posed we need enrollment statistics. For that dataset, we've
had Pandas strip a bunch of human-friendly labelling out of the data before export to SQLite.

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

sqlite> .schema membership_raw
CREATE TABLE IF NOT EXISTS "membership_raw" (
"index" INTEGER,
  "school" TEXT,
  "grade" TEXT,
  "AA-F" INTEGER,
  "AA-M" INTEGER,
  "A-F" INTEGER,
  "A-M" INTEGER,
  "H-F" INTEGER,
  "H-M" INTEGER,
  "MR-F" INTEGER,
  "MR-M" INTEGER,
  "NA-F" INTEGER,
  "NA-M" INTEGER,
  "PA-F" INTEGER,
  "PA-M" INTEGER,
  "W-F" INTEGER,
  "W-M" INTEGER
);
CREATE INDEX "ix_membership_raw_index"ON "membership_raw" ("index");

sqlite> select count(*) from membership_raw;
678



```
