import socket
import threading

def handle_client(client_socket, client_address):
    client_info = client_socket.recv(1024).decode('utf-8')
    name, ip_address, port = client_info.split("|")
    print(f"Connected to {name} at {ip_address}:{port}")

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Received from {name}: {message}")
                broadcast(message, client_socket)
        except ConnectionResetError:
            print(f"Connection reset by {name}")
            break
        except ConnectionAbortedError:
            print(f"Connection aborted by {name}")
            break
        except:
            print(f"Error occurred for {name}")
            break

    clients.remove(client_socket)
    client_socket.close()
    print(f"Connection closed for {name}")

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            client.send(message.encode('utf-8'))

def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

current_ip = get_ip_address()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set up the server
host = '0.0.0.0'  # Listen on all network interfaces
port = 9999
"""
port = 5000  # Starting port number
while True:
    try:
        server_socket.bind((host, port))
        break
    except OSError:
        print(f"Port {port} is already in use. Trying the next port...")
        port += 1
"""
server_socket.bind((host, port))
server_socket.listen(5)

clients = []

# Wait for and handle incoming connections
print(f"\nServer listening on {host}:{port} -> \tlocalhost = {current_ip}\n")

while True:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    # print(f"Connected with {client_address}")
    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_handler.start()
