#! env perl

use 5.38.0;
use DBI;
use Getopt::Long;

my $grades;
GetOptions("grades=s" => \$grades)  # string
  or usage();

if (not defined $grades) {
  say STDERR "FATAL: Argument 'grades' is mandatory.";
  usage();
}

my $dbh = DBI->connect("dbi:SQLite:dbname=ops.sqlite3","","");
my $strsql1 = <<SQL;
  SELECT count(*)
  FROM disc
  JOIN resolution_categories rc ON (disc.resolutionName = rc.resolutionName)
  WHERE rc.category = 'positive'
  AND Grade IN ($grades)
  AND RaceEthnicity = ?
SQL
my $sth1 = $dbh->prepare($strsql1);

my $strsql2 = <<SQL;
  SELECT count(*)
  FROM disc
  WHERE Grade IN ($grades)
  AND RaceEthnicity = ?
SQL
my $sth2 = $dbh->prepare($strsql2);

my %positive_by_race;
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
    $positive_by_race{$race} = $row[0];
  }
  $sth2->execute($race);
  while (my @row = $sth2->fetchrow) {
    say sprintf("%s|%d|%d|%0.2f", $race, $positive_by_race{$race}, $row[0], $positive_by_race{$race} / $row[0] * 100);
  }
}

sub usage {
    say STDERR "Usage: $0 " . '--grades "\'PK\', \'KG\', 1, 2, 3"';
    exit;
}
