import socket
import threading
import json
import http.client

LOAD_BALANCER_HOST = "localhost"
LOAD_BALANCER_PORT = 8888
SERVER_HOST = "localhost"

SERVERS = {"TCP-Server": 8000, "UDP-Server": 8887}

def connect_to_server(server_port, server_type, rest_data, connect_necessary, client_socket):
    server_socket = socket.socket(socket.AF_INET, server_type)
    server_address = (SERVER_HOST, server_port)
    data_json = json.dumps(rest_data)

    try:
        if connect_necessary:
            conn = http.client.HTTPConnection(server_address[0], server_address[1])
            headers = {'Content-type': 'application/json'}
            method = rest_data.pop('Method')

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
            print(cleaned_message)
            
            # Send the cleaned message back to the client
            client_socket.sendall(cleaned_message.encode())
            conn.close()
        else:
            server_socket.sendto(data_json.encode(), server_address)
        
    except Exception as e:
        print(f"Error connecting to server: {e}")
    finally:
        client_socket.close()
        server_socket.close()

def get_server_by_name(server_name, rest_data, client_socket):
    server_port = SERVERS[server_name]
    try:
        if server_name == "TCP-Server":
            connect_to_server(server_port, socket.SOCK_STREAM, rest_data, True, client_socket)
        elif server_name == "UDP-Server":
            connect_to_server(server_port, socket.SOCK_DGRAM, rest_data, False, client_socket)
    except Exception as e:
        print(f"Connecting to {server_name} unsuccessful: {e}")

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

        

def receive_from_client():
    load_balancer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    load_balancer_socket.bind((LOAD_BALANCER_HOST, LOAD_BALANCER_PORT))
    load_balancer_socket.listen(5)

    print(f"Load balancer is listening on {LOAD_BALANCER_HOST}:{LOAD_BALANCER_PORT}")

    while True:
        client_socket, client_address = load_balancer_socket.accept()
        print(f"Accepted connection from {client_address}")
        client_thread = threading.Thread(target=handle_client_connection, args=(client_socket,))
        client_thread.start()

receive_from_client()
