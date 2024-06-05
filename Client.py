import socket
import json

LOAD_BALANCER_HOST = "localhost"
LOAD_BALANCER_PORT = 9999


def get_server_type():
    while True:
        server_type = input("Choose a server (TCP or UDP): ").strip().upper()
        if server_type in ["TCP", "UDP"]:
            return f"{server_type}-Server"
        else:
            print("Invalid input. Please choose either TCP or UDP.")

def get_http_method(server_type):
    if server_type == "UDP-Server":
     return ""
    while True:
        method = input("Choose an HTTP method (GET, PUT, POST, DELETE): ").strip().upper() 
        if method in ["GET", "PUT", "POST", "DELETE"]:
            return method
        else:
            print("Invalid input. Please choose either GET, PUT, POST or DELETE. ")
            


def get_payload():
    server_type = get_server_type()
    method = get_http_method(server_type)
    message = input("Enter the message: ")
    payload = json.dumps({"Connect to": server_type, "Message": message, "Method": method})
    return payload


def send_message():
    try:
        payload = get_payload()
        communicate_with_load_balancer(payload)
    except Exception as e:
        print(f"An error has occurred: {e}")



def communicate_with_load_balancer(payload):
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect((LOAD_BALANCER_HOST, LOAD_BALANCER_PORT))
        tcp_socket.sendall(payload.encode())

        response = receive_response_from_tcp_server(tcp_socket)
        if response is not None:
            print("Response from the server:", response)

    finally:
        tcp_socket.close()


def receive_response_from_tcp_server(tcp_socket):
    try:
        response = tcp_socket.recv(4096)
        decoded_response = json.loads(response.decode())
        return decoded_response
    except socket.error as e:
        print(f"Error receiving the response from the server: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding the JSON response: {e}")
        return None
    


send_message()


        
        
        
