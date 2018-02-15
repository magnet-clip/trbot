#Installation
##Installing linux packages 

`sudo apt-get install mysql-server python3 git vim`

## Getting code
`git pull https://github.com/magnet-clip/trbot`

## Installing python modules
`python3 -m pip install pony pymysql python-telegram`

## Setting up db

 * Run mysql: `mysql -u root -ppassword`
 * Execute the following script:
 
```sql
CREATE DATABASE DbName;
USE DbName;
SET NAMES utf8;
SET collation_connection = 'utf8_general_ci';
ALTER DATABASE TrCommodities
CHARACTER SET utf8
COLLATE utf8_general_ci;
CREATE USER 'user'@'localhost' IDENTIFIED BY 'user_password';
GRANT ALL PRIVILEGES ON TrCommodities.* TO 'user'@'localhost'
WITH GRANT OPTION;
```

## Configuring
 * Create a copy of sample config: `cp ./config.example.ini ./config.ini`
 * Edit it and set necessary values `vim ./config.ini`


# Running
Execute `nohup python3 ./main.py`
