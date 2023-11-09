# LiveChatRoom

# Testing/Linting
## Our code is thoroughly tested in linting. For testing, our project utilize unit testing and mock testing with PyTest. For linting, our project uses PyLint with every error option enabled. 

# Private Chat Rooms: Anonymous accounts with messages that do not persist. Messages are deleted with websockets and owners of the project have zero access to the texts!
# Direct Messaging: Private, direct messaging that requires user login. Saves messages in database and has disappearing messages feature if users want to delete messages in a certain time frame. Example: messages delete after 10 seconds.

# Encryption: we utilize end to end encryption. Not yet, but we want to. i need to figure out how. 