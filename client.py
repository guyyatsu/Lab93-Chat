import socket, threading
import argparse 

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
