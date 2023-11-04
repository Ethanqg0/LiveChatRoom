"""
    App Module Docstrings

    This module contains the main flask application
    and socketio instance.

    Functions:
        home: renders home.html
"""

import random
from string import ascii_uppercase
from flask import Flask, render_template, request, session, redirect
from flask_socketio import SocketIO, join_room, leave_room, send

app = Flask(__name__)
app.config["SECRET_KEY"] = "generatelater"
socketio = SocketIO(app) # create socketio instance

@app.route("/home", methods=["GET", "POST"])
def home():
    return render_template("home.html")

if __name__ == "__main__":
    socketio.run(app, debug=True)