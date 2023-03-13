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

                if msg:
                    print(msg.decode())
                else:
                    connection.close()
                    break

            except Exception as e:
                print(f'Error handling message from server: {e}')
                connection.close()
                break

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

                # User Commands
                """ User commands allow for actions to be made from chat;
                such as quitting the session or defining a subject for
                a message.  Commands are defined by typing a forward slash
                as the first letter of your message."""

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
                    base64.b64encode(
                        str(message_packet).encode('ascii')
                    )
                )

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

        # The classes semblance of identity.
        self             = self

        # An address to host services on.
        self.address     = address

        # A socket to listen out for.
        self.port        = port

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
                    message = load(base64.b64decode(msg)\
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
    
    
    def start(self, address, port) -> None:
        """
    
        """
        
    
        try:
            self.socket_instance = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            self.socket_instance.bind(
                (str(address), int(port))
            )

            self.socket_instance.listen(4)

            # TODO: Log successful server instance.
        
            while True:

                # Accept client connection
                socket_connection, address = self.socket_instance.accept()

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
            if len(self.connections) > 0:
                for i in range(len(self.connections)):
                    del self.connections[0]
                    

            self.socket_instance.close()