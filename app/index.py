from flask import Flask
import socket
import logging
import os


app = Flask(__name__)
log_file = os.path.join(os.path.dirname(__file__), 'logs', f"Container ID:{socket.gethostname()}")
logging.basicConfig(filename=log_file, level=logging.INFO)


@app.route("/")
def home():
    #Log a message - testing app docker-compose volume(logging)
    logging.info("Received a request to the home route")
    return f"Container ID:{socket.gethostname()}"

if __name__ == "__main__":
    app.run(debug=True)





