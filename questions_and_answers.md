# Questions and Answers

2018-19 School Year

## Overall Discipline Picture:

### 1) Total number of referrals for Pre-K through 3.

```
SELECT count(*)
FROM disc
WHERE Grade IN ('PK', 'KG', 1, 2, 3);
19,933
```

### 2) Total number of referral for Pre-K through 3 by race.

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

### 3) Total number of 4th through 6 students referred.

```
SELECT count(DISTINCT w)
FROM disc
WHERE Grade IN (4, 5, 6);

3754
```

### 4) Total number of 4th through 6 students referred by race.

```
SELECT RaceEthnicity, count(DISTINCT w)
FROM disc
WHERE Grade IN (4, 5, 6)
GROUP BY 1;

African American|1687
Asian|93
Hispanic|873
Multi Racial|277
Native American|30
Pacific Islander|7
White|787
```

### 5) Total number of repeat of referrals by race (2 or more, 5 or more, 10 or more, 20 or more, 30 or more). 

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

## Reasons for Referrals:

### 1) Top 10 Reasons Pre-K through 3rd grade students received referral.

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

### 2) Top 10 Reasons 4th through 6th grade students received referral.

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

### 3) Top 10 Reasons Pre-K through 3rd grade students received referral by race.

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

### 4) Top 10 Reasons 4th through 6th grade students received referral by race.

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

## Resolutions:  

**Positive Resolutions:** Conflict Resolution, Consultation with/Referral to a School Psychologist, Referral to Community Agency, Referral to Community Counselor,  Parent Guardian Conference, Parent Guardian Contact Made, Referred for IEP Update, Referral for 1st SAT, Referral for 2nd SAT, Due Process IEP Conference, Referral to School Counselor-Admin Intervention, Referral to School Counselor-Consultation and Refer to Social Worker.

**Out-of-Class Resolutions:** Dismissed from Program, Emergency Exclusion, Expelled-Calendar Year, Expelled –This Semester Only, Long-Term Suspension (6-19 days), PAC Admin Intervention, PAC Consultation, Removed from Class/Activity- Admin Intervention, Removed from Class/Activity-Consultation, Student Success Center, Suspended Short-Term (1-5 Days).

One time database table load & bad data cleanup:

```
sqlite3 ops.sqlite3 < resolution_categories.sql

Applied to Other Action|other|9495
Assigned to Saturday School|other|118
Board Appeal Requested|other|1
Board Decision-Hearing Decision Overturned-Reinstated|other|1
Board Decision-Hearing Decision Upheld|other|1
Changed Class/Schedule|other|233
Conference with Student|other|15704
Conference with Student and Teacher|other|1130
Confiscation of Contraband|other|83
Confiscation of Electronic Device|other|1380
Conflict Resolution|positive|681
Consultation with/Referral to Gang Interventionist|other|16
Consultation with/Referral to School Psychologist|positive|15
Detention Assigned|other|15435
Dismissed from Program|out_of_class|38
Due Process 504 Conference|other|11
Due Process IEP Conference|positive|259
Emergency Exclusion|out_of_class|20
Expelled-Calendar Year|out_of_class|7
Expelled-This Semester Only|out_of_class|408
Hearing Request Withdrawn|other|1
Hearing-Long-Term Suspension|other|1
Hearing-No Show|other|2
Hearing-Reassignment to Another School|other|13
Hearing-Recommendation Upheld|other|6
Hearing-Reinstate to School|other|4
Late School|other|1149
Law Enforcement Contacted|other|11
Long-Term Suspension (6-19 days)|out_of_class|340
Loss of School Privileges|other|2158
Mentoring|other|81
No Action Taken|other|1966
PAC - Admin Intervention|out_of_class|6041
PAC - Consultation|out_of_class|12167
Parent/Guardian Conference|positive|2124
Parent/Guardian Contact Made|positive|8145
Reassignment Recommendation Overturned (OSCFE Only)|other|12
Reassignment Recommendation Upheld (OSCFE Only)|other|67
Recommended Reassignment|other|91
Refer to Social Worker|other|139
Referral for 1st SAT|positive|1
Referral for 2nd SAT|positive|1
Referral to Community Agency|positive|80
Referral to Community Counselor|positive|84
Referral to School Counselor-Admin Intervention|positive|1
Referral to School Counselor-Consultation and Refer to Social Worker|positive|1
Referred for IEP Update|positive|178
Referred for/1st SAT|other|156
Referred for/2nd SAT|other|39
Referred for/3rd SAT|other|4
Referred to SSL|other|88
Referred to School Counselor - Admin Intervention|other|436
Referred to School Counselor - Consultation|other|293
Removed from Class/Activity - Admin Intervention|out_of_class|6139
Removed from Class/Activity - Consultation|out_of_class|5845
Request for Hearing (Hearing Office Only)|other|3
Restitution|other|132
School/Community Service|other|71
Secondary Transition Program|other|52
Student Success Center|out_of_class|13242
Substance Abuse Screening|other|21
Suspended Short-Term (1-5 Days)|out_of_class|13332
Suspended from Bus/Van|other|208
Suspension from co-curricular activity|other|27
Threat Assessment|other|111
```

### 1) What % of all PK-3 grader referrals resulting in positive resolutions.

```
SELECT count(*)
FROM disc
JOIN resolution_categories rc ON (disc.resolutionName = rc.resolutionName)
WHERE rc.category = 'positive'
AND Grade IN ('PK', 'KG', 1, 2, 3);
2568

SELECT count(*)
FROM disc
WHERE Grade IN ('PK', 'KG', 1, 2, 3);
19,933

12.88%
```

### 2) What % of all PK-3 grader referrals resulting in positive resolutions by race.

```
./by_race2.pl --grades "'PK', 'KG', 1, 2, 3" --category positive
African American|1339|10652|12.57
Asian|31|237|13.08
Hispanic|350|2307|15.17
Multi Racial|232|1966|11.80
Native American|33|146|22.60
Pacific Islander|2|16|12.50
White|581|4609|12.61
```

### 3) What % of all PK-3 grader referrals resulting in out-of-class or other resolutions.

```
SELECT category, count(*)
FROM disc
JOIN resolution_categories rc ON (disc.resolutionName = rc.resolutionName)
WHERE Grade IN ('PK', 'KG', 1, 2, 3)
GROUP BY 1;

other|3385
out_of_class|13351
positive|2568

SELECT count(*)
FROM disc
WHERE Grade IN ('PK', 'KG', 1, 2, 3);

19933

other:        16.98%
out_of_class: 66.98%
positive:     12.88%
```

### 4) What % of all PK-3 grader referrals resulting in out-of-class or other resolutions by race.

```
./by_race2.pl --grades "'PK', 'KG', 1, 2, 3" --category out_of_class
African American|7211|10652|67.70
Asian|159|237|67.09
Hispanic|1535|2307|66.54
Multi Racial|1351|1966|68.72
Native American|71|146|48.63
Pacific Islander|11|16|68.75
White|3013|4609|65.37

./by_race2.pl --grades "'PK', 'KG', 1, 2, 3" --category other
African American|1696|10652|15.92
Asian|34|237|14.35
Hispanic|383|2307|16.60
Multi Racial|335|1966|17.04
Native American|38|146|26.03
Pacific Islander|2|16|12.50
White|897|4609|19.46
```

Sanity check: Show all Pacific Islanders:

```
SELECT disc.resolutionName, category
FROM disc
LEFT OUTER JOIN resolution_categories rc ON (disc.resolutionName = rc.resolutionName)
WHERE Grade IN ('PK', 'KG', 1, 2, 3)
AND RaceEthnicity = 'Pacific Islander';
```

Oh... ya, sometimes in our original .xlsx data `resolutionName` is NULL. So that explains
why sometimes resolutions aren't `postitive` nor `out_of_class` nor `other`. So apparently
this is a feature, not a bug, given our original data source.

### 5) Number of all PK-3 grader referrals resulting in each of these: a. referrals to counselors, b. referrals to social workers and c. referral/consult with school psychologist.

```
SELECT resolutionName, count(*)
FROM disc
WHERE Grade IN ('PK', 'KG', 1, 2, 3)
AND resolutionName like '%referral%'
COLLATE NOCASE
GROUP BY 1;

Consultation with/Referral to School Psychologist|7
Referral to Community Agency|3
Referral to Community Counselor|1
```

### 6) Number of all PK-3 grader referrals resulting in each of these: a. referrals to counselors, b. referrals to social workers and c. referral/consult with school psychologist by race.

```
SELECT resolutionName, raceEthnicity, count(*)
FROM disc
WHERE Grade IN ('PK', 'KG', 1, 2, 3)
AND resolutionName like '%referral%'
COLLATE NOCASE
GROUP BY 1, 2;

Consultation with/Referral to School Psychologist|African American|3
Consultation with/Referral to School Psychologist|Hispanic|1
Consultation with/Referral to School Psychologist|Native American|1
Consultation with/Referral to School Psychologist|White|2
Referral to Community Agency|African American|1
Referral to Community Agency|Multi Racial|1
Referral to Community Agency|White|1
Referral to Community Counselor|African American|1
```

## Parent Engagement:

### 1) Number of all PK-3 grader referrals resulting in parent contacts.

```
SELECT resolutionName, count(*)
FROM disc
WHERE Grade IN ('PK', 'KG', 1, 2, 3)
AND resolutionName like '%parent%'
COLLATE NOCASE
GROUP BY 1;

Parent/Guardian Conference|407
Parent/Guardian Contact Made|2063
```

### 2) Number of all PK-3 grader referrals resulting in parent contacts by race.

```
SELECT resolutionName, raceEthnicity, count(*)
FROM disc
WHERE Grade IN ('PK', 'KG', 1, 2, 3)
AND resolutionName like '%parent%'
COLLATE NOCASE
GROUP BY 1, 2;

Parent/Guardian Conference|African American|218
Parent/Guardian Conference|Asian|3
Parent/Guardian Conference|Hispanic|52
Parent/Guardian Conference|Multi Racial|31
Parent/Guardian Conference|Native American|4
Parent/Guardian Conference|Pacific Islander|2
Parent/Guardian Conference|White|97
Parent/Guardian Contact Made|African American|1079
Parent/Guardian Contact Made|Asian|24
Parent/Guardian Contact Made|Hispanic|290
Parent/Guardian Contact Made|Multi Racial|192
Parent/Guardian Contact Made|Native American|27
Parent/Guardian Contact Made|White|451
```

### 3) Number of all PK-3 grader referrals resulting in parent conferences.

See #1 above.

### 4) Number of all PK-3 grader referrals resulting in parent conference by race.

See #2 above.

## Suspensions

### 1) What % of referrals resulting in short-term and long-term suspensions.

```
SELECT count(*) FROM disc;

122758

SELECT resolutionName, count(*),
  round(count(*) * 1.0 / 122758 * 100, 2)  -- * 1.0 forces int -> float
FROM disc
WHERE resolutionName like '%suspen%'
COLLATE NOCASE
GROUP BY 1;

Hearing-Long-Term Suspension|1|0.0
Long-Term Suspension (6-19 days)|340|0.28
Suspended Short-Term (1-5 Days)|13332|10.86
Suspended from Bus/Van|208|0.17
Suspension from co-curricular activity|27|0.02
```

### 2) What % of referrals resulting in short-term and long-term suspensions by race.

```
WITH suspensions_by_race AS (
  SELECT RaceEthnicity, count(*) cnt_sus
  FROM disc
  WHERE resolutionName like '%suspen%'
  COLLATE NOCASE
  GROUP BY 1
)
SELECT disc.RaceEthnicity, cnt_sus, count(*), round(cnt_sus * 1.0 / count(*) * 100, 2) 
FROM disc
JOIN suspensions_by_race ON (disc.RaceEthnicity = suspensions_by_race.RaceEthnicity)
GROUP BY 1;

African American|7437|66990|11.1
Asian|164|1369|11.98
Hispanic|3007|24687|12.18
Multi Racial|898|8680|10.35
Native American|143|1311|10.91
Pacific Islander|18|196|9.18
White|2241|19525|11.48
```

### 3) Total number of repeat of suspensions by race (1+ times, 2 + times, 3 + times, 5 + times, 8 + times by race).  (See attached example of graph chart would like with this data.)

```
./cluster2.pl | sort
1+ times|African American|2776
1+ times|Asian|94
1+ times|Hispanic|1385
1+ times|Multi Racial|393
1+ times|Native American|73
1+ times|Pacific Islander|7
1+ times|White|964
2+ times|African American|1458
2+ times|Asian|32
2+ times|Hispanic|573
2+ times|Multi Racial|195
2+ times|Native American|32
2+ times|Pacific Islander|5
2+ times|White|438
3+ times|African American|940
3+ times|Asian|15
3+ times|Hispanic|320
3+ times|Multi Racial|109
3+ times|Native American|18
3+ times|Pacific Islander|3
3+ times|White|253
5+ times|African American|452
5+ times|Asian|5
5+ times|Hispanic|143
5+ times|Multi Racial|39
5+ times|Native American|4
5+ times|Pacific Islander|1
5+ times|White|117
8+ times|African American|180
8+ times|Asian|1
8+ times|Hispanic|52
8+ times|Multi Racial|15
8+ times|Native American|2
8+ times|White|37
```

Sanity check: 8+ times Native American:

```
SELECT w, count(*)
FROM disc
WHERE raceEthnicity = 'Native American'
AND resolutionName like '%suspen%'
COLLATE NOCASE
GROUP BY "w"
ORDER BY 2 DESC;
```

Yup, found 2 students at 8+: One at 8 suspensions, one at 9.

## Disproportionality

### 1) Total number of PK through 3rd graders.

```
SELECT sum(students)
FROM membership
WHERE grade IN ('PK', 'KG', 1, 2, 3);

17,801
```

### 2) Total number of PK through 3rd grade students by race. 

```
SELECT raceEthnicity, sum(students)
FROM membership
WHERE grade IN ('PK', 'KG', 1, 2, 3)
GROUP BY 1;

African American|4089
Asian|1348
Hispanic|6186
Multi Racial|1142
Native American|133
Pacific Islander|27
White|4876
```

### 3) PK through 3rd graders disaggregated by race. (Pie Chart)

I'm not sure what "disaggregated" means. redundant?

### 4) What % of PK through 3rd grade students received discipline referrals by race? (Pie Chart)

```
WITH students_referred AS (
  SELECT raceEthnicity, count(DISTINCT w) referral_count
  FROM disc
  WHERE grade IN ('PK', 'KG', 1, 2, 3)
  GROUP BY raceEthnicity
),
all_students AS (
  SELECT raceEthnicity, sum(students) sum_students
  FROM membership
  WHERE grade IN ('PK', 'KG', 1, 2, 3)
  GROUP BY 1
)
SELECT
  students_referred.raceEthnicity, students_referred.referral_count, all_students.sum_students,
  ROUND(students_referred.referral_count * 1.0 / all_students.sum_students * 100, 2)
FROM students_referred
JOIN all_students ON (students_referred.raceEthnicity = all_students.raceEthnicity);

African American|1350|4089|33.02
Asian|103|1348|7.64
Hispanic|551|6186|8.91
Multi Racial|291|1142|25.48
Native American|23|133|17.29
Pacific Islander|4|27|14.81
White|768|4876|15.75
```

Sanity check that top CTE:

```
SELECT w
FROM disc
WHERE grade IN ('PK', 'KG', 1, 2, 3)
AND raceEthnicity = 'Pacific Islander'
ORDER BY 1;
```

Yes, we see there are 4 unique students.

### 5) What % of PK through 3rd grade students received suspensions by race? (Pie Chart)

```
WITH students_referred AS (
  SELECT raceEthnicity, count(DISTINCT w) referral_count
  FROM disc
  WHERE grade IN ('PK', 'KG', 1, 2, 3)
  AND resolutionName like '%suspen%'
  COLLATE NOCASE
  GROUP BY raceEthnicity
),
all_students AS (
  SELECT raceEthnicity, sum(students) sum_students
  FROM membership
  WHERE grade IN ('PK', 'KG', 1, 2, 3)
  GROUP BY 1
)
SELECT
  students_referred.raceEthnicity, students_referred.referral_count, all_students.sum_students,
  ROUND(students_referred.referral_count * 1.0 / all_students.sum_students * 100, 2)
FROM students_referred
JOIN all_students ON (students_referred.raceEthnicity = all_students.raceEthnicity);

African American|368|4089|9.0
Asian|5|1348|0.37
Hispanic|97|6186|1.57
Multi Racial|70|1142|6.13
Native American|4|133|3.01
White|153|4876|3.14
```
