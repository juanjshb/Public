import mysql.connector

# Set connection
cnn = mysql.connector.connect(
  host="localhost",
  user="root",
  password=""
)

# Get a cursor
cur = cnn.cursor()

# Execute a query
cur.execute("SELECT CURDATE()")
# Fetch one result
row = cur.fetchone()
print("Current date is: {0}".format(row[0]))

# Close connection
cnn.close()