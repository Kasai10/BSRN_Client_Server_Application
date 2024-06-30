import logging
from http.server import BaseHTTPRequestHandler, HTTPServer 
import argparse
import json

# Request handler class (inherits from BaseHTTPRequestHandler) to process Client requests
class RequestHandler(BaseHTTPRequestHandler): 
    
    # Process GET requests
    def do_GET(self):
        self.handle_payload("GET", "The resource was successfully retrieved.")

    # Process POST requests
    def do_POST(self):
        self.handle_payload("POST", "New resource successfully created.")

    # Process PUT requests
    def do_PUT(self):
        self.handle_payload("PUT", "The resource was successfully updated.")

    # Process DELETE requests
    def do_DELETE(self):
        self.handle_payload("DELETE", "The resource was successfully deleted.")

    # Common method to process the payload from each request type
    def handle_payload(self, method, response_message):
        try:
            # Log incoming request
            logging.info(f"Incoming {method} message from Client")
            print(f"{method} message received from Client")

            # Read and process payload for PUT and POST Requests
            if method in ['PUT', 'POST']:
                message_length = int(self.headers['Content-Length'])
                payload_json = self.rfile.read(message_length).decode()
                payload_dict = json.loads(payload_json)
                payload = f"- Message: {payload_dict['Message']} \n- Method: {payload_dict['Method']}"          
            
            # Process payload for GET and DELETE Requests
            else:
                payload = f"- Message: none \n- Method: {method}"
            
            # Calls respond_to_client() Method
            self.respond_to_client(method, response_message, payload)

        except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as e:  
            logging.error(f"Error processing {method} request: {e}")
            self.send_error(400, "Bad Request") 

    # Sends a response to the Client
    def respond_to_client(self, method, response_message, payload):
        try:
            # Send 200 Ok response
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()

            # Create and send response message
            response = f"TCP-Server received following request: \n{payload} \n{response_message}"
            self.wfile.write(response.encode())

            # Log response to Client
            logging.info(f"Following message sent to Client: \n{response}")
            print(f"{response_message}\n")

        # Log error if connection is reset by client before answer is possible
        except ConnectionResetError:
            logging.error(f"Connection reset by Client during {method} request")
            self.send_error(500, "Connection reset by client")
        except Exception as e:
            logging.error(f"Error responding to {method} request: {e}")
            self.send_error(500, "Internal Server Error")
        
        # Ensure all data is flushed before closing the connection
        finally:
            self.wfile.flush()  
 
    # Override and personalise log_request method
    def log_request(self, code='-', size='-'):
        logging.info(f"Request currently being handled: \n- Client IP Address: {self.client_address[0]} \n- Request details: {self.requestline}")

# Start server
def start_server():
    server_address = ('localhost', 8000)
    httpd = HTTPServer(server_address, RequestHandler)

    # Log server start
    start_info = "TCP-Server has started on port 8000"
    logging.info(start_info)
    print(start_info)

    # Run server indefinitely 
    try:
        httpd.serve_forever()
    
    # Server shutdown by user (ctrl+c)
    except KeyboardInterrupt:
        logging.info("Server shutdown initiated by user")
    
    except OSError as e:
        logging.error(f"Server startup error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error during server startup: {e}")
    
    # Close server and create Logfile entry
    finally:
        httpd.server_close()
        logging.info(f"TCP-Server is closed") 
        print("TCP-Server closed")  

 
# Start logging
def start_logging(log_file_path=None):
    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logging.info("TCP Server started logging")
    
# Main
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Server")
    parser.add_argument('-logdatei', dest="logfile", type=str, required=True, help='Logfile path and name')
    args = parser.parse_args()
    start_logging(args.logfile)
    start_server()


