#! env perl

use 5.38.0;
use DBI;

my $dbh = DBI->connect("dbi:SQLite:dbname=ops.sqlite3","","");

$dbh->do("DROP TABLE IF EXISTS disc_cluster");
$dbh->do("
  CREATE TABLE disc_cluster (
    referral_count TEXT,
    RaceEthnicity TEXT,
    grade TEXT,
    students INT
  )
");

my $strsql = <<SQL;
  WITH repeat_referrals AS (
    SELECT RaceEthnicity, grade, count(*) referral_count
    FROM disc
    GROUP BY "w"
  )
  SELECT referral_count, RaceEthnicity, grade, count(*)
  FROM repeat_referrals
  WHERE referral_count > 1
  GROUP BY 1, 2, 3;
SQL
my $sth1 = $dbh->prepare($strsql);
$sth1->execute;

$strsql = <<SQL;
  INSERT INTO disc_cluster (referral_count, RaceEthnicity, grade, students)
  VALUES (?, ?, ?, ?)
SQL
my $sth2 = $dbh->prepare($strsql);

my $counts = {};
while (my @row = $sth1->fetchrow) {
  if ($row[0] >= 2)  { $counts->{"02 or more"}->{$row[1]}->{$row[2]} += $row[3] || 0 }
  if ($row[0] >= 5)  { $counts->{"05 or more"}->{$row[1]}->{$row[2]} += $row[3] || 0 }
  if ($row[0] >= 10) { $counts->{"10 or more"}->{$row[1]}->{$row[2]} += $row[3] || 0 }
  if ($row[0] >= 20) { $counts->{"20 or more"}->{$row[1]}->{$row[2]} += $row[3] || 0 }
  if ($row[0] >= 30) { $counts->{"30 or more"}->{$row[1]}->{$row[2]} += $row[3] || 0 }
}

foreach my $count (keys %$counts) {
  foreach my $race (keys %{$counts->{$count}}) {
    foreach my $grade (keys %{$counts->{$count}->{$race}}) {
      say "$count|$race|$grade|" . $counts->{$count}->{$race}->{$grade};
      $sth2->execute($count, $race, $grade, $counts->{$count}->{$race}->{$grade});
    }
  }
}


