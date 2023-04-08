import mysql.connector
from configparser import ConfigParser

############################################################
## This file will not work without access to the MySQL    ##
## server. This is a privately maintained databse and is  ##
## available for $2 a month. Contact info@adsb.pro for    ##
## access information orquestions.                        ##
############################################################


# Read the configuration file and load the MySQL.
parser = ConfigParser()
parser.read('config.ini')

# Assign MySql Database Values
dbhost = parser.get('mysql', 'server') # MySQL Host Name
dbuser = parser.get('mysql', 'user') # MySQL Host Name
dbpasswd = parser.get('mysql', 'passwd') # MySQL Host Name
dbdatabase = parser.get('mysql', 'database') # MySQL Host Name

connection = mysql.connector.connect(user=dbuser, password=dbpasswd, host=dbhost, database=dbdatabase)

def model(hex):
    try:

        connection = mysql.connector.connect(user=dbuser, password=dbpasswd, host=dbhost, database=dbdatabase)
        cursor = connection.cursor()
        sql_select_query = """select model from aircraftDatabase where icao24 = %s"""
        # set variable in query
        cursor.execute(sql_select_query, (hex.lower(),))
        # fetch result
        record = cursor.fetchone()

    except mysql.connector.Error as error:
        print("Failed to get record from MySQL table: {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            model1 = record[0]
            return model1

def typecode(hex):
    try:
        global connection
        connection = mysql.connector.connect(user=dbuser, password=dbpasswd, host=dbhost, database=dbdatabase)
        cursor = connection.cursor()
        sql_select_query = """select typecode from aircraftDatabase where icao24 = %s"""
        # set variable in query
        cursor.execute(sql_select_query, (hex.lower(),))
        # fetch result
        record = cursor.fetchone()

    except mysql.connector.Error as error:
        print("Failed to get record from MySQL table: {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            type1 = record[0]
            return type1

def owner(hex):
    try:

        global connection
        connection = mysql.connector.connect(user=dbuser, password=dbpasswd, host=dbhost, database=dbdatabase)
        cursor = connection.cursor()
        sql_select_query = """select owner from aircraftDatabase where icao24 = %s"""
        # set variable in query
        cursor.execute(sql_select_query, (hex.lower(),))
        # fetch result
        record = cursor.fetchone()

    except mysql.connector.Error as error:
        print("Failed to get record from MySQL table: {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            owner1 = record[0]

            return owner1

def myoper(hex):
    try:

        global connection
        connection = mysql.connector.connect(user=dbuser, password=dbpasswd, host=dbhost, database=dbdatabase)
        cursor = connection.cursor()
        sql_select_query = """select operator from aircraftDatabase where icao24 = %s"""
        # set variable in query
        cursor.execute(sql_select_query, (hex.lower(),))
        # fetch result
        record = cursor.fetchone()

    except mysql.connector.Error as error:
        print("Failed to get record from MySQL table: {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            oper1 = record[0]

            return oper1
