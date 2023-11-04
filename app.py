"""
    App Module Docstrings

    This module contains the main flask application
    and socketio instance.

    Functions:
        home: renders home.html
"""

import random
from string import ascii_uppercase
from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, send

app = Flask(__name__)
app.config["SECRET_KEY"] = "generatelater"
socketio = SocketIO(app) # create socketio instance

rooms = {}

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break

    return code

@app.route("/", methods=["GET", "POST"])
def home():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)
        
        if not name: # if name is empty
            return render_template("home.html", error="Please enter a name.", code=code, name=name) #passing an error variable that will be accessed in html page
        if join and not code: # If they attempt to join a room without a code (problem)
            return render_template("home.html", error="Please enter a code to join a room.", code=code, name=name)
        
        room = code
        if create != False: # if they are creating a room
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms: # if they are joining a room that doesn't exist
            return render_template("home.html", error=f"Room {code} does not exist.", code=code, name=name)

        # temporary data storage. we want to keep track of the room and name
        # stores data between refreshes
        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html")

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))
    
    return render_template("room.html")

@socketio.on("connect")
def connect(auth): # auth is used for authentication but is not currently used


if __name__ == "__main__":
    socketio.run(app, debug=True)