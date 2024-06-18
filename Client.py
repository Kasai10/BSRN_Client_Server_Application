import socket
import json

LOAD_BALANCER_PORT = 8888


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

        response = tcp_socket.recv(1024).decode()
        if response:
            if "TCP" in server_type:
                print("[INFO] Response from the TCP server:")
            elif "UDP" in server_type:
                print("[INFO] Response from the UDP server:")
            print(response)
        else:
            print("[ERROR] No response received from the server.")
     
    except socket.error as e:
        print(f"[ERROR] Socket error: {e} ")
    except Exception as e:
        print(f"[ERROR] Failed to communicate to the load balancer: {e}")
    finally:
        if tcp_socket:
            tcp_socket.close()

    

if __name__ == "__main__":
    print_header("Client Application Started")
    while True:   
        send_message()
        continue_sending_requests = input("\nDo you want to send another request (yes/no)? ").strip().lower()
        if continue_sending_requests != "yes":
            print_header("Program Ended")
            break