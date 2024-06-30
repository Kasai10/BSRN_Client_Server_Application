import socket
import json

LOAD_BALANCER_PORT = 8888
LOAD_BALANCER_HOST = "localhost"

#Prompt the user to choose a host and return the chosen host
def choose_host():
    host = input("Choose a host. Press Enter for default localhost or enter the load balancer IP address: ").strip()
    if not host:
        return LOAD_BALANCER_HOST
    else:
        return host

#Prompt the user to choose a server and return the selected server
def get_server_type():
    while True:
        server_type = input("Choose a server (TCP or UDP): ").strip().upper()
        if server_type in ["TCP", "UDP"]:
            return f"{server_type}-Server"
        else:
            print("Invalid input. Please choose either TCP or UDP.")

#Prompt the user to choose an HTTP method if the TCP server was selected
def get_http_method(server_type):
    #Returns empty string if server is a UDP server
    if server_type == "UDP-Server":
     return ""
    while True:
        method = input("Choose an HTTP method (GET, PUT, POST, DELETE): ").strip().upper() 
        if method in ["GET", "PUT", "POST", "DELETE"]:
            return method
        else:
            print("Invalid input. Please choose either GET, PUT, POST or DELETE. ")
          
#Creates and returns the JSON-encoded payload, server type and load balancer host
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

#Initiates a connection to the load balancer
def communicate_with_load_balancer(payload, server_type, load_balancer_host):
    try:
        #Creates a TCP socket
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Connects to the load balancer
        tcp_socket.connect((load_balancer_host, LOAD_BALANCER_PORT))
        #Sends the payload
        tcp_socket.sendall(payload.encode())
        print("[INFO] Payload sent to the load balancer.")
        
        #Receives response
        response = tcp_socket.recv(1024).decode()
        if response:
            if "TCP" in server_type:
                print("[INFO] Response from the TCP server:")
            elif "UDP" in server_type:
                print("[INFO] Response from the UDP server:")
            print(response)
        else:
            #Error handling
            print("[ERROR] No response received from the server.")
    except socket.error as e:
        print(f"[ERROR] Socket error: {e} ")
        #Closes socket
    finally:
            tcp_socket.close()

#Manages the sending of the message to the load balancer based on user inputs
def send_message():
    try:
        payload, server_type, load_balancer_host = get_payload()
        communicate_with_load_balancer(payload, server_type, load_balancer_host)
    except Exception as e:
        print(f"[ERROR] Payload could not be sent to the load balancer: {e}")

#Main program
print("\n--- Client Started ---\n")
#Loop to send messages until the user chooses to stop
while True:   
    send_message()
    continue_sending_requests = input("\nDo you want to send another request (yes/no)? ").strip().lower()
    if continue_sending_requests != "yes":
        print("\n--- Program Ended ---\n")
        break