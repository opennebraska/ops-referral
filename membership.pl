#! env perl

use 5.38.0;
use DBI;
use Data::Printer;

my $dbh = DBI->connect("dbi:SQLite:dbname=ops.sqlite3","","") or die $DBI::errstr;
my $strsql = <<SQL;
  DROP TABLE IF EXISTS membership;
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
  SELECT *
  FROM membership_raw
SQL
my $sth1 = $dbh->prepare($strsql) or die $DBI::errstr;
# $strsql = <<SQL;
#   INSERT INTO membership (school, grade, RaceEthnicity, gender, students) VALUES
#   (?, ?, ?, ?, ?)
# SQL
# my $sth2 = $dbh->prepare($strsql) or die $DBI::errstr;

say "hi1";
while (my @row = $sth1->fetchrow) {
  say "hi2";
  p @row;
  #if ($row->{'AA-F'}) {
  #  say $row->{'AA-F'};
  #  $sth2->execute($row->{school}, $row->{grade}, "African American", "F", $row->{'AA-F'});
  #}
}

say "Done";
