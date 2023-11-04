"""
    Chat Room Module Docstrings

    Description:
        This module is the main module for the chat room application. 
        It handles the routing and socketio events.

    Functions:
        generate_unique_code(length)
        home()
        room()
        message(data)
        connect(auth)
        disconnect()
"""

import random
from string import ascii_uppercase
from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = "generatelater"
socketio = SocketIO(app) # create socketio instance

rooms = {}

def generate_unique_code(length):
    """
    Generate a unique code of a specified length.

    This function generates a random code consisting of uppercase letters from 'A' to 'Z'
    and returns it. The generated code is guaranteed to be unique within the current
    context (e.g., within a list of existing codes). The function continues generating
    codes until it finds one that is not already present in the 'rooms' list.

    Args:
        length (int): The length of the unique code to generate.

    Returns:
        str: A unique code of the specified length, consisting of uppercase letters.

    Note:
        The uniqueness of the generated code is determined by checking if it already exists
        in the 'rooms' list. To ensure uniqueness, make sure to provide a unique context,
        such as a list of existing codes.
    """
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break

    return code

@app.route("/", methods=["POST", "GET"])
def home():
    """
    Handle the home page and form submissions.

    This function manages the home page, where users can enter their name and either
    create a new chat room or join an existing one. It handles user inputs, creates new
    chat rooms with unique codes, and redirects users to the chat room.

    Returns:
        If the request method is POST and the form data is valid, the function redirects
        the user to the chat room. Otherwise, it renders the home page template.
    """
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name)

        if join is not False and not code:
            return render_template("home.html", error="Please enter a room code.",
                                   code=code, name=name)

        current_room = session.get("room")
        current_room = code
        if create is not False:
            current_room = generate_unique_code(4)
            rooms[current_room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist.", code=code, name=name)

        session["room"] = current_room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html")

@app.route("/room")
def room():
    """
    Render the chat room page.

    This function renders the chat room page if the user is part of a valid chat room
    session. It ensures that the user has a valid room code and a name and redirects
    them to the home page if the session is not valid.

    Returns:
        If the user's session is valid, the chat room page is rendered. Otherwise, the
        user is redirected to the home page.
    """
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])

@socketio.on("message")
def message(data):
    """
    Handle incoming chat messages.

    This function is an event handler for incoming chat messages. It takes the message
    data, adds the sender's name, and broadcasts the message to all participants in
    the chat room. It also logs the message in the chat room's message history.

    Args:
        data (dict): A dictionary containing the message data with a 'data' key.

    Note:
        The message is broadcast to all participants in the chat room.
    """
    room = session.get("room")
    if room not in rooms:
        return

    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def connect(auth):
    """
    Handle user connection to a chat room.

    This function is called when a user connects to a chat room. It checks the user's
    session for room and name information, validates the session, and adds the user to
    the chat room. It also logs the user's entry in the chat room.

    Args:
        auth (bool): Authentication status (not used in this function).

    Note:
        The user is added to the chat room, and an entry is logged.
    """
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return

    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    """
    Handle user disconnection from a chat room.

    This function is called when a user disconnects from a chat room. It removes the user
    from the room, updates the room's member count, and logs the user's departure.

    Note:
        The user is removed from the chat room, and an exit message is logged. If the
        member count of the room becomes zero, the room is deleted.
    """
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]

    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")


if __name__ == "__main__":
    socketio.run(app, debug=True)
