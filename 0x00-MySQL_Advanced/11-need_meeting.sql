-- Creates a view for students under 80 since last month meeting
DROP VIEW IF EXISTS need_meeting;
CREATE VIEW need_meeting AS SELECT NAME FROM students
WHERE score < 80 AND 
    (last_meeting IS NULL OR last_meeting < SUBDATE(CURRENT_DATE(), INTERVAL 1 MONTH))
