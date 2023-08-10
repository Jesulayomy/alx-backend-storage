-- Uses the Compute Average SCore For User Procedure
-- to compute the avertage score for A USER.
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER ||
CREATE PROCEDURE ComputeAverageScoreForUser (user_id INT)
BEGIN
    DECLARE total INT DEFAULT 0;
    DECLARE nb_projects INT DEFAULT 0;

    SELECT SUM(score) INTO total FROM corrections
        WHERE correction.user_id = user_id;
    SELECT COUNT(*) INTO nb_projects FROM corrections
        WHERE corrections.user_id = user_id;

    UPDATE users SET users.average_score = IF(nb_projects = 0, 0, total / nb_projects)
        WHERE users.id = user_id;
END ||
Delimiter ;
