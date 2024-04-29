DROP TABLE IF EXISTS resolution_categories;
CREATE TABLE resolution_categories (
  category STRING,
  resolutionName STRING
);
INSERT INTO resolution_categories (category, resolutionName) VALUES
  ('positive', 'Conflict Resolution'),
  ('positive', 'Consultation with/Referral to a School Psychologist'),
  ('positive', 'Referral to Community Agency'),
  ('positive', 'Referral to Community Counselor'),
  ('positive', 'Parent Guardian Conference'),
  ('positive', 'Parent Guardian Contact Made'),
  ('positive', 'Referred for IEP Update'),
  ('positive', 'Referral for 1st SAT'),
  ('positive', 'Referral for 2nd SAT'),
  ('positive', 'Due Process IEP Conference'),
  ('positive', 'Referral to School Counselor-Admin Intervention'),
  ('positive', 'Referral to School Counselor-Consultation and Refer to Social Worker'),
  ('out_of_class', 'Dismissed from Program'),
  ('out_of_class', 'Emergency Exclusion'),
  ('out_of_class', 'Expelled-Calendar Year'),
  ('out_of_class', 'Expelled –This Semester Only'),
  ('out_of_class', 'Long-Term Suspension (6-19 days)'),
  ('out_of_class', 'PAC Admin Intervention'),
  ('out_of_class', 'PAC Consultation'),
  ('out_of_class', 'Removed from Class/Activity- Admin Intervention'),
  ('out_of_class', 'Removed from Class/Activity-Consultation'),
  ('out_of_class', 'Student Success Center'),
  ('out_of_class', 'Suspended Short-Term (1-5 Days)');

SELECT rc.category, rc.resolutionName, count(*)
FROM resolution_categories rc
LEFT OUTER JOIN disc ON (rc.resolutionName = disc.resolutionName)
GROUP BY 1,2;
