-- Uses the Compute Average SCore For User Procedure
-- to compute the avertage score for A USER.
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER ||
CREATE PROCEDURE ComputeAverageScoreForUser (user_id INT)
BEGIN
    DECLARE total_sc INT DEFAULT 0;
    DECLARE p_count INT DEFAULT 0;

    SELECT SUM(score) INTO total_sc FROM corrections
        WHERE corrections.user_id = user_id;
    SELECT COUNT(*) INTO p_count FROM corrections
        WHERE corrections.user_id = user_id;

    UPDATE users
        SET users.average_score = IF(p_count = 0, 0, total_sc / p_count)
        WHERE users.id = user_id;
END ||
DELIMITER ;
