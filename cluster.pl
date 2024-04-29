#! env perl

use 5.38.0;
use DBI;

my $dbh = DBI->connect("dbi:SQLite:dbname=ops.sqlite3","","");
my $strsql = <<SQL;
  WITH repeat_referrals AS (
    SELECT RaceEthnicity, count(*) referral_count
    FROM disc
    GROUP BY "w"
  )
  SELECT referral_count, RaceEthnicity, count(*)
  FROM repeat_referrals
  WHERE referral_count > 1
  GROUP BY 1,2;
SQL
my $sth = $dbh->prepare($strsql);
$sth->execute;

my $counts = {};
while (my @row = $sth->fetchrow) {
  if ($row[0] >= 2)  { $counts->{"02 or more"}->{$row[1]} += $row[2] || 0 }
  if ($row[0] >= 5)  { $counts->{"05 or more"}->{$row[1]} += $row[2] || 0 }
  if ($row[0] >= 10) { $counts->{"10 or more"}->{$row[1]} += $row[2] || 0 }
  if ($row[0] >= 20) { $counts->{"20 or more"}->{$row[1]} += $row[2] || 0 }
  if ($row[0] >= 30) { $counts->{"30 or more"}->{$row[1]} += $row[2] || 0 }
}

foreach my $count (keys %$counts) {
  foreach my $race (keys %{$counts->{$count}}) {
    say "$count|$race|" . $counts->{$count}->{$race};
  }
}


