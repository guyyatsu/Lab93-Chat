<<<<<<< HEAD
import socket
import threading
from os import getlogin as username
from datetime import datetime
import inspect
from argparse import ArgumentParser
from json import loads as load
from base64 import b64decode, b64encode
from logging import getLogger, exception
from logging import info as information
from logging import debug as debugging


class client:


    def __init__(self):
        self = self


    def handle_messages(self, connection: socket.socket):
    
        while True:
            try:
                msg = connection.recv(1024)
    
=======
import socket, threading
from glob import glob
import base64
import argparse
from json import loads as load
from logging import getLogger, exception
from logging import debug as debugging
from logging import info as information
from datetime import datetime
import inspect

class Client:
    """Client class"""

    def __init__(self):
        pass

    def handle_messages(self, connection: socket.socket):

        while True:
            try:
                msg = connection.recv(1024)

>>>>>>> 07636e6aebe315c45abde9faed3739284b07eb94
                if msg:
                    print(msg.decode())
                else:
                    connection.close()
                    break

            except Exception as e:
                print(f'Error handling message from server: {e}')
                connection.close()
                break

<<<<<<< HEAD

    def start(self, address, port) -> None:
        """
        """

        # Set up logging.
        getLogger()
    
        _name = inspect.stack()[0][3]
        _time = lambda datetime.timestamp(datetime.now())


        debugging(
            f"{_time}:{_name}:Beginning client connection."
        )

        try:
    
            # Instantiate socket and start connection with server.
            socket_instance = socket.socket(); debugging(
                f"{_time}:{_name}:"
            )

            socket_instance.connect(
                (str(address), int(port))
            )

            # Create a thread in order to handle messages sent by server
            threading.Thread(
                target=handle_messages, 
                args=[socket_instance]
            ).start()
    
            while True:
    
                # Recieve user input as message string.
                message_packet = {
                    "content": input(), 
                    "username": username()
                }
               
    
=======
    def start(self, address, port) -> None:


        try:

            # Instantiate socket and start connection with server
            self.socket_instance = socket.socket()
            self.socket_instance.connect((address, int(port)))

            # Create a thread in order to handle messages sent by server
            threading.Thread(target=self.handle_messages, args=[self.socket_instance]).start()

            while True:

                # Recieve user input as message string.
                message_packet = {"content": input(), "username": username()}
                message_content = message_packet["content"]
                username = message_packet["username"]

>>>>>>> 07636e6aebe315c45abde9faed3739284b07eb94
                # User Commands
                """ User commands allow for actions to be made from chat;
                such as quitting the session or defining a subject for
                a message.  Commands are defined by typing a forward slash
                as the first letter of your message."""
<<<<<<< HEAD
    
                # All commands start with a '/', so check for that.
                if message_packet["content"][0] != "/": pass
                else:
    
                    # The command is the first word in the msg.
                    cmd = message_packet["content"].split(" ")[0]
    
                    # The quit command breaks the loop and
                    # returns control back to the terminal.
                    if cmd == "/quit": break
    
                    # Allows the attachment of a subject line to a msg.
                    if cmd == "/subject":
                        message_packet["subject"] = str(msg.split(" ")[1])
                        message_packet["content"] = str(" ".join(msg.split(" ")[2:-1]))
    
                    # Scan the local network for fellow chat servers.
                    if cmd == "/scan": pass
                        
    
    
                # Convert message packet to ascii string and send to the comms bus.
                socket_instance.send(
=======

                # All commands start with a '/', so check for that.
                if message_packet["content"][0] != "/": pass
                else:

                    # The command is the first word in the msg.
                    cmd = message_packet["content"].split(" ")[0]

                    # The quit command breaks the loop and
                    # returns control back to the terminal.
                    if cmd == "/quit": 
                        break

                    # Allows the attachment of a subject line to a msg.
                    if cmd == "/subject":
                        message_packet["subject"] = str(message_content.split(" ")[1])
                        message_packet["content"] = str(" ".join(message_content.split(" ")[2:-1]))

                    if cmd == "/changename":
                        pass

                # Convert message packet to ascii string
                self.socket_instance.send(
>>>>>>> 07636e6aebe315c45abde9faed3739284b07eb94
                    base64.b64encode(
                        str(message_packet).encode('ascii')
                    )
                )
<<<<<<< HEAD
    
            # Close connection with the server
            socket_instance.close()
    
        except Exception as Error:
            exception(
                f"{_name}:{_time}There was an issue trying to set up the chat client;\n"
                f"{error}"
            ); socket_instance.close()

            return Error


class server:


    def __init__(self):
        """ """
=======

            # Close connection with the server
            self.socket_instance.close()

        except Exception as e:
            print(f'Error connecting to server socket {e}')
            self.socket_instance.close()


class Server:
    """Server class"""
    
    def __init__(self, address="127.0.0.1", port=5190):
        """
        Set up a couple of constants required at runtime.  Here we've got self; but also
        we've got self.address which defines an IP to make the service available on, a self.port
        which narrows down the channel to operate on, and self.connections which enumerates every
        address that has made a valid connection to the instance.
        """
>>>>>>> 07636e6aebe315c45abde9faed3739284b07eb94

        # The classes semblance of identity.
        self             = self

<<<<<<< HEAD
=======
        # An address to host services on.
        self.address     = address

        # A socket to listen out for.
        self.port        = port

>>>>>>> 07636e6aebe315c45abde9faed3739284b07eb94
        # A list of clients connected to this server.
        self.connections = []


    def handle_user_connection(self, connection: socket.socket, address: str) -> None:
        while True:
            try:
                # Recieve client's posted message, up to 4096 bytes.
                msg = connection.recv(4096)
    
                if msg:
                    # TODO: Log client messages to server database.

                    # Convert the msg bytes into a dictionary named message.
<<<<<<< HEAD
                    message = load(b64decode(msg)\
=======
                    message = load(base64.b64decode(msg)\
>>>>>>> 07636e6aebe315c45abde9faed3739284b07eb94
                                         .decode()\
                                         .replace("'", '"'))
                    
                    # Pass the dictionary to the broadcast function.
                    self.broadcast(message, connection)
    
                # Close connection if no message was sent
                else:
                    self.remove_connection(connection)
                    break
    
            except Exception as error:
                exception(
                        f"There was an issue handling the user connection:\n"
                        f"{error}"
                )
                self.remove_connection(connection)
                break
    
    
    def broadcast(self, message: dict, sender: socket.socket) -> None:
    
        # Iterate on connections in order to send message to all client's connected
        for client in self.connections:

            # Don't send back to the sender.
            if client != sender:
    
                if message["subject"]:# Add the subject line, if one is provided.
                    message_string = ( f"from: {message['username']}\n"
                                       f"subject: {message['subject']}\n"
                                       f"content:\n{message['content']}\n" )\
                        .encode()
    
                # Otherwise, present the string as normal.
                else:
                    message_string = ( f"from: {message['username']}\n"
                                       f"content:\n{message['content']}\n" )\
                        .encode()
    
                try: client.send(message_string)
    
                # If that fails, you've probably got a dead socket.
                except Exception as error:
                    print('Error broadcasting message: {error}')
                    self.remove_connection(client_conn)
    
    
    def remove_connection(self, conn: socket.socket) -> None:
    
        # Check if connection exists on connections list
        if conn in self.connections:
            # Close socket connection and remove connection from connections list
            conn.close()
            self.connections.remove(conn)
    
    
<<<<<<< HEAD
    def server(self, address, port) -> None:
=======
    def start(self, address, port) -> None:
>>>>>>> 07636e6aebe315c45abde9faed3739284b07eb94
        """
    
        """
        
    
<<<<<<< HEAD
        try:# Set up a socket to run the server on.

            # Create the socket object.
            socket_instance = socket.socket(
=======
        try:
            self.socket_instance = socket.socket(
>>>>>>> 07636e6aebe315c45abde9faed3739284b07eb94
                socket.AF_INET,
                socket.SOCK_STREAM
            )

<<<<<<< HEAD
            # Bind the object to an address and port.
            socket_instance.bind(
                (str(address), int(port))
            )

            # Begin listening on the connection.
            socket_instance.listen(4)
=======
            self.socket_instance.bind(
                (str(address), int(port))
            )

            self.socket_instance.listen(4)
>>>>>>> 07636e6aebe315c45abde9faed3739284b07eb94

            # TODO: Log successful server instance.
        
            while True:

                # Accept client connection
<<<<<<< HEAD
                socket_connection, address = socket_instance.accept()
=======
                socket_connection, address = self.socket_instance.accept()
>>>>>>> 07636e6aebe315c45abde9faed3739284b07eb94

                # Add client connection to connections list
                self.connections.append(socket_connection)

                threading.Thread( target=self.handle_user_connection,
                                  args=[ socket_connection,
                                         address            ]   )\
                         .start()


        except Exception as error:
            # TODO: Exception Logging.
            pass


        finally:
<<<<<<< HEAD
            if len(connections) > 0:
                for conn in connections:
                    remove_connection(conn)

            socket_instance.close()


class tools:

    def __init__(self):

    def createUserDB():
        """
        Create an sqlite3 database within the users .local directory and populate
        it with a table for logging chat messages.
    
        The table will consist of a X fields; username for logging who sent the
        message, subject for the general idea behind the message which can be set
        with a /command, a timestamp for when it was sent, and the text body
        of the message itself.
        """
    
        # Set up logging.
        getLogger()
    
        _name = inspect.stack()[0][3]
        _time = lambda datetime.timestamp(datetime.now())
    
        debugging(#####} CONSTANTS
            f"{_time}:{_name}:Beginning constants setup."
        )
    
        # The users .local directory; see the Linux FS for info about that.
        local_directory = f"/home/{username()}/.local"
        debugging(f"{_time}:{_name}:    --Local Directory: ✅")
    
        # Filename and path for the sqlite database.
        lab_database = f"{local_directory}/lab-93.db"
        debugging(f"{_time}:{_name}:    --Lab Database: ✅")
    
        # Bash command for creating the .local directory.
        createSubDirectory = f"mkdir -p {local_directory} > /dev/null "
        debugging(f"{_time}:{_name}:    --Sub-Directory Shell String: ✅")
    
        # SQLite3 command for creating the messages table
        # with our required columns.
        createMessagesTable_SQL = (
            f"CREATE TABLE IF NOT EXISTS "
                f"messages("
                    f"username TEXT REQUIRED KEY, "
                    f"subject TEXT, "
                    f"timestamp REAL, "
                    f"message TEXT"
                f")"
        )
        debugging(f"{_time}:{_name}:    --Messages Table Creation SQL String: ✅")
    
    
    
        # Check for the .local directory and create it if need be.
        debugging(f"{_time}:{_name}:    --Validate Local Directory:")
    
        # If glob returns any results then the directory already exists.
        if len(glob(local_directory)) >= 1:
            debugging(f"{_time}:{_name}:      --Directory exists. ✅"); pass
    
        else:# If not, then the directory needs to be created.
            debugging(f"{_time}:{_name}:      --Directory does not exist; creating.")
    
            try: subprocess.Run(# Execute the directory creation one-liner.
                createSubDirectory.split()
            ); information(
                f"{_time:{_name}:      --Created subdirectory at {local_directory}"
            )
    
            # Log any mishaps and inform the caller.
            except Exception as error:
                exception(
                f"{_time}:{_name}:"
                f"There was an issue creating the .local subdirectory:\n"
                f"{error}"
            )


    # Begin sqlite database connection and initialize cursor.
    debugging(f"{_time}:{_name}:    --Attempting connection to database at {lab_database}")
    try:
        # Establish connection to .db file.
        connection = sqlite3.connect(lab_database); debugging(
            f"{_time}:{_name}:      --Connection established ✅"
        )

        # Create cursor and lable it for execution.
        cursor = connection.cursor(); execute = cursor.execute; debugging(
            f"{_time}:{_name}:      --Cursor successfully labelled ✅"
        )

    # Run the table creation sql and save your work!
    while True: try:
        cursor.execute(
            createMessagesTable_SQL
        ); information(
            f"{_time}:{_name}:"
            f"Messages table successfully created for user {username()}"
        ); connection.commit(); break

    # Handle any errors gracefully, and inform the caller.
    except Exception as error:
        exception(
            f"{_time}:{_name}:"
            f"There was an issue creating a messages table "
            f"within the user database;\n{error}}"
        )

        return error


if __name__ == "__main__":


    class OptionsError(Exception):


        class ConflictingOptions(Exception, *options):
            """ Called if the user calls exclusive, conflicting options. """
            
            print(
                f"Conflicting arguments {argument for argument in options} "
                f"can not be used together."
            )

            exit()

        class InsufficientOptions(Exception,  *options, **solutions):
            """ Called if the user does not provide enough information. """

            for option in options:
                print(
                    f"Option {option} requires additional information;\n"
                    f"Try {solutions[option]}"
                )

            exit()


    parser = ArgumentParser()
    
    parser.add_argument( "-a",
                         "--address",
                         help="IP Address to route connections on." )

    parser.add_argument( "-b",
                         "--broadcast",
                         action="store_true",
                         help="Set the client to act as a dynamic agent." )

    parser.add_argument( "-c",
                         "--client",
                         action="store_true",
                         help="If using repeater mode, sets the agent to client mode." )

    parser.add_argument( "-m",
                         "--mode",
                         help="Alternate definition of either repeater or broadcast mode." )

    parser.add_argument( "-p",
                         "--port",
                         help="Port number to listen on." )

    parser.add_argument( "-r",
                         "--repeater",
                         action="store_true",
                         help="Set client to run in client/server mode." )

    parser.add_argument( "-s",
                         "--server",
                         action="store_true",
                         help="If using repeater mode, sets the agent to server mode." )

    arguments = parser.parse_args()


    # Collect or define address; defaults to all public addresses.
    if arguments.address: address = arguments.address
    else: address = "0.0.0.0"


    # Collect or define port number; default to 5190 because AOL Chat.
    if arguments.port: port = arguments.port
    else: port = 5190
    

    # The mode could be anything, but we only respond to two specific options.
    if arguments.mode and arguments.mode != "repeater" or "broadcast":
        raise OptionsError.ImproperOptions()

    # If not by mode bu by flag, but we have both flags, thats a conflict.
    elif not arguments.mode and arguments.broadcast and arguments.repeater:
        raise OptionsError.ConflictingOptions(
            "--broadcast", "--repeater"
        )

    # If not by mode nor flag, that's an insufficiency.
    elif not arguments.mode and not arguments.broadcast and not arguments.repeater:
        raise OptionsError.InsufficientOptions()


    # Broadcast-Mode subchecks.
    if arguments.broadcast is True or arguments.mode is "broadcast": ...


    # Repeater-Mode subchecks.    
    if arguments.repeater is True or arguments.mode is "repeater":

        # Check client & server aren't both given.
        if arguments.server and arguments.client:
            raise OptionsError.ConflictingOptions(
                "--client", "--server"
            )
        
        # Check at least server or client are given.
        elif not arguments.server and not arguments.client:
            raise OptionsError.InsufficientOptions(
                "repeater",
                repeater="supplying either the --server or --client flags."
            )

        else:
            if arguments.server: server.server(address, port)
            if arguments.client: client.client(address, port)
=======
            if len(self.connections) > 0:
                for i in range(len(self.connections)):
                    del self.connections[0]
                    

            self.socket_instance.close()
>>>>>>> 07636e6aebe315c45abde9faed3739284b07eb94
