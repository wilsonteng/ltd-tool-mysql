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
from pathlib import Path

load_dotenv()
ltd_api_key = os.getenv("ltd_api_key")
mysql_config = {
    'user': os.getenv("mysql_user"),
    'password': os.getenv("mysql_password"),
    'host': os.getenv("mysql_host"),
    'database': os.getenv("mysql_database"),
    'raise_on_warnings': True
    }

def connect_to_mysql(config, attempts=3, delay=2):
    attempt = 1

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

def make_api_request(offset : int, queuetype : str) -> list:
    """
    Makes the API request to Legion TD API
    Returns a dictionary containing the data from api call
    """

    headers = {'x-api-key': ltd_api_key, 'accept': 'application/json'}

    URL = f"""{ltd_api_key}/games?limit={limit}&offset={offset}&sortBy=date&sortDirection=1&includeDetails=true&countResults=false&queueType={queuetype}"""

    r = requests.get(URL, headers=headers)
    if not r.ok:
        print(r, "Response not OK")
        return False
    
    print(f"Retrieving data for {offset} to {offset + int(limit)} of {limit * end} for queueType {queuetype}. Status Code: {r.status_code}")

    return r.text

def check_if_data_useful(input_data) -> bool:
    """
    Checks if this particular build is a pro leak
    Looking for groups of waves that leak less than 4, 4, 7 on waves 1, 2, 3
    """
    if len(input_data) < 3:
        return False

    if (0 < len(input_data[0]) < 4 and
        0 < len(input_data[1]) < 4 and
        0 < len(input_data[2]) < 7):
            print(input_data)
            return True

    return False

def clean_data(raw_data : str) -> list:
    """
    Takes in entire api return in string format.
    Drops columns from both the outer match dictionary and the nested playersData dictionary
    Returns the updated dictionary
    """

    number_of_waves_to_keep = 3
    data_dict = raw_data
    new_list = []

    for game in data_dict:
        for player in game["playersData"]:
            if check_if_data_useful(player["leaksPerWave"]):
                # creating a new dictionary with only the data we need
                player_dict = {}
                player_dict["id"] = game["_id"]
                player_dict["version"] = game["version"]
                player_dict["date"] = game["date"]
                player_dict["legion"] = player["legion"]
                player_dict["buildPerWave"] = player["buildPerWave"][:3]
                player_dict["mercenariesReceivedPerWave"] = player["mercenariesReceivedPerWave"][:3]
                player_dict["leaksPerWave"] = player["leaksPerWave"][:3]

                new_list.append(player_dict)

    return new_list

with open("/home/wilson/git/legiontd_tool/data/json_data_20231113-092359.json", "r") as f:
    json_data = json.loads(f.read())

clean_data(json_data)

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

#cnx = connect_to_mysql(mysql_config, attempts=3, delay=2)
#print(cnx)


# Close mysql connection

def main():
    
    big_array = [] # make one big array before inserting into sql
    start, end = 0, 2 #1000 x 50 is the max per day
    limit = 50

    for i in range(start, end):
        offset = i * int(limit)
        data_normal = make_api_request(offset, "Normal")
        data_classic = make_api_request(offset, "Classic")
        if not data_normal or not data_classic: 
            print("Error!")
            break # break if bad http request so big_array still gets written
        big_array.extend(clean_data(data_normal))
        big_array.extend(clean_data(data_classic))
