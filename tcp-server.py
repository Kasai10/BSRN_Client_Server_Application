import logging
from http.server import BaseHTTPRequestHandler, HTTPServer 
import argparse
import json

class requestHandler(BaseHTTPRequestHandler): 
    def do_GET(self): 
        self.respond_to_client(self, "GET")

    def do_PUT(self):
        self.handle_payload(self, "PUT")

    def do_POST(self):
        self.handle_payload(self, "POST")

    def do_DELETE(self):
        self.respond_to_client(self, "DELETE")

    def respond_to_client(self, type):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = json.dumps("Received " + type +  "-Request")
        self.wfile.write(response.encode())

    def handle_payload(self, type):
        message_length = int(self.headers['Content-Length'])
        self.respond_to_client(self, type)
        decoded_message = self.rfile.read(message_length).decode()


        

def main():
    parser = argparse.ArgumentParser(description='Start TCP Server')
    parser.add_argument('-logdatei', type=str, required=True, help='Log datei Pfad und Name')
    args = parser.parse_args()
    # '%(levelname)s' Schweregrad, '%(name)s' Namen des Loggers, '%(filename)s' Name der Datei '%(lineno)d' Zeilennummer
    logging.basicConfig(filename=args.logdatei, level=logging.INFO, format='%(asctime)s - %(message)s')
    
    server_address = ('localhost', 40)
    httpd = HTTPServer(server_address, requestHandler)

    logging.info("Starting TCP server on port 40")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    logging.info("Stopping TCP server")


if __name__ == "__main__":
    main()

    