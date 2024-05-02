#! env perl

use 5.38.0;
use DBI;

my $dbh = DBI->connect("dbi:SQLite:dbname=ops.sqlite3","","");

$dbh->do("DROP TABLE IF EXISTS disc_cluster2");
$dbh->do("
  CREATE TABLE disc_cluster2 (
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
    WHERE (
      resolutionName like '%suspen%' OR
      resolutionName like '%expelled%' OR
      resolutionName like '%emergency%' OR
      resolutionName like '%law enfor%'
    )
    COLLATE NOCASE
    GROUP BY "w"
  )
  SELECT referral_count, RaceEthnicity, grade, count(*)
  FROM repeat_referrals
  GROUP BY 1, 2, 3;
SQL
my $sth1 = $dbh->prepare($strsql);
$sth1->execute;

$strsql = <<SQL;
  INSERT INTO disc_cluster2 (referral_count, RaceEthnicity, grade, students)
  VALUES (?, ?, ?, ?)
SQL
my $sth2 = $dbh->prepare($strsql);

my $counts = {};
while (my @row = $sth1->fetchrow) {
  if ($row[0] >= 1) { $counts->{"1+ times"}->{$row[1]}->{$row[2]} += $row[3] || 0 }
  if ($row[0] >= 2) { $counts->{"2+ times"}->{$row[1]}->{$row[2]} += $row[3] || 0 }
  if ($row[0] >= 3) { $counts->{"3+ times"}->{$row[1]}->{$row[2]} += $row[3] || 0 }
  if ($row[0] >= 5) { $counts->{"5+ times"}->{$row[1]}->{$row[2]} += $row[3] || 0 }
  if ($row[0] >= 8) { $counts->{"8+ times"}->{$row[1]}->{$row[2]} += $row[3] || 0 }
}

foreach my $count (keys %$counts) {
  foreach my $race (keys %{$counts->{$count}}) {
    foreach my $grade (keys %{$counts->{$count}->{$race}}) {
      say "$count|$race|$grade|" . $counts->{$count}->{$race}->{$grade};
      $sth2->execute($count, $race, $grade, $counts->{$count}->{$race}->{$grade});
    }
  }
}


