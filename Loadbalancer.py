import socket
import threading
import json
import http.client

LOAD_BALANCER_HOST = "0.0.0.0"
LOAD_BALANCER_PORT = 8888
SERVER_HOST = "localhost"

SERVERS = {"TCP-Server": 8000, "UDP-Server": 8887}

# Send the data to the UDP-Server and then back to the Client
def send_to_udp_server(server_port, server_type, rest_data, client_socket):
    server_address = (SERVER_HOST, server_port)
    data_json = json.dumps(rest_data)
    try:
        server_socket = socket.socket(socket.AF_INET, server_type)
        server_socket.sendto(data_json.encode(), server_address)
        print(f"Data sucessfully send to Server: {data_json}")
        # Wait for the response from the UDP server
        response, server = server_socket.recvfrom(4096)
        response_message = response.decode()
        print(f"Received response from server: {response_message}")

        # Send the response back to the client
        client_socket.sendall(response_message.encode())
        
    except Exception as e:
        print(f"Error sending to UDP-Server: {e}")
    finally:
        client_socket.close()
        server_socket.close()

# Connect to TCP-Server, send Data to it and forward it to Client
def connect_to_tcp_server(server_port, rest_data, client_socket):
    server_address = (SERVER_HOST, server_port)
    data_json = json.dumps(rest_data)
    try:
        conn = http.client.HTTPConnection(server_address[0], server_address[1])
        headers = {'Content-type': 'application/json'}
        method = rest_data.pop('Method')

        # Decide wether or not a body is needed
        if method == 'GET' or method == "DELETE":
            conn.request(method, '/', headers=headers)
        else:
            conn.request(method, '/', body=data_json, headers=headers)
        
        response = conn.getresponse()
        print(f"Response status: {response.status}, reason: {response.reason}")
        
        # Read and process the response body
        body = response.read().decode()
        message = body.split('\r\n\r\n')[-1]
        cleaned_message = message.strip('"')
        
        # Send the message back to the client
        client_socket.sendall(cleaned_message.encode())
        conn.close()

    except Exception as e:
        print(f"Error connecting to TCP-Server: {e}")
    finally:
        client_socket.close()

# Find out which server type is required
def get_server_by_name(server_name, rest_data, client_socket):
    server_port = SERVERS[server_name]
    try:
        if server_name == "TCP-Server":
            connect_to_tcp_server(server_port, rest_data, client_socket)
        elif server_name == "UDP-Server":
            send_to_udp_server(server_port, socket.SOCK_DGRAM, rest_data, client_socket)
    except Exception as e:
        print(f"Connecting to {server_name} unsuccessful: {e}")

# Make a TCP connection to the Client
def handle_client_connection(client_socket):
    try:
        client_data = client_socket.recv(1024).decode()
        data_dict = json.loads(client_data)
        print("Received data from client:", client_data)
        get_server_by_name(data_dict.pop("Connect to"), data_dict, client_socket)
    except Exception as e:
        print(f"Error handling client connection: {e}")
    finally:
        client_socket.close()

# Receive data from Client
def receive_from_client():
    load_balancer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    load_balancer_socket.bind((LOAD_BALANCER_HOST, LOAD_BALANCER_PORT))
    load_balancer_socket.listen(5)

    print(f"Load balancer is listening on {LOAD_BALANCER_HOST}:{LOAD_BALANCER_PORT}")

    # Endless loop to listen
    while True:
        client_socket, client_address = load_balancer_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Establishing threads for cuncurrent client handling 
        client_thread = threading.Thread(target=handle_client_connection, args=(client_socket,))
        client_thread.start()

receive_from_client()
