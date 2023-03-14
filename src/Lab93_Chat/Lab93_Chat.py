import base64
import datetime
import socket
import threading
import inspect
from os import getlogin as username
from argparse import ArgumentParser
from json import loads as load
from logging import getLogger, exception



class Client:


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
    
      # Set up logging.
        getLogger()
    
        _name = inspect.stack()[0][3]
        _time = lambda: datetime.timestamp(datetime.now())

        try:

            # Instantiate socket and start connection with server
            self.socket_instance = socket.socket()
            self.socket_instance.connect((address, int(port)))

            # Create a thread in order to handle messages sent by server
            threading.Thread(target=self.handle_messages, args=[self.socket_instance]).start()

            while True:

                # Recieve user input as message string.
                message_packet = {
                    "content": input(),
                    "username": username()
                }
                
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
                    if cmd == "/quit": break
    
                    # Allows the attachment of a subject line to a msg.
                    if cmd == "/subject":
                        message_packet["subject"] = str(message_content.split(" ")[1])
                        message_packet["content"] = str(" ".join(message_content.split(" ")[2:-1]))
    
                    # Scan the local network for fellow chat servers.
                    if cmd == "/scan": pass
                        
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
    
        except Exception as error:
            exception(
                f"{_name}:{_time}There was an issue trying to set up the chat client;\n"
                f"{error}"
            ); self.socket_instance.close()

            return error


class Server:


    
    def __init__(self):
        """
        Set up a couple of constants required at runtime.  Here we've got self; but also
        we've got self.address which defines an IP to make the service available on, a self.port
        which narrows down the channel to operate on, and self.connections which enumerates every
        address that has made a valid connection to the instance.
        """

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
    
                try: 
                    client.send(message_string)
    
                # If that fails, you've probably got a dead socket.
                except Exception as error:
                    print('Error broadcasting message: {error}')
                    self.remove_connection(client)
    
    
    def remove_connection(self, conn: socket.socket) -> None:
    
        # Check if connection exists on connections list
        if conn in self.connections:
            # Close socket connection and remove connection from connections list
            conn.close()
            self.connections.remove(conn)
    
    
    def start(self, address, port) -> None:
        """
    
        """
        print(f"Starting server on ip {address} and port {port}...")
        try:# Set up a socket to run the server on.

            # Create the socket object.
            socket_instance = socket.socket()


            self.socket_instance = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )


            # Bind the object to an address and port.
            self.socket_instance.bind(
                (str(address), int(port))
            )

            # Begin listening on the connection.
            self.socket_instance.listen(4)


            # TODO: Log successful server instance.
        
            while True:
                print("Waiting for connections...")
                # Accept client connection

                socket_connection, address = self.socket_instance.accept()

                print(f"Connection to {address} made!")

                # Add client connection to connections list
                self.connections.append(socket_connection)
                threading.Thread( target=self.handle_user_connection,
                                  args=[ socket_connection,
                                         address            ]   )\
                         .start()


        except Exception as error:
            print(error)
            # TODO: Exception Logging.
            pass


        finally:

            if len(self.connections) > 0:
                for conn in self.connections:
                    self.remove_connection(conn)

            socket_instance.close()



if __name__ == "__main__":


    class OptionsError(Exception):

        class ConflictingOptions(Exception):
            """ Called if the user calls exclusive, conflicting options. """
            def __init__(self, *options):
                super().__init__()
                arguments = ""
                for args in options:
                    arguments += args + " "
                print(
                    f"Conflicting arguments {arguments} "
                    f"can not be used together."
                )

                exit()


        class InsufficientOptions(Exception):
            """ Called if the user does not provide enough information. """
            def __init__(self, *options, **solutions):
                super().__init__()

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
    if arguments.address: 
        address = arguments.address
    else: 
        address = "0.0.0.0"


    # Collect or define port number; default to 5190 because AOL Chat.
    if arguments.port: 
        port = arguments.port
    else: 
        port = 5190
    

    # If not by mode bu by flag, but we have both flags, thats a conflict.
    if arguments.broadcast and arguments.repeater:
        raise OptionsError.ConflictingOptions(
            "--broadcast", "--repeater"
        )

    # If not by mode nor flag, that's an insufficiency.
    elif not arguments.broadcast and not arguments.repeater:
        raise OptionsError.InsufficientOptions()


    # Broadcast-Mode subchecks.
    if arguments.broadcast is True: 
        ...
        #TODO: Broadcast process


    # Repeater-Mode subchecks.    
    if arguments.repeater is True:

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
            if arguments.server:
                server1 = Server() 
                server1.start(address, port)
            if arguments.client: 
                client1 = Client()
                client1.start(address, port)

