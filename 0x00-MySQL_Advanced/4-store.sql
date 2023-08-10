-- Trigger to deccrease quantity in a db
DROP TRIGGER IF EXISTS redux;
DELIMITER ||
CREATE TRIGGER redux AFTER INSERT ON orders
FOR EACH ROW
BEGIN
UPDATE items SET quantity =  quantity - NEW.number
WHERE name = NEW.item_name;
END ||
DELIMITER ;
