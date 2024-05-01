import mysql.connector

# Set connection
cnn = mysql.connector.connect(
  host="localhost",
  user="root",
  database='covid'
)

cur = cnn.cursor()

# Number of deaths
cur.execute("SELECT COUNT(*) FROM deaths")
row = cur.fetchone()
print("Count deaths: {0}".format(row[0]))

# Number of vaccinations
cur.execute("SELECT COUNT(*) FROM vaccinations")
row = cur.fetchone()
print("Count vaccinations: {0}".format(row[0]))

# Number of vaccinations
cur.execute("SELECT continent, COUNT(continent) AS vaccinations FROM vaccinations GROUP BY continent")
for row in cur.fetchall():
    print("Vaccinations in {0}: {1}".format(row[0], row[1]))
