import logging
from http.server import BaseHTTPRequestHandler, HTTPServer 
import argparse
import json

class request_handler(BaseHTTPRequestHandler): 
    def do_GET(self):
        antwort = "The resource was successfully retrieved." 
        self.handle_payload("GET", antwort)

    def do_PUT(self):
        antwort = "The resource was successfully updated."
        self.handle_payload("PUT", antwort)

    def do_POST(self):
        antwort = "New resource successfully created."
        self.handle_payload("POST", antwort)

    def do_DELETE(self):
        antwort = "The resource was successfully deleted."
        self.handle_payload("DELETE", antwort)

    def handle_payload(self, method, antwort):
        try:
            if method in ['PUT', 'POST']:
                message_length = int(self.headers['Content-Length'])
                payload = self.rfile.read(message_length).decode()

                payload_dict = json.loads(payload)
                payload = f"- Message: {payload_dict['Message']} \n- Method: {payload_dict['Method']}"
                
                self.respond_to_client(method, antwort, payload)
            else:
                payload = f"- Message: none \n- Method: {method}"
                self.respond_to_client(method, antwort, payload)
        except (ValueError, UnicodeDecodeError):  
            error_info = f"Error processing request: {method}, Path: {self.path}"
            logging.error(error_info)
            print(error_info)
            self.send_error(400, "Bad Request") 

    def respond_to_client(self, method, antwort, payload):
        try:
            print(f"Incoming {method} message from Client")
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = (f"TCP-Server received following request: \n{payload} \n{antwort}")
            self.wfile.write(response.encode())

            sent_info = f"Following message sent to client: \n{response}"
            logging.info(sent_info)
            print(sent_info)
        except ConnectionResetError:
            error_info = f"Connection reset by client during {method} request"
            logging.error(error_info)
            print(error_info)
            self.send_error(500, "Connection reset by client")
        except Exception as e:
            error_info = f"Error responding to {method} request: {e}"
            logging.error(error_info)
            print(error_info)
            self.send_error(500, "Internal Server Error")
        finally:
            self.wfile.flush()  # Ensure all data is flushed before closing the connection
            print("")
            
 
    def log_request(self, code='-', size='-'):
        status_info = f"Request currently being handled: \n- Client IP Address: {self.client_address[0]} \n- Request details: {self.requestline}"
        logging.info(status_info)
        print(status_info)

def start_server():
    server_address = ('localhost', 8000)
    httpd = HTTPServer(server_address, request_handler)
    start_info = f"TCP server has started on port 8000"
    logging.info(start_info)
    print(start_info)

    try:
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        pass
    except (OSError) as e:
        error_status = f"Server startup error: {e}"
        logging.error(error_status)
        print(error_status)
    finally:
        httpd.server_close()

    close_info = f"TCP Server is closed"    
    print(close_info)
    logging.info(close_info)


def start_logging(log_file_path=None):
    if log_file_path:
        logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
        start_info = "TCP Server started logging"
        logging.info(start_info)
        print(start_info)
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Server")
    parser.add_argument('-logdatei', dest="logfile", type=str, required=True, help='Logdatei Pfad und Name')
    args = parser.parse_args()
    start_logging(args.logfile)
    start_server()

