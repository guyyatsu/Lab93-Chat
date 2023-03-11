import socket, threading
import argparse

connections = []


def handle_user_connection(connection: socket.socket, address: str) -> None:
    while True:
        try:
            # Recieve client's posted message.
            msg = connection.recv(4096)

            if msg:
                # TODO: Log client messages to server database.
                message = load(b64decode(msg)\
                                     .decode()\
                                     .replace("'", '"'))
                
                # Build message format and broadcast to users connected on server
                msg_to_send = f'From {address[0]}:{address[1]} - {msg.decode()}'
                broadcast(msg_to_send, connection)

            # Close connection if no message was sent
            else:
                remove_connection(connection)
                break

        except Exception as e:
            print(f'Error to handle user connection: {e}')
            remove_connection(connection)
            break


def broadcast(message, connection: socket.socket) -> None:
    '''
        Broadcast message to all users connected to the server
    '''

    # Iterate on connections in order to send message to all client's connected
    for client_conn in connections:
        # Check if isn't the connection of who's send
        if client_conn != connection:
            try:
                # Sending message to client connection
                client_conn.send(message["content"].encode())

            # if it fails, there is a chance of socket has died
            except Exception as e:
                print('Error broadcasting message: {e}')
                remove_connection(client_conn)


def remove_connection(conn: socket.socket) -> None:

    # Check if connection exists on connections list
    if conn in connections:
        # Close socket connection and remove connection from connections list
        conn.close()
        connections.remove(conn)


def server(port, address) -> None:
    """

    """
    

    try:
        socket_instance = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        socket_instance.bind(
            (str(address), int(port))
        )

        socket_instance.listen(4)

        # TODO: Log successful server instance.
        
        while True:

            # Accept client connection
            socket_connection, address = socket_instance.accept()

            # Add client connection to connections list
            connections.append(socket_connection)

            threading.Thread( target=handle_user_connection,
                              args=[ socket_connection,
                                     address            ]   )\
                     .start()


    except Exception as error:
        # TODO: Exception Logging.
        pass


    finally:
        if len(connections) > 0:
            for conn in connections:
                remove_connection(conn)

        socket_instance.close()


if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument( "-a",
                         "--address",
                         help="IP Address to route connections on." )

    parser.add_argument( "-p",
                         "--port",
                         help="Port number to listen on." )

    arguments = parser.parse_args()


    if arguments.address: address = arguments.address
    else: address = "0.0.0.0"

    if arguments.port: port= arguments.port
    else: port = 12000


    server(port, address)
