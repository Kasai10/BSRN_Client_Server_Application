import socket
import threading
import json
import http.client

LOAD_BALANCER_HOST = "localhost"
LOAD_BALANCER_PORT = 9999
SERVER_HOST = "localhost"
#How does the tcp server know if it should use http or https?
#Very confusing
SERVERS = {"TCP-Server": [8000, 80, 443], "UDP-Server": 8887}

def connect_to_server(server_port, server_type, rest_data, connect_necessary, client_socket):
    server_socket = socket.socket(socket.AF_INET, server_type)
    server_adress = (SERVER_HOST, server_port)
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
        #Test this out
        body = response.read().decode()
        message = body.split('\r\n\r\n')[-1]
        cleaned_message = message.strip('"')
        print(cleaned_message)
        client_socket.sendall(cleaned_message.encode())
        
        conn.close()
    else:
        server_socket.sendto(data_json.encode(),server_adress)
    

    server_socket.close()


def get_server_by_name(server_name, rest_data, client_socket):
   
    server_port = SERVERS[server_name][0] #must be changed when I know how the http/https is determined
    
    try:
        match server_name:
            case "TCP-Server":
                connect_to_server(server_port, socket.SOCK_STREAM, rest_data, True, client_socket)
            case "UDP-Server":
                connect_to_server(server_port, socket.SOCK_DGRAM, rest_data, False, client_socket)
    except:
        raise Exception(f"Connecting to {server_name} unsuccessfull")


def handle_client_connection(client_socket):
    client_data = client_socket.recv(1024).decode()
    data_dict = json.loads(client_data)
    print("Received data from client:", client_data)
    get_server_by_name(data_dict.pop("Connect to"),data_dict, client_socket)
    

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
        handle_client_connection(client_socket)

receive_from_client()