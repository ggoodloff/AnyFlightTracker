import mysql.connector as mysql
from configparser import ConfigParser

# Read the configuration file for this application.
parser = ConfigParser()
parser.read('config.ini')

# Assign MySql Database Values
dbhost = parser.get('mysql', 'server') # MySQL Host Name
dbuser = parser.get('mysql', 'user') # MySQL Host Name
dbpasswd = parser.get('mysql', 'passwd') # MySQL Host Name
dbdatabase = parser.get('mysql', 'database') # MySQL Host Name



hex = "A32F17"

db = mysql.connect(user=dbuser, password=dbpasswd, host=dbhost, database=dbdatabase)

cursor = db.cursor()

## defining the Query
query = "SELECT model,operatoricao,operator FROM aircraftDatabase where icao24=LOWER('%s')" % (hex)

## getting records from the table
cursor.execute(query)

## fetching all records from the 'cursor' object
records = cursor.fetchone()

## Showing the data
#for record in records:
#   print(record)

model = (records[0])
type = (records[1])
owner = (records[2])

print (model)
print (type)
print (owner)
