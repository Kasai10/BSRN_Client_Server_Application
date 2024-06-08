import logging
from http.server import BaseHTTPRequestHandler, HTTPServer 
import argparse
import json

class request_handler(BaseHTTPRequestHandler): 
    def do_GET(self): 
        self.respond_to_client("GET")

    def do_PUT(self):
        self.handle_payload("PUT")

    def do_POST(self):
        self.handle_payload("POST")

    def do_DELETE(self):
        self.respond_to_client("DELETE")


    def respond_to_client(self, method, payload):
        try:
            print(f"Incoming message from Client")
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            response = json.dumps(f"TCP-Server received {method} request, Payload: {payload}")
            response = response.replace('\\', '').replace('"', '')
            logging.info(f"Following message sent to client: {response}")
            self.wfile.write(response.encode())
            print(f"Following message sent to client: {response}")
        except ConnectionResetError:
            logging.error(f"Connection reset by client during {method} request")
            print(f"Connection reset by client during {method} request")
        except Exception as e:
            print(f"Error responding to {method} request: {e}")
            self.send_error(500, "Internal Server Error")
        finally:
            self.wfile.flush()  # Ensure all data is flushed before closing the connection
        
    def handle_payload(self, method):
        try:
            message_length = int(self.headers['Content-Length'])
            payload = self.rfile.read(message_length).decode()
            self.respond_to_client(method, payload)
        except (ValueError, UnicodeDecodeError):  
            logging.error(f"Error processing request: {method}, Path: {self.path}")
            self.send_error(400, "Bad Request")  


    def log_request(self, code='-', size='-'):
        logging.info(f"Request currently being handled: Client IP Address {self.client_address[0]}, Type: {self.requestline}")
        print(f"[{self.log_date_time_string()}] Client IP: {self.client_address[0]}, Request details: {self.requestline} ")

def start_server():
 
    server_address = ('localhost', 8000)
    httpd = HTTPServer(server_address, request_handler)
    logging.info(f"TCP server has started on port 8000")
    print(f"TCP server has started on port 8000")

    try:
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        pass
    except (OSError) as e:
        logging.error(f"Server startup error: {e}")
        print("Server startup error:  {e}")
    finally:
        httpd.server_close()
        logging.info("Stopping TCP server")

    httpd.server_close()

    print("Server is closed")
    logging.info("Stopping TCP server")


def start_logging(log_file_path=None):
    if log_file_path:
        logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
        logging.info("Starting logging")
        print("Starting logging")
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Server")
    parser.add_argument('-logdatei', dest="logfile", type=str, required=True, help='Log datei Pfad und Name')
    args = parser.parse_args()
    start_logging(args.logfile)
    start_server()

    