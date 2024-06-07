import socket
import threading
from user import User

PORT = 55555
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = '![DISCONNECT]'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# List to hold User objects
users = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for user in users:
        user.send_message(message)

# Handling Messages From Clients
def handle(user):
    while True:
        try:
            # Broadcasting Messages
            message = user.conn.recv(1024).decode(FORMAT)
            broadcast(message)
        except Exception as e:
            # Removing And Closing Clients
            print(f"Error or disconnect from user: {user.username}, {e}")
            users.remove(user)
            user.conn.close()
            broadcast(f'{user.username} left!')
            break

# Sending specific requests to a client
def send_request(client, request):
    client.sendall((f"[R]{request}").encode('utf-8'))

def get_input(client, username):
    padded_input = client.recv(1024).decode(FORMAT)
    input = padded_input[len(username)+2:]
    return input

# Registration and Login Function
def register_or_login(client):
    while True:
        send_request(client, 'USER')
        username = client.recv(1024).decode(FORMAT)
        client.send('Do you want to (1) Register or (2) Login?'.encode(FORMAT))
        choice = get_input(client, username)

        if choice == '1':
            client.send('Enter password:'.encode(FORMAT))         
            password = get_input(client, username)
            User.register(username, password)
            client.send('Registration successful. Please login.'.encode(FORMAT))
        elif choice == '2':
            client.send('Enter password:'.encode(FORMAT))
            password = get_input(client, username)
            authenticated, permission_level = User.authenticate(username, password)
            if authenticated:
                return User(username, client)
            else:
                client.send('Invalid credentials. Try again.'.encode(FORMAT))
        else:
            client.send('Invalid choice. Please choose 1 or 2.'.encode(FORMAT))

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print(f"Connected with {address}")

        # Handle user registration or login
        user = register_or_login(client)

        # Add user to the list of connected users
        users.append(user)

        # Print and broadcast the username
        print(f"Username is {user.get_username()}")
        broadcast(f"{user.get_username()} joined!")
        user.send_message('Connected to server!')

        # Start handling thread for the client
        thread = threading.Thread(target=handle, args=(user,))
        thread.start()

def start():
    server.listen()
    print("[STARTING] SERVER...")
    print(f"[LISTENING] {SERVER}")
    receive()

start()