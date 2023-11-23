import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
load_dotenv()

mysql_config = {
    'user': os.getenv("mysql_user"),
    'password': os.getenv("mysql_password"),
    'host': os.getenv("mysql_host"),
    'database': os.getenv("mysql_database"),
    'raise_on_warnings': True
    }

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

DB_NAME = 'legion_td_tool'

TABLES = {}
TABLES['MATCH_DATA'] = (
    "CREATE TABLE `MATCH_DATA` ("
    "  `BUILD_ID` int(11) NOT NULL AUTO_INCREMENT,"
    "  `GAME_ID` varchar(50) NOT NULL,"
    "  `GAME_VERSION` varchar(50) NOT NULL,"
    "  `GAME_DATE` varchar(50) NOT NULL,"
    "  `PLAYER_LEGION` varchar(20) NOT NULL,"
    "  `PLAYER_BUILDPERWAVE` varchar(255) NOT NULL,"
    "  `PLAYER_MERCSRECEIVED` varchar(255) NOT NULL,"
    "  `PLAYER_LEAKSPERWAVE` varchar(255) NOT NULL,"
    "  PRIMARY KEY (`emp_no`)"
    ") ENGINE=InnoDB")

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()