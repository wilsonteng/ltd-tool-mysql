# Attempt mysql connection
import requests
import json
from datetime import date, datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def connect_to_mysql() -> None:
    """
    Attempts to connect to mysql server
    """

def api_request() -> dict:
    """
    Makes the API request to legion TD api
    Returns a dictionary containing the data from api call
    """

def filter_data() -> dict:
    """
    Filters the data for specific parameters. 
    For now looking for groups of waves that leak less than 4, 4, 7 on waves 1,2,3
    """

def shorten_data() -> dict:
    """
    After finding a build of interest, keep only the data we need
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