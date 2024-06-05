import socket
import json

LOAD_BALANCER_HOST = "localhost"
LOAD_BALANCER_PORT = 9999
UDP_SERVER_PORT = 8887
BUFFER_SIZE = 4096


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
            print("Response from the TCP server:")
            print(json.dumps(response, indent=4))
    except Exception as e:
        print(f"Error communicating to the load balancer: {e}")
    finally:
        tcp_socket.close()


def receive_response_from_tcp_server(tcp_socket):
    try:
        response = tcp_socket.recv(4096)
        decoded_response = json.loads(response.decode())
        print(json.loads(decoded_response))
        return decoded_response
    except socket.error as e:
        print(f"Error receiving the response from the  TCP server: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding the JSON response: {e}")
    

def receive_response_from_udp_server():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('', UDP_SERVER_PORT))
    print(f"Listening for UDP response on port {UDP_SERVER_PORT}...")

    try:
        while True:
            message, server_address = udp_socket.recvfrom(BUFFER_SIZE)
            decoded_message = message.decode()
            try:
                json_response = json.loads(decoded_message)
                print(f"Response from the UDP server:")
                print(json.dumps(json_response, indent=4))
            except json.JSONDecodeError as e:
                print(f"Error decoding the JSON response: {e}")
                print(f"Raw response from UDP server: {decoded_message}")

    except socket.error as e:
        print(f"Error receiving the response from the UDP server: {e}")
    finally:
        udp_socket.close()
    


if __name__ == "__main__":
    send_message()
    receive_response_from_udp_server()


        
        
        
