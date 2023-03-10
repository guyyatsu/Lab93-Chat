import socket, threading
import argparse
from os import getlogin as username
import base64
from glob import glob
from logging import getLogger, exception
from logging import debug as debugging
from logging import info as information
from datetime import datetime
import inspect


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
            f"{_time}:{_name}:Messages table successfully created for user {username()}"
        ); connection.commit(); break

    # Handle any errors gracefully, and inform the caller.
    except Exception as error:
        exception(
            f"{_time}:{_name}:"
            f"There was an issue creating a messages table "
            f"within the user database;\n{error}}"
        )

        return error


def handle_messages(connection: socket.socket):
    '''
        Receive messages sent by the server and display them to user
    '''

    while True:
        try:
            msg = connection.recv(1024)

            # If there is no message, there is a chance that connection has closed
            # so the connection will be closed and an error will be displayed.
            # If not, it will try to decode message in order to show to user.
            if msg:
                print(msg.decode())
            else:
                connection.close()
                break

        except Exception as e:
            print(f'Error handling message from server: {e}')
            connection.close()
            break

def client(SERVER_ADDRESS, SERVER_PORT) -> None:
    '''
    '''


    try:

        # Instantiate socket and start connection with server
        socket_instance = socket.socket()
        socket_instance.connect((SERVER_ADDRESS, int(SERVER_PORT)))

        # Create a thread in order to handle messages sent by server
        threading.Thread(target=handle_messages, args=[socket_instance]).start()

        while True:

            # Recieve user input as message string.
            message_packet = {"content": input(), "username": username()})
           

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
                    message_packet["subject"] = str(msg.split(" ")[1])
                    message_packet["content"] = str(" ".join(msg.split(" ")[2:-1]))


            # Convert message packet to ascii string
            socket_instance.send(
                base64.b64encode(
                    str(message_packet).encode('ascii')
                )
            )

        # Close connection with the server
        socket_instance.close()

    except Exception as e:
        print(f'Error connecting to server socket {e}')
        socket_instance.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", help="IP Address to route connections on.")
    parser.add_argument("-p", "--port", help="Port number to listen on.")
    parser.add_argument("-s", "--scan", action="store_true")

    arguments = parser.parse_args()

    if arguments.address: address = arguments.address
    else: address = "0.0.0.0"

    if arguments.port: port = arguments.port
    else: port = 12000


    # TODO: Local IP Address Scanning.
    """ 
    if arguments.scan:
        socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket.connect(("8.8.8.8", 80))

        IP = socket.getsockname()[0]
        LocalNet = ".".join(IP.split(".")[0:3])
        socket.close()


        print(f"Scanning for connection on local network {LocalNet}0-255, port {port}")
        for _address in range(0, 256):
            try: client(f"{LocalNet}.{str(_address)}", port)

    """
        
        

    client(address, port)
