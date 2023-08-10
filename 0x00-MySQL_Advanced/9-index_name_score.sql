-- Creeates an index on the names table using the
-- first letter of name and the score
CREATE INDEX isd_name_first_score ON names(name(1), score);
