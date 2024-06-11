import socket
import threading


HEADER = 64
PORT = 5050
# SERVER = "192.168.192.119" # Device's IPV4, Because i wanna run this on my local network, this is the device the server is gonna run on
# print(socket.gethostname()) # PADDY-117
SERVER = socket.gethostbyname(socket.gethostname()) #192.168.192.119
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# Now we make a socket, its gonna allow us to open up this device to other connections
# Pick the PORT and the SERVER and pick the socket and then bind the socket to that address

# The first arg is the family of the socket, its more of a category, the second 
# specifies the type, that we're streaming data through the socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Now we bind our socket to an address
server.bind(ADDR) # So anything that connects to this address now, will hit this socket(server variable)


# Now we setup the socket for listening, print out a few things, and let it wait for new connections

def handle_client(conn, addr):
    """
    This function will be running concurrently for 
    each client
    """
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) # How many bytes to accept
        if msg_length:
            msg_length = int(msg_length)

            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Message Received".encode(FORMAT))

    conn.close()


def start():
    """
    To start the socket server for us
    """
    # allow our server to start listening to connections
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept() # We will wait for a new connection to the server,
                                     # When a new connection is established, it will store the conn and the addr
                                     # conn will help send information back to that connection

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
start()