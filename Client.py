import sys
import socket
import subprocess
import concurrent.futures
import threading
import time

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            sender, message_content = message.split(">", 1)
            if sender != username:
                print(message)
        except ConnectionAbortedError:
            print("Connection to the server was aborted.")
            sys.exit(0)
            # break
        except ConnectionResetError:
            print("Connection to the server was reset.")
            sys.exit(0)
            # break
        except:
            print("An error occurred while receiving messages.")
            client_socket.close()
            sys.exit(0)
            # break

# '''
def get_local_ip():
    # Create a UDP socket to connect to a known external host
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))  # Google's DNS server
    local_ip = sock.getsockname()[0]
    sock.close()
    return local_ip
def ping(ip):
    try:
        output = subprocess.check_output(["ping", "-n", "1", "-w", "200", ip], shell=True)
        if "TTL=" in output.decode('utf-8'):
            return ip
    except subprocess.CalledProcessError:
        pass
def scan_network(ip_prefix):
    active_devices = []
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit ping tasks to the thread pool
        ping_tasks = [executor.submit(ping, f"{ip_prefix}.{i}") for i in range(1, 255)]
        # Wait for the ping tasks to complete and collect the results
        for task in ping_tasks:
            result = task.result()
            if result:
                # print(f"Device found at IP: {result}")
                active_devices.append(result)
    end_time = time.time()
    execution_time = end_time - start_time
    return active_devices, execution_time
# Get the local IP address of the current device
local_ip = get_local_ip()
ip_prefix = ".".join(local_ip.split(".")[:-1])  # Remove the last octet

print("Scanning network for devices...")
# Scan the network for devices
active_devices, timer = scan_network(ip_prefix)
print("Took " + str(timer) + " seconds to complete.")
# # Print the discovered IP addresses
# print("Active devices on the network:")
# for device in active_devices:
#     print(device)
for ip_address in active_devices:
    try:
        # Set up the client
        host = ip_address  # Replace with the server's IP address or hostname
        port = 9999
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print("Connected to",host+':'+str(port))
        break
    except:
        continue
# '''

# Get the username from the user
username = input("Enter Your Name: ")

# Send the name, IP address, and port to the server
client_address = client_socket.getsockname()
info_message = f"{username}|{client_address[0]}|{client_address[1]}"
client_socket.send(info_message.encode('utf-8'))

# Start a thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Main loop to send messages
while True:
    try:
        message = input()
        if message == "exit()":
            client_socket.close()
            # sys.exit(0)
            # break
        full_message = f"{username}> {message}"
        client_socket.send(full_message.encode('utf-8'))
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Closing the client.")
        client_socket.close()
        # sys.exit(0)
    except Exception as e:
        print(f"An error occurred while sending the message: {str(e)}")
        break