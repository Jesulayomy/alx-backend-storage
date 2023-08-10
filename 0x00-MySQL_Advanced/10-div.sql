-- Create a function that divides two numbers
DROP FUNCTION IF EXISTS SafeDiv;
DELIMITER ||
CREATE FUNCTION SafeDiv (a INT, b INT) RETURNS FLOAT DETERMINISTIC
BEGIN
    DECLARE res FLOAT DEFAULT 0;

    IF b != 0 THEN SET res = a / b;
    END IF;
    RETURN res;
END ||
DELIMITER ;
