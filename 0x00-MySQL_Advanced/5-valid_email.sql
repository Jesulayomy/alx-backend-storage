-- validating sql email using the database itself
DROP TRIGGER IF EXISTS check_email;
DELIMITER ||
CREATE TRIGGER check_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF OLD.email != NEW.email THEN
        SET NEW.valid_email = 0;
    ELSE
        SET NEW.valid_email = NEW.valid_email;
    END IF;
END ||
DELIMITER ;
