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

## Features

- Import a HTML file and watch it magically convert to Markdown
- Drag and drop images (requires your Dropbox account be linked)
- Import and save files from GitHub, Dropbox, Google Drive and One Drive
- Drag and drop markdown and HTML files into Dillinger
- Export documents as Markdown, HTML and PDF

Markdown is a lightweight markup language based on the formatting conventions
that people naturally use in email.
As [John Gruber] writes on the [Markdown site][df1]

> The overriding design goal for Markdown's
> formatting syntax is to make it as readable
> as possible. The idea is that a
> Markdown-formatted document should be
> publishable as-is, as plain text, without
> looking like it's been marked up with tags
> or formatting instructions.

This text you see here is *actually- written in Markdown! To get a feel
for Markdown's syntax, type some text into the left window and
watch the results in the right.

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
