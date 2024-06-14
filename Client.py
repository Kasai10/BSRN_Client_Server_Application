import socket
import json

LOAD_BALANCER_PORT = 9999
UDP_SERVER_PORT = 8887
BUFFER_SIZE = 4096

def print_header(header):
    print(f"\n--- {header} ---\n")


def choose_host():
    host = input("Choose a host. Press Enter for default localhost or enter the load balancer IP address: ").strip()
    if not host:
        return "localhost"
    else:
        return host


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
    load_balancer_host = choose_host()
    server_type = get_server_type()
    method = get_http_method(server_type)
    message = ""

    if method not in ["GET", "DELETE"]:
        message = input("Enter the message: ")

    payload = json.dumps({
        "IP Address": load_balancer_host,
        "Connect to": server_type,
        "Message": message,
        "Method": method
    })
    return payload, server_type, load_balancer_host


def send_message():
    try:
        payload, server_type, load_balancer_host = get_payload()
        communicate_with_load_balancer(payload, server_type, load_balancer_host)
    except Exception as e:
        print(f"An error has occurred: {e}")


def communicate_with_load_balancer(payload, server_type, load_balancer_host):
    tcp_socket = None
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect((load_balancer_host, LOAD_BALANCER_PORT))
        tcp_socket.sendall(payload.encode())
        print("[INFO] Payload sent to the load balancer.")

        if "TCP" in server_type:
            response = receive_response_from_tcp_server(tcp_socket)
            if response is not None:
                print("[INFO] Response from the TCP server:")
                print(response)
        elif "UDP" in server_type:
            receive_response_from_udp_server()
    except Exception as e:
        print(f"Payload couldn't be sent to the load balancer: {e}")
    finally:
        if tcp_socket:
           tcp_socket.close()


def receive_response_from_tcp_server(tcp_socket):
    try:
        response = tcp_socket.recv(1024).decode()
        return response
    except socket.error as e:
        print(f"Error receiving the response from the TCP server: {e}")


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
                print(f"[INFO] Response from the UDP server:")
                print(json.dumps(json_response))
            except json.JSONDecodeError as e:
                print(f"Error decoding the JSON response: {e}")
                

    except socket.error as e:
        print(f"Error receiving the response from the UDP server: {e}")
    finally:
        udp_socket.close()
    

if __name__ == "__main__":
    print_header("Client Application Started")
    while True:   
        send_message()
        continue_sending_requests = input("\nDo you want to send another request (yes/no)? ").strip().lower()
        if continue_sending_requests == "yes":
            print("\n")
        else:
            print_header("Program Ended")
            break

        
        
        
