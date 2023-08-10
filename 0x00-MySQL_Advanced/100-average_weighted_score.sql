-- Creates a computed procedure to calc and store the weighted score
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER ||
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (user_id INT)
BEGIN
    DECLARE total_wg_sc INT DEFAULT 0;
    DECLARE total_wg INT DEFAULT 0;

    SELECT SUM(corrections.score * projects.weight)
        INTO total_wg_sc
        FROM corrections
            INNER JOIN projects
                ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

    SELECT SUM(projects.weight)
        INTO total_wg
        FROM corrections
            INNER JOIN projects
                ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

    IF total_wg = 0 THEN
        UPDATE users
            SET users.average_score = 0
            WHERE users.id = user_id;
    ELSE
        UPDATE users
            SET users.average_score = total_wg_sc / total_wg
            WHERE users.id = user_id;
    END IF;
END ||
DELIMITER ;
