import logging
from http.server import BaseHTTPRequestHandler, HTTPServer 

class requestHandler(BaseHTTPRequestHandler): 
    def do_GET(self): 
        logging.info(f"GET request received from {self.client_address}") 
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello, world!")

    