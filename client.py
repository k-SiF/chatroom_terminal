import socket
import threading
from user import User

PORT = 55555
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = '![DISCONNECT]'

# Choosing Username
username = input("Username: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'USER' Send Username
            message = client_socket.recv(1024).decode(FORMAT)
            if message.startswith("[R]"):
                command = message[3:]
                if command == "USER":
                    send(username)
            else:
                print(message)
        except Exception as e:
            # Close Connection When Error
            print(f"An error occurred: {e}")
            client_socket.close()
            break

def send(msg):
    message = msg.encode(FORMAT)
    client_socket.send(message)

# Sending Messages To Server
def write():
    while True:
        message = '{}: {}'.format(username, input(''))
        send(message)

def main():    
    # Starting Threads For Listening And Writing
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()

if __name__ == "__main__":
    main()