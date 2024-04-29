#! env perl

use 5.38.0;
use DBI;

my $dbh = DBI->connect("dbi:SQLite:dbname=ops.sqlite3","","");
my $strsql = <<SQL;
  SELECT RaceEthnicity, eventName, count(*)
  FROM disc
  WHERE Grade IN ('PK', 'KG', 1, 2, 3)
  AND RaceEthnicity = ?
  GROUP BY 1, 2
  ORDER BY 3 DESC
  LIMIT 10;
SQL
my $sth = $dbh->prepare($strsql);

foreach my $race (
  "African American",
  "Asian",
  "Hispanic",
  "Multi Racial",
  "Native American",
  "Pacific Islander",
  "White",
) {
  $sth->execute($race);
  while (my @row = $sth->fetchrow) {
    say join "|", @row;
  }
}

