#! env perl

use 5.38.0;
use DBI;

my $dbh = DBI->connect("dbi:SQLite:dbname=ops.sqlite3","","");
my $strsql = <<SQL;
  WITH repeat_referrals AS (
    SELECT RaceEthnicity, count(*) referral_count
    FROM disc
    WHERE resolutionName like '%suspen%'
    COLLATE NOCASE
    GROUP BY "w"
  )
  SELECT referral_count, RaceEthnicity, count(*)
  FROM repeat_referrals
  GROUP BY 1,2;
SQL
my $sth = $dbh->prepare($strsql);
$sth->execute;

my $counts = {};
while (my @row = $sth->fetchrow) {
  if ($row[0] >= 1) { $counts->{"1+ times"}->{$row[1]} += $row[2] || 0 }
  if ($row[0] >= 2) { $counts->{"2+ times"}->{$row[1]} += $row[2] || 0 }
  if ($row[0] >= 3) { $counts->{"3+ times"}->{$row[1]} += $row[2] || 0 }
  if ($row[0] >= 5) { $counts->{"5+ times"}->{$row[1]} += $row[2] || 0 }
  if ($row[0] >= 8) { $counts->{"8+ times"}->{$row[1]} += $row[2] || 0 }
}

foreach my $count (keys %$counts) {
  foreach my $race (keys %{$counts->{$count}}) {
    say "$count|$race|" . $counts->{$count}->{$race};
  }
}


