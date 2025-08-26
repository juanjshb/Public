# B2B Transactions Export Script
[![IPG|Juan Herrera](https://raysonline.in/image/python-Rays.png)](https://github.com/juanjshb/)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://github.com/juanjshb/)

This Python script is an example to integrate PRIME4 to VISA Concur. By retrieving a business transaction data from the database and exports it into a text file and exports it in a format easy to process for another business.

## Usage

### First Way: Using Oracle:
This way you have the credentials for the database directly writen in your code. Notice there is a folder:
- oracle-based ( contains all files for running this process in Oracle)

### Second Way: Using RedShift:
This way is for a more secure infraestucture where ypur business have a Credential Manager/API Manager which delivers you the credentials you are going to use. Notice there a file: :
- redshift-based ( contains all files for running this process in RedShift)

1. **Query Execution:**
   - The script executes a SQL query to retrieve B2B transaction data from the database.
   - The SQL query is defined as a multi-line string in the `query` variable within the script.
   - Modify the query according to your specific requirements.

2. **Exporting Results:**
   - The script exports the query results into a pipe-delimited text file.
   - The output file name is dynamically generated based on the current date and a custom file name.
   - You can specify the custom file name by modifying the `custom_file_name` variable within the script.

3. **Dependencies:**
   - The script relies on the `query.py` module, which contains the `runqry` function for executing SQL queries.
   - Make sure to have the `query.py` module present in the same directory as this script.

4. **Execution:**
   - Run the script using Python 3.
   - Upon execution, the script will execute the SQL query and export the results into a text file in the same directory.

## Example Output File Name:
   - B2B_123456_TRANSACTIONS_20220509.txt

Ensure to have the necessary dependencies installed (`query.py`), and modify the script according to your environment and requirements before execution.


## Installation

Data Migration requires [Python](https://python.org/) v3.12.3+ to run.

Install these dependencies to run the script:

```sh
pip install cx_Oracle
pip install redshift_connector
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

