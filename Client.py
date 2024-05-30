import socket
import json

def get_load_balancer_ip():
    while True:
        load_balancer_ip: input("Enter the IP address of the load balancer: ") # type: ignore
        try:
            socket.inet_aton(load_balancer_ip)
            return load_balancer_ip
        except socket.error:
            print("Invalid IP address. Please enter a valid IP address")
