
import mysql.connector
import time

connectionstart = time.time()
connection = mysql.connector.connect(
    user="yutongd",
    password="12345",
    host="mysql.metropolia.fi",
    port=3306,
    database="yutongd",
    connection_timeout=60,
    autocommit = True
)
connectedtime = time.time()

def print_connection_time():
    print(f'Connected to the database in {connectedtime - connectionstart} seconds.')

def get_start_time():
    return connectedtime