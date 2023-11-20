# Attempt mysql connection
import requests
import json
from datetime import date, datetime
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector
import os
import logging
import time

load_dotenv()

ltd_api_key = os.getenv("ltd_api_key")

mysql_config = {
    'user': os.getenv("mysql_user"),
    'password': os.getenv("mysql_password"),
    'host': os.getenv("mysql_host"),
    'database': os.getenv("mysql_database"),
    'raise_on_warnings': True
    }
    
# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Log to console
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

# Also log to a file
file_handler = logging.FileHandler("cpy-errors.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler) 

def connect_to_mysql(config, attempts=3, delay=2):
    attempt = 1
    # Implement a reconnection routine
    while attempt < attempts + 1:
        try:
            return mysql.connector.connect(**config)
        except (mysql.connector.Error, IOError) as err:
            if (attempts is attempt):
              # Attempts to reconnect failed; returning None
                logger.info("Failed to connect, exiting without a connection: %s", err)
                return None
            logger.info(
                "Connection failed: %s. Retrying (%d/%d)...",
                err,
                attempt,
                attempts-1,
            )
            # progressive reconnect delay
            time.sleep(delay ** attempt)
            attempt += 1
    return None

cnx = connect_to_mysql(mysql_config, attempts=3, delay=2)
print(cnx)


def api_request() -> dict:
    """
    Makes the API request to legion TD api
    Returns a dictionary containing the data from api call
    """

def check_if_data_useful() -> bool:
    """
    Checks if this particular build is a pro leak
    Looking for groups of waves that leak less than 4, 4, 7 on waves 1, 2, 3
    """

def shorten_data() -> dict:
    """
    After finding a build of interest, truncate data to only waves 1 to 3.
    """

def write_sql_insert_statement() -> str:
    """
    Formats the data into an SQL insert statement.
    """

def insert_into_mysql():
    """
    Inserts the data into mysql
    """
    # cnx commit


# close cursor


# Close mysql connection