import socket
import threading

LOAD_BALANCER_HOST = "loadbalancer"
LOAD_BALANCER_PORT = 9999
SERVERS = {"TCP-Server": 8888, "UDP-Server": 8889}

def connect_to_server(server_adress, server_type, client_socket,):
    server_socket = socket.socket(socket.AF_INET, server_type)
    server_socket.connect(server_adress)

def get_server_by_name(server_name):
    match server_name:
        case "TCP-Server":
            connect_to_server(SERVERS[server_name], socket.SOCK_STREAM)
        case "UDP-Server":
            connect_to_server(SERVERS[server_name], socket.SOCK_DGRAM)

def receive_from_client():
    load_balancer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    load_balancer_socket.bind((LOAD_BALANCER_HOST, LOAD_BALANCER_PORT))
    load_balancer_socket.listen(5)

    print(f"Load balancer is listening on {LOAD_BALANCER_HOST}:{LOAD_BALANCER_PORT}")

    while True:
        client_socket, client_address = load_balancer_socket.accept()
        print(f"Accepted connection from {client_address}")

        client_data = client_socket.recv(1024).decode()

        print("Received data from client:", client_data)
        
        client_socket.close()