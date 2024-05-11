# Data Migration from Oracle to PostgreSQL
### Editor: Juan Herrera, 2024-05-11

[![IPG|Juan Herrera](https://raysonline.in/image/python-Rays.png)](https://github.com/juanjshb/)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://github.com/juanjshb/)

This data migration is a solution for migrating data from an Oracle Database to a PostgreSQL Database

## Usage
This solution is based on Python and have to ways to use it:

### Simple Way: Direct Database Connection (not secure):
This way you have the credentials for the database directly writen in your code. Notice there are 3 files:
- ora_conn.py (Oracle Database Connection File)
- postgres_conn.py (PostgreSQL Database Connection File)
- migration_with_direct_connection.py (Migration Script)

### Hard Way: API Manager (more secure):
This way is for a more secure infraestucture where ypur business have a Credential Manager/API Manager which delivers you the credentials you are going to use. Notice there a file: :
- migration_with_apimanager.py (Migration Script)


## Installation

Data Migration requires [Python](https://python.org/) v3.12.3+ to run.

Install these dependencies to run the script:

```sh
pip install requests
pip install cx_Oracle
pip install psycopg2
```

## Development

Want to contribute? Great!.

First:

```sh
Put a Star to this github repo: https://github.com/juanjshb/Public/
```

Second:

```sh
Clone or Download this project
```

Third and most important:

```sh
Have fun!
```
