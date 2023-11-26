#!/bin/python3
from flask import Flask
from os import getenv

PORT = getenv("NOMAD_PORT_web", 8080)

app = Flask(__name__)
    

@app.route("/")
@app.route("/index.html")
def index():
    return app.send_static_file("index.html")

# Run it all
if __name__ == "__main__":
    app.run("0.0.0.0", PORT)