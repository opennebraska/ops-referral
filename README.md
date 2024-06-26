# Omaha Public Schools Referral (Disciplinary) Data Analysis

This repository does not contain the data, only all our source code for processing
the data. The data is not included in this repository due to privacy concerns.

Feel free to [create an Issue](https://github.com/opennebraska/ops-referral/issues) in this
respository to request the source data (we'll put you in contact with our source), and/or
if you find any errors, or have any questions, about our data processing.

The remainder of this document intends to show all the recreation steps for running the
analysis we performed, from scratch (.xlsx). Hopefully this work is useful for future
years of updated data.

## Overview

```mermaid
flowchart TD
  xlsx1-->Dockerfile-xlsx["`Dockerfile-xlsx
    xlsx_to_sqlite.py`"]
  xlsx2-->Dockerfile-xlsx
  Dockerfile-xlsx-->disc[[disc]]
  Dockerfile-xlsx-->membership_raw[[membership_raw]]
  disc<-->resolution_categories.sql
  resolution_categories.sql-->resolution_categories[[resolution_categories]]
  membership_raw-->membership.pl
  membership.pl-->membership[[membership]]
  disc-->cluster.pl
  cluster.pl-->disc_cluster[[disc_cluster]]
  disc-->cluster2.pl
  cluster2.pl-->disc_cluster2[[disc_cluster2]]
  disc-->by_race.pl
  by_race.pl-->reasons[[reasons]]
  subgraph SQLite1 [SQLite]
    disc
    membership_raw
  end
  subgraph SQLite2 [SQLite]
    membership
    disc_cluster
    disc_cluster2
    reasons
    resolution_categories
  end
  SQLite2-->Dockerfile-html["`Dockerfile-html
    generate_website.py`"]
  %% SQLite2-->Dockerfile-html
  Dockerfile-html-->index.html
  Dockerfile-html-->d*.png
```

## Step 1: Turn .xlsx files into a SQLite database

We don't have Microsoft Excel, so can't natively attempt a CSV export of the spreadsheets.
We work from macOS, and Numbers.app CSV export is broken: it drops the time portion out of
datetime fields, regardless of how we format them in Numbers.app. So we're going to use Python
Pandas to export .xlsx into SQLite. Locally we have a bunch of Pythons, and Pandas won't
install, so let's use Docker:

    docker build . --file Dockerfile-xlsx --tag pandas-xlsx
    docker run -it --mount type=bind,source="$(pwd)",target=/home/data pandas-xlsx

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
HS|56     # Head Start. If children are in HS they may next attend PK OR KG 
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
  "PI-F" INTEGER,
  "PI-M" INTEGER,
  "W-F" INTEGER,
  "W-M" INTEGER
);
CREATE INDEX "ix_membership_raw_index"ON "membership_raw" ("index");

sqlite> select count(*) from membership_raw;
678
```

## Step 2: Cleanse bad xlsx data, create membership table

```
./membership.pl

sqlite> select count(*) from membership;
5187

sqlite> SELECT RaceEthnicity, sum(students) FROM membership GROUP BY 1;
African American|13124
Asian|3421
Hispanic|19213
Multi Racial|2868
Native American|444
Pacific Islander|79
White|14031
```

## Step 3: Generate website

    docker build . --file Dockerfile-html --tag pandas-html
    docker run -it --mount type=bind,source="$(pwd)",target=/home/data pandas-html


