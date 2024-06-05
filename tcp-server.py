import logging
import ssl
from http.server import BaseHTTPRequestHandler, HTTPServer 
import argparse
import json

class request_handler(BaseHTTPRequestHandler): 
    def do_GET(self): 
        self.respond_to_client(self, "GET")

    def do_PUT(self):
        self.handle_payload(self, "PUT")

    def do_POST(self):
        self.handle_payload(self, "POST")

    def do_DELETE(self):
        self.respond_to_client(self, "DELETE")

    def respond_to_client(self, method: str):
        try:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = json.dumps(f"Received {method} request for path: {self.path}")
            self.wfile.write(response.encode())

        except (Exception, json.JSONDecodeError) as e:
            logging.error(f"Error responding to {method} request: {e}")
            self.send_error(500, "Internal Server Error")

    def handle_payload(self, method: str):
        try:
            message_length = int(self.headers['Content-Length'])
            self.respond_to_client(self, type)
            payload = self.rfile.read(message_length).decode()
            logging.info(f"Received {method} request - Path: {self.path}, Payload: {payload}") 
            self.respond_to_client(self, method: str)
        except (ValueError, UnicodeDecodeError):  
            logging.error(f"Error processing request: {method}, Path: {self.path}")
            self.send_error(400, "Bad Request")  

              
          
def start_server():
    logging.basicConfig(filename="", level=logging.INFO, format='%(asctime)s  %(levelname)s %(message)s')
    logging.info("Starting TCP server on port 8080")
    
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, request_handler)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    except (OSError, socket.error) as e:
        logging.error(f"Server startup error: {e}")
    finally:
        httpd.server_close()
        logging.info("Stopping TCP server")

    httpd.server_close()
    logging.info("Stopping TCP server")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='TCP Server')
    parser.add_argument('-logdatei', type=str, required=True, help='Log datei Pfad und Name')
    args = parser.parse_args()
    start_server(args.log_file)

    