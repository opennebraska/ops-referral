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

Reasons for Referrals:

1) Top 10 Reasons Pre-K through 3rd grade students received referral.

```
SELECT eventName, count(*)
FROM disc
WHERE Grade IN ('PK', 'KG', 1, 2, 3)
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;

Classroom Disruption/Behavior Disruptive to the School Environment|7671
Insubordination/Non-compliance with behavioral expectations|2225
Disrespectful to Adults/Others|2215
Reckless Behavior|1529
Assault, No Injury|1174
Fighting, Less Serious|747
Assault to Staff|409
Violation of other Defined School Rules|399
No Behavior Event/Documentation|386
Repeated Violations|355
```

2) Top 10 Reasons 4th through 6th grade students received referral.

```
SELECT eventName, count(*)
FROM disc
WHERE Grade IN (4, 5, 6)
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;

Classroom Disruption/Behavior Disruptive to the School Environment|7600
Insubordination/Non-compliance with behavioral expectations|3543
Disrespectful to Adults/Others|3479
No Behavior Event/Documentation|2753
Excessive Tardies/Hall Sweep|1570
Reckless Behavior|1511
Fighting, Less Serious|1275
Assault, No Injury|674
Misuse of Pass/Out of Area|591
Inappropriate Language|591
```

3) Top 10 Reasons Pre-K through 3rd grade students received referral by race.

```
./by_race.pl --grades "'PK', 'KG', 1, 2, 3"
African American|Classroom Disruption/Behavior Disruptive to the School Environment|4140
African American|Insubordination/Non-compliance with behavioral expectations|1200
African American|Disrespectful to Adults/Others|1167
African American|Reckless Behavior|859
African American|Assault, No Injury|608
African American|Fighting, Less Serious|436
African American|Violation of other Defined School Rules|243
African American|Repeated Violations|191
African American|Assault to Staff|188
African American|Assault with Injury (Intentional)|153
Asian|Classroom Disruption/Behavior Disruptive to the School Environment|75
Asian|Disrespectful to Adults/Others|33
Asian|Assault, No Injury|23
Asian|No Behavior Event/Documentation|19
Asian|Reckless Behavior|16
Asian|Bus Misconduct|13
Asian|Insubordination/Non-compliance with behavioral expectations|13
Asian|Fighting, Less Serious|8
Asian|Inappropriate Language|5
Asian|Violation of other Defined School Rules|5
Hispanic|Classroom Disruption/Behavior Disruptive to the School Environment|827
Hispanic|Insubordination/Non-compliance with behavioral expectations|289
Hispanic|Disrespectful to Adults/Others|261
Hispanic|Reckless Behavior|176
Hispanic|Assault, No Injury|127
Hispanic|Fighting, Less Serious|82
Hispanic|No Behavior Event/Documentation|79
Hispanic|Bus Misconduct|62
Hispanic|Inappropriate Language|53
Hispanic|Assault to Staff|47
Multi Racial|Classroom Disruption/Behavior Disruptive to the School Environment|792
Multi Racial|Insubordination/Non-compliance with behavioral expectations|244
Multi Racial|Disrespectful to Adults/Others|194
Multi Racial|Reckless Behavior|122
Multi Racial|Assault, No Injury|99
Multi Racial|Fighting, Less Serious|68
Multi Racial|Assault to Staff|63
Multi Racial|No Behavior Event/Documentation|45
Multi Racial|Violation of other Defined School Rules|39
Multi Racial|Damage to School, Staff, or Student Property|37
Native American|Classroom Disruption/Behavior Disruptive to the School Environment|57
Native American|Insubordination/Non-compliance with behavioral expectations|21
Native American|Disrespectful to Adults/Others|17
Native American|Reckless Behavior|15
Native American|Fighting, Less Serious|12
Native American|Damage to School, Staff, or Student Property|3
Native American|Engaging in Verbal Conflict|3
Native American|Assault, No Injury|2
Native American|Bullying|2
Native American|No Behavior Event/Documentation|2
Pacific Islander|Classroom Disruption/Behavior Disruptive to the School Environment|13
Pacific Islander|Insubordination/Non-compliance with behavioral expectations|2
Pacific Islander|Bullying|1
White|Classroom Disruption/Behavior Disruptive to the School Environment|1767
White|Disrespectful to Adults/Others|543
White|Insubordination/Non-compliance with behavioral expectations|456
White|Reckless Behavior|341
White|Assault, No Injury|315
White|No Behavior Event/Documentation|149
White|Fighting, Less Serious|141
White|Assault to Staff|110
White|Repeated Violations|105
White|Assault with Injury (Intentional)|84
```

4) Top 10 Reasons 4th through 6th grade students received referral by race.

```
./by_race.pl --grades "4,5,6"
African American|Classroom Disruption/Behavior Disruptive to the School Environment|4764
African American|Disrespectful to Adults/Others|2136
African American|Insubordination/Non-compliance with behavioral expectations|2126
African American|No Behavior Event/Documentation|1766
African American|Excessive Tardies/Hall Sweep|935
African American|Reckless Behavior|919
African American|Fighting, Less Serious|741
African American|Engaging in Verbal Conflict|429
African American|Assault, No Injury|393
African American|Misuse of Pass/Out of Area|368
Asian|Classroom Disruption/Behavior Disruptive to the School Environment|67
Asian|Insubordination/Non-compliance with behavioral expectations|44
Asian|Excessive Tardies/Hall Sweep|36
Asian|Disrespectful to Adults/Others|27
Asian|Reckless Behavior|13
Asian|Assault, No Injury|12
Asian|Fighting, Less Serious|11
Asian|Inappropriate Language|10
Asian|No Behavior Event/Documentation|10
Asian|Violation of other Defined School Rules|10
Hispanic|Classroom Disruption/Behavior Disruptive to the School Environment|1041
Hispanic|Disrespectful to Adults/Others|524
Hispanic|Insubordination/Non-compliance with behavioral expectations|460
Hispanic|No Behavior Event/Documentation|382
Hispanic|Excessive Tardies/Hall Sweep|228
Hispanic|Reckless Behavior|223
Hispanic|Fighting, Less Serious|217
Hispanic|Inappropriate Language|129
Hispanic|Assault, No Injury|84
Hispanic|Threats or Intimidation|77
Multi Racial|Classroom Disruption/Behavior Disruptive to the School Environment|599
Multi Racial|Insubordination/Non-compliance with behavioral expectations|304
Multi Racial|Disrespectful to Adults/Others|268
Multi Racial|No Behavior Event/Documentation|211
Multi Racial|Excessive Tardies/Hall Sweep|151
Multi Racial|Reckless Behavior|115
Multi Racial|Fighting, Less Serious|111
Multi Racial|Violation of other Defined School Rules|72
Multi Racial|Misuse of Pass/Out of Area|67
Multi Racial|Assault, No Injury|51
Native American|Classroom Disruption/Behavior Disruptive to the School Environment|73
Native American|Insubordination/Non-compliance with behavioral expectations|26
Native American|No Behavior Event/Documentation|21
Native American|Fighting, Less Serious|20
Native American|Disrespectful to Adults/Others|14
Native American|Excessive Tardies/Hall Sweep|9
Native American|Violation of other Defined School Rules|8
Native American|Misuse of Pass/Out of Area|7
Native American|Damage to School, Staff, or Student Property|6
Native American|Threats or Intimidation|5
Pacific Islander|Classroom Disruption/Behavior Disruptive to the School Environment|23
Pacific Islander|No Behavior Event/Documentation|16
Pacific Islander|Disrespectful to Adults/Others|14
Pacific Islander|Insubordination/Non-compliance with behavioral expectations|13
Pacific Islander|Truancy|13
Pacific Islander|Reckless Behavior|11
Pacific Islander|Fighting, Serious|6
Pacific Islander|Misuse of Pass/Out of Area|6
Pacific Islander|Assault, No Injury|4
Pacific Islander|Excessive Tardies/Hall Sweep|3
White|Classroom Disruption/Behavior Disruptive to the School Environment|1033
White|Insubordination/Non-compliance with behavioral expectations|570
White|Disrespectful to Adults/Others|496
White|No Behavior Event/Documentation|347
White|Reckless Behavior|226
White|Excessive Tardies/Hall Sweep|208
White|Fighting, Less Serious|172
White|Violation of other Defined School Rules|131
White|Assault, No Injury|126
White|Inappropriate Language|102
```

Resolutions:  

Positive Resolutions: Conflict Resolution, Consultation with/Referral to a School Psychologist, Referral to Community Agency, Referral to Community Counselor,  Parent Guardian Conference, Parent Guardian Contact Made, Referred for IEP Update, Referral for 1st SAT, Referral for 2nd SAT, Due Process IEP Conference, Referral to School Counselor-Admin Intervention, Referral to School Counselor-Consultation and Refer to Social Worker.

Out-of-Class Resolutions: Dismissed from Program, Emergency Exclusion, Expelled-Calendar Year, Expelled –This Semester Only, Long-Term Suspension (6-19 days), PAC Admin Intervention, PAC Consultation, Removed from Class/Activity- Admin Intervention, Removed from Class/Activity-Consultation, Student Success Center, Suspended Short-Term (1-5 Days).

One time database table load:

    sqlite3 ops.sqlite3 < resolution_categories.sql

1) What % of all PK-3 grader referrals resulting in positive resolutions.

```
SELECT count(*)
FROM disc
JOIN resolution_categories rc ON (disc.resolutionName = rc.resolutionName)
WHERE rc.category = 'positive'
AND Grade IN ('PK', 'KG', 1, 2, 3);
91

SELECT count(*)
FROM disc
WHERE Grade IN ('PK', 'KG', 1, 2, 3);
19,933

0.46%
```

2) What % of all PK-3 grader referrals resulting in positive resolutions by race.

```
./by_race2.pl --grades "'PK', 'KG', 1, 2, 3" --category positive
African American|39|10652|0.37
Asian|4|237|1.69
Hispanic|7|2307|0.30
Multi Racial|9|1966|0.46
Native American|1|146|0.68
Pacific Islander|0|16|0.00
White|31|4609|0.67
```

3) What % of all PK-3 grader referrals resulting in out-of-class or other resolutions.

```
./by_race2.pl --grades "'PK', 'KG', 1, 2, 3" --category out_of_class
African American|917|10652|8.61
Asian|8|237|3.38
Hispanic|249|2307|10.79
Multi Racial|168|1966|8.55
Native American|8|146|5.48
Pacific Islander|0|16|0.00
White|439|4609|9.52
```




