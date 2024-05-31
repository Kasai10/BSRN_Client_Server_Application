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
    payload = json.dumps({"message": message})
    return payload




        
        
        
