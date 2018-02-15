# Installation

## Installing linux packages 

`sudo apt-get install mysql-server python3 git vim`

## Getting code
`git pull https://github.com/magnet-clip/trbot`

## Installing python modules
`python3 -m pip install pony pymysql python-telegram`

## Setting up db

 * Create a copy of sample sql: `cp ./db_create.sample.sql ./db_create.sql`
 * Edit it and replace `DbName`, `user` and `user_password` to desired values
 * Run this script: `mysql -u root -ppassword < ./db_create.sql`
 
## Configuring
 * Create a copy of sample config: `cp ./config.example.ini ./config.ini`
 * Edit it and set necessary values `vim ./config.ini`


# Running
Execute `nohup python3 ./main.py`
