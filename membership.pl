#! env perl

# We wouldn't need this program if I could have fingured out how to de-crosstab in Python
# Pandas over in xlsx_to_sqlite.py, but alas...

use 5.38.0;
use DBI;

my $dbh = DBI->connect("dbi:SQLite:dbname=ops.sqlite3","","") or die $DBI::errstr;
my $strsql = <<SQL;
  DROP TABLE IF EXISTS membership
SQL
$dbh->do($strsql) or die $DBI::errstr;
$strsql = <<SQL;
  CREATE TABLE membership (
    "school" TEXT,
    "grade" TEXT,
    "RaceEthnicity" TEXT,
    "gender" TEXT,
    "students" INTEGER
  )
SQL
$dbh->do($strsql) or die $DBI::errstr;

$strsql = <<SQL;
  SELECT * FROM membership_raw
SQL
my $sth1 = $dbh->prepare($strsql) or die $DBI::errstr;
$strsql = <<SQL;
  INSERT INTO membership (school, grade, RaceEthnicity, gender, students) VALUES
  (?, ?, ?, ?, ?)
SQL
my $sth2 = $dbh->prepare($strsql) or die $DBI::errstr;

$sth1->execute() or die $DBI::errstr;
while (my $row = $sth1->fetchrow_hashref) {
  if ($row->{'AA-F'}) { $sth2->execute($row->{school}, $row->{grade}, "African American", "F", $row->{'AA-F'}) }
  if ($row->{'AA-M'}) { $sth2->execute($row->{school}, $row->{grade}, "African American", "M", $row->{'AA-M'}) }
  if ($row->{'A-F'})  { $sth2->execute($row->{school}, $row->{grade}, "Asian",            "F", $row->{'A-F'}) }
  if ($row->{'A-M'})  { $sth2->execute($row->{school}, $row->{grade}, "Asian",            "M", $row->{'A-M'}) }
  if ($row->{'H-F'})  { $sth2->execute($row->{school}, $row->{grade}, "Hispanic",         "F", $row->{'H-F'}) }
  if ($row->{'H-M'})  { $sth2->execute($row->{school}, $row->{grade}, "Hispanic",         "M", $row->{'H-M'}) }
  if ($row->{'MR-F'}) { $sth2->execute($row->{school}, $row->{grade}, "Multi Racial",     "F", $row->{'MR-F'}) }
  if ($row->{'MR-M'}) { $sth2->execute($row->{school}, $row->{grade}, "Multi Racial",     "M", $row->{'MR-M'}) }
  if ($row->{'NA-F'}) { $sth2->execute($row->{school}, $row->{grade}, "Native American",  "F", $row->{'NA-F'}) }
  if ($row->{'NA-M'}) { $sth2->execute($row->{school}, $row->{grade}, "Native American",  "M", $row->{'NA-M'}) }
  if ($row->{'PI-F'}) { $sth2->execute($row->{school}, $row->{grade}, "Pacific Islander", "F", $row->{'PI-F'}) }
  if ($row->{'PI-M'}) { $sth2->execute($row->{school}, $row->{grade}, "Pacific Islander", "M", $row->{'PI-M'}) }
  if ($row->{'W-F'})  { $sth2->execute($row->{school}, $row->{grade}, "White",            "F", $row->{'W-F'}) }
  if ($row->{'W-M'})  { $sth2->execute($row->{school}, $row->{grade}, "White",            "M", $row->{'W-M'}) }
}

say "Done";
