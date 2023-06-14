from flask import Flask, request, make_response
import socket
import logging
import os
import mysql.connector
from datetime import datetime, timedelta
import time

# init flask
app = Flask(__name__)

# init logging
log_file = os.path.join(os.path.dirname(__file__), 'logs', f"Container ID:{socket.gethostname()}")
logging.basicConfig(filename=log_file, level=logging.INFO)

# db connection - sleep 10 sec to let mysql container to start
time.sleep(10)
# Connect to MySQL
db_connection = mysql.connector.connect(
    user='root',
    password='root',
    host='mysql',
    port='3306',
    database='db'
)

cursor = db_connection.cursor()
if db_connection.is_connected():
    logging.info(f"Container ID:{socket.gethostname()} - Connected to MySQL database!")

# Drop existing tables if they exist
drop_counter_table_query = "DROP TABLE IF EXISTS counter"
drop_access_log_table_query = "DROP TABLE IF EXISTS access_log"
cursor.execute(drop_counter_table_query)
cursor.execute(drop_access_log_table_query)
db_connection.commit()

# Execute CREATE TABLE statements
create_counter_table_query = '''
    CREATE TABLE IF NOT EXISTS counter (
        counter_name VARCHAR(100) NOT NULL,
        counter_value INT NOT NULL DEFAULT 0,
        PRIMARY KEY (counter_name)
    )
'''

create_access_log_table_query = '''
    CREATE TABLE IF NOT EXISTS access_log (
        access_datetime DATETIME NOT NULL,
        client_ip VARCHAR(100) NOT NULL,
        internal_ip VARCHAR(100) NOT NULL
    )
'''

cursor.execute(create_counter_table_query)
cursor.execute(create_access_log_table_query)

# Commit the changes
db_connection.commit()

global_counter = 0
# Insert initial data into the counter table
insert_counter_query = "INSERT INTO counter (counter_name, counter_value) VALUES (%s, %s)"
counter_data = ("global_counter", 0)
try:
    cursor.execute(insert_counter_query, counter_data)
    db_connection.commit()
    logging.info("Inserted initial data into the counter table")
except Exception as e:
    logging.error(f"Error inserting data into the counter table: {str(e)}")

db_connection.commit()

@app.route("/")
def home():
    global global_counter
    # Increment the global counter
    global_counter += 1
    
    # Update the counter table in the database
    update_counter_query = "UPDATE counter SET counter_value = %s WHERE counter_name = %s"
    counter_data = (global_counter, "global_counter")
    cursor.execute(update_counter_query, counter_data)
    db_connection.commit()

    # Log the contents of the counter table
    select_counter_query = "SELECT * FROM counter"
    cursor.execute(select_counter_query)
    counter_rows = cursor.fetchall()
    logging.info("Counter table contents:")
    for row in counter_rows:
        logging.info(row)

    # Insert data into the access_log table
    access_datetime = datetime.now()
    client_ip = request.remote_addr
    internal_ip = socket.gethostbyname(socket.gethostname())
    insert_access_log_query = "INSERT INTO access_log (access_datetime, client_ip, internal_ip) VALUES (%s, %s, %s)"
    access_log_data = (access_datetime, client_ip, internal_ip)
    cursor.execute(insert_access_log_query, access_log_data)
    db_connection.commit()

    # Log the contents of the access_log table
    select_access_log_query = "SELECT * FROM access_log"
    cursor.execute(select_access_log_query)
    access_log_rows = cursor.fetchall()
    logging.info("Access log table contents:")
    for row in access_log_rows:
        logging.info(row)

    # Create a response object
    response = make_response(f"Container ID:{socket.gethostname()}")

    # Set the cookie with the internal IP and expiration time
    response.set_cookie('internal_ip', internal_ip, max_age=300)  # 300 seconds = 5 minutes

    # Log a message - testing app docker-compose volume(logging)
    logging.info("Received a request to the home route")

    return response


if __name__ == "__main__":
    app.run(debug=True)
