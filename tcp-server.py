import logging
from http.server import BaseHTTPRequestHandler, HTTPServer 
import argparse

class requestHandler(BaseHTTPRequestHandler): 
    def do_GET(self): 
        logging.info(f"GET request received from {self.client_address}") 
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello, world!")

    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        logging.info(f"PUT request received from {self.client_address}, Payload: {post_data.decode()}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Received PUT request")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data_decoded = post_data.decode()
        logging.info(f"POST request received from {self.client_address}, Payload: {post_data_decoded}") 

    def do_DELETE(self):
        logging.info(f"DELETE request received from {self.client_address}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Received DELETE request")     

def main():
    parser = argparse.ArgumentParser(description='Start TCP Server')
    parser.add_argument('-logdatei', type=str, required=True, help='Log datei Pfad und Name')
    args = parser.parse_args()
    # '%(levelname)s' Schweregrad, '%(name)s' Namen des Loggers, '%(filename)s' Name der Datei '%(lineno)d' Zeilennummer
    logging.basicConfig(filename=args.logdatei, level=logging.INFO, format='%(asctime)s - %(message)s')
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, requestHandler)

    logging.info("Starting TCP server on port 8080")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    logging.info("Stopping TCP server")

if __name__ == "__main__":
    main()

    