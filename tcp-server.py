import logging
from http.server import BaseHTTPRequestHandler, HTTPServer 

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


    