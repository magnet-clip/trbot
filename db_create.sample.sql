CREATE DATABASE DbName;
USE DbName;
SET NAMES utf8;
SET collation_connection = 'utf8_general_ci';
ALTER DATABASE DbName
CHARACTER SET utf8
COLLATE utf8_general_ci;
CREATE USER 'user'@'localhost' IDENTIFIED BY 'user_password';
GRANT ALL PRIVILEGES ON DbName.* TO 'user'@'localhost'
WITH GRANT OPTION;