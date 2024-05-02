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

# Ummm... not sure how to handle clean start vs. multiple runs for this:
# $dbh->do("DROP TABLE IF EXISTS reasons");
# $dbh->do("
#   CREATE TABLE reasons (
#     grades TEXT,
#     raceEthnicity TEXT,
#     eventName TEXT,
#     occurrences INT
#   )
# ");

my $strsql = <<SQL;
  SELECT RaceEthnicity, eventName, count(*)
  FROM disc
  WHERE Grade IN ($grades)
  AND RaceEthnicity = ?
  GROUP BY 1, 2
  ORDER BY 3 DESC
  LIMIT 10;
SQL
my $sth1 = $dbh->prepare($strsql);

$strsql = <<SQL;
  INSERT INTO reasons (grades, raceEthnicity, eventName, occurrences)
  VALUES (?, ?, ?, ?)
SQL
my $sth2 = $dbh->prepare($strsql);

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
    say join "|", @row;
    $sth2->execute($grades, @row);
  }
}

sub usage {
    say STDERR "Usage: $0 " . '--grades "\'PK\', \'KG\', 1, 2, 3"';
    exit;
}
