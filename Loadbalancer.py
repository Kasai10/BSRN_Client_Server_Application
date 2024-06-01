import socket
import threading
import json
import http.client

LOAD_BALANCER_HOST = "loadbalancer"
LOAD_BALANCER_PORT = 9999
SERVERS = {"TCP-Server": [8888, 8889, 8890], "UDP-Server": [8891, 8892, 8893]}

lock_thread = threading.Lock()

def connect_to_server(server_adress, server_type, rest_data, connect_necessary):
    server_socket = socket.socket(socket.AF_INET, server_type)
    
    data_json = json.dumps(rest_data)

    if(connect_necessary):
        conn = http.client.HTTPConnection(server_adress[0], server_adress[1])
        headers = {'Content-type': 'application/json'}
        method = rest_data.pop('Method')

        if method == 'GET':
            conn.request(method, '/', headers=headers)
        else:
            conn.request(method, '/', body=data_json, headers=headers)
        
        response = conn.getresponse()
        print(f"Response status: {response.status}, reason: {response.reason}")
        conn.close()
    else:
        server_socket.sendto(data_json.encode(),server_adress)
    

    server_socket.close()


def get_server_by_name(server_name, server_address, rest_data):
    with lock_thread:
        if not SERVERS[server_name]:
            raise Exception(f"No available ports for {server_name}")
        
        server_port = SERVERS[server_name].pop(0)
        server_address = (server_address, server_port)
    
    try:
        match server_name:
            case "TCP-Server":
                connect_to_server(server_address, socket.SOCK_STREAM, rest_data, True)
            case "UDP-Server":
                connect_to_server(server_address, socket.SOCK_DGRAM, rest_data, False)
    except:
        raise Exception(f"Connecting to {server_name} unsuccessfull")
    finally:
        with lock_thread:
            SERVERS[server_name].append(server_port)

def handle_client_connection(client_socket):
    client_data = client_socket.recv(1024).decode()
    data_dict = json.loads(client_data)
    print("Received data from client:", client_data)
    client_socket.close()
    get_server_by_name(data_dict.pop("Connect to"), data_dict.pop("IP-Adress"),data_dict)
    

def receive_from_client():
    load_balancer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    load_balancer_socket.bind((LOAD_BALANCER_HOST, LOAD_BALANCER_PORT))
    load_balancer_socket.listen(5)

    print(f"Load balancer is listening on {LOAD_BALANCER_HOST}:{LOAD_BALANCER_PORT}")

    while True:
        client_socket, client_address = load_balancer_socket.accept()
        print(f"Accepted connection from {client_address}")
        client_thread = threading.Thread(target=handle_client_connection, args=(client_socket, client_address))
        client_thread.start()