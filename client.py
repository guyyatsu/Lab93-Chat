import socket, threading
from glob import glob
import base64
import argparse
from os import getlogin as username


from logging import getLogger, exception



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

    # The users .local directory; see the Linux FS for info about that.
    local_directory = f"/home/{username()}/.local"

    # Filename and path for the sqlite database.
    lab_database = f"{local_directory}/lab-93.db"

    # Bash command for creating the .local directory.
    createSubDirectory = f"mkdir -p {local_directory} > /dev/null "

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

    # Check for the .local directory and create it if need be.
    if len(glob(local_directory)) >= 1: pass
    else: subprocess.Run(createSubDirectory.split())

    # Begin sqlite database connection and initialize cursor.
    connection = sqlite3.connect(lab_database)
    cursor = connection.cursor(); execute = cursor.execute

    # Run the tabe creation sql and save your work!
    while True: try:
        cursor.execute(
            createMessagesTable_SQL
        ); connection.commit(); break

    except Exception as error:
        exception(
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
        Main process that start client connection to the server 
        and handle it's input messages
    '''

    # Port and address are taken by argument now.
    #SERVER_ADDRESS = '0.0.0.0'
    #SERVER_PORT = 12000

    try:
        # Instantiate socket and start connection with server
        socket_instance = socket.socket()
        socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))
        # Create a thread in order to handle messages sent by server
        threading.Thread(target=handle_messages, args=[socket_instance]).start()

        print('Connected to chat!')

        # Read user's input until it quit from chat and close connection
        while True:
            msg = input()

            if msg == 'quit':
                break

            # Parse message to utf-8
            socket_instance.send(msg.encode())

        # Close connection with the server
        socket_instance.close()

    except Exception as e:
        print(f'Error connecting to server socket {e}')
        socket_instance.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", help="IP Address to route connections on.")
    parser.add_argument("-p", "--port", help="Port number to listen on.")

    arguments = parser.parse_args()
    if arguments.address: address = arguments.address
    else: address = ".0.0.0"

    if not arguments.port: port = arguments.port
    else: port = 12000

    client(address, port)
