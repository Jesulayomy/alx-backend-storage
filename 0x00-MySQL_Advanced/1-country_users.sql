-- Creates tables with special property
-- Default for ENUM is the first enumeration value (US)
DROP TABLE IF EXISTS USERS;
CREATE TABLE IF NOT EXISTS users(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    country CHAR(2) NOT NULL ENUM('US', 'CO', 'TN')
);
