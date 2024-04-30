#! env perl

use 5.38.0;
use DBI;

my $dbh = DBI->connect("dbi:SQLite:dbname=ops.sqlite3","","");
my $strsql1 = <<SQL;
  SELECT resolutionName, count(*)
  FROM disc
  WHERE resolutionName like '%suspen%'
  AND RaceEthnicity = ?
  COLLATE NOCASE
  GROUP BY 1;
SQL
my $sth1 = $dbh->prepare($strsql1);

my $strsql2 = <<SQL;
  SELECT count(*)
  FROM disc
  WHERE resolutionName like '%suspen%'
  AND RaceEthnicity = ?
  COLLATE NOCASE;
SQL
my $sth2 = $dbh->prepare($strsql2);

my $positive_by_race = {};
foreach my $race (
  "African American",
  "Asian",
  "Hispanic",
  "Multi Racial",
  "Native American",
  "Pacific Islander",
  "White",
) {
  $sth1->execute($race);
  while (my @row = $sth1->fetchrow) {
    $positive_by_race->{$race}->{$row[0]} = $row[1];
  }
  $sth2->execute($race);
  while (my @row = $sth2->fetchrow) {
    say sprintf("%s|%d|%d|%0.2f", $race, $positive_by_race{$race}, $row[0], $positive_by_race{$race} / $row[0] * 100);
  }
}

