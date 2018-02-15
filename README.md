# Telegram bot

`pip install pony pymysql python-telegram`

# Script to create a db

```sql
CREATE DATABASE TrCommodities;
USE TrCommodities;
SET NAMES utf8;
SET collation_connection = 'utf8_general_ci';
ALTER DATABASE TrCommodities
CHARACTER SET utf8
COLLATE utf8_general_ci;
CREATE USER 'rustam'@'localhost' IDENTIFIED BY 'rustam_password';
GRANT ALL PRIVILEGES ON TrCommodities.* TO 'rustam'@'localhost'
WITH GRANT OPTION;
```