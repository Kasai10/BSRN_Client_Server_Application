import socket
import json

def get_load_balancer_ip():
    while True:
        load_balancer_ip: input("Enter the IP address of the load balancer: ")  # type: ignore
        try:
            socket.inet_aton(load_balancer_ip)
            return load_balancer_ip
        except socket.error:
            print("Invalid IP address. Please enter a valid IP address")


def get_load_balancer_port():
    while True:
        port_input: input("Enter the port number of the load balancer: ")  # type: ignore
        try:
            load_balancer_port = int(port_input)
            return load_balancer_port
        except ValueError:
            print("Invalid input for port number. Please enter a valid number.")



def get_hostname_from_ip(load_balancer_ip):
    try:
        hostname = socket.gethostbyname(load_balancer_ip)
        print (f"The hostname for the IP address {load_balancer_ip} is {hostname}")
        return hostname
    except socket.gaierror as e:
        print(f"Error converting IP address: {e} ")
        return None
    

def get_server_type():
    while True:
        server_type = input("Choose a server (TCP or UDP): ").strip().upper()
        if server_type in ["TCP", "UDP"]:
            return server_type
        else:
            print("Invalid input. Please choose either TCP or UDP.")
            


def get_payload():
    message = input("Enter the message: ")
    server_type = get_server_type()
    payload = json.dumps({"message": message, "\Connect to": server_type})
    return payload


def send_message():
    try:
        load_balancer_ip = get_load_balancer_ip()
        load_balancer_port = get_load_balancer_port()

        payload = get_payload()
        server_type = payload.get("Connect to")

        if server_type == "TCP":
            communicate_with_tcp_server(load_balancer_ip, load_balancer_port, payload)
        elif server_type == "UDP":
            communicate_with_udp_server(load_balancer_ip, load_balancer_port, payload)

    except Exception as e:
        print(f"An error has occurred: {e}")



def communicate_with_tcp_server(load_balancer_ip, load_balancer_port, payload):
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect((load_balancer_ip, load_balancer_port))

        tcp_socket.sendall(payload.encode())

        response = tcp_socket.recv(1024)
        response_data = json.loads(response.decode())

        print(f"Response from the server: {response_data}")
    except json.JSONDecodeError:
        print("Error while decoding the JSON response from the server")
    except socket.error as e:
        print(f"Socket error on the TCP server: {e}")
    finally:
        tcp_socket.close()


def communicate_with_udp_server(load_balancer_ip, load_balancer_port, payload):
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        udp_socket.sendto(payload.encode(), (load_balancer_ip, load_balancer_port))

        response, _ = udp_socket.recvfrom(1024)
        response_data = json.loads(response.decode())

        print(f"Response from the server: {response_data}")
    except json.JSONDecodeError:
        print("Error while decoding the JSON response from the server")
    except socket.error as e:
        print(f"Socket error on the TCP server: {e}")
    finally:
        udp_socket.close()

    

send_message()


        
        
        
