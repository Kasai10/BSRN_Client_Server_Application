import socket #Library to access sockets and create an network server
import logging #Library to create a logfile which provides us with feedback 
import argparse #Library to parse commandline arguments
def loggingfunction(log_file_path): #Function which implements logging
        logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s%(levelname)s%(message)s')
        logging.info("UDP Server is starting")
def server(port): #Function that has the main server operations
    buffersize = 4096 #Sets buffersize for the receiving method
    try:
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Creates a UDP socket for IPv4 addresses.
        logging.info ("A new socket was created") 
    except Exception as socketerror:
        logging.error(f"Couldnt create socket on  Port : {port}")
        return
    try:
        address=('localhost', port) #Sets the server address and the port
        socket1.bind(address) #Binds the socket to the address
        logging.info(f"Socket was bound to the address {address}")
    except Exception as bindfailed:
         logging.error(f"Failed to bind the socket to the address {address}")
         return
    
    while True: #Infinite loop where the server waits for new messages
        try:
                message, addressloadbalancer = socket1.recvfrom(buffersize) #Waits for a message, receives it and returns the message and address.
        except Exception as receiveerror:
                logging.error("The message could not be received")
                continue
        try:    
                    decodedmessage = message.decode() #Decodes message since it will be received as binary data.
                    logging.info(f"Received message from {addressloadbalancer}: {decodedmessage}") 
        except Exception as decodeerror:
                   logging.error("Failed to decode the message")
                   continue
        answer = f"status:success, message: your message has been received, data: {decodedmessage}"
                
        try:
            socket1.sendto(answer.encode(), addressloadbalancer) #Here the message will be send back to the loadbalancer
            logging.info(f"The response {answer} was sent to {addressloadbalancer}")
        except Exception as senderror:
            logging.error("Failed to send the response")    
            
if __name__=="__main__": #This part ensures the code runs only if the script is executed directly
    argumentparser = argparse.ArgumentParser(description="UDP-Server")
    argumentparser.add_argument('-logfile', dest='logfile', type=str, required=True, help='Path and Name of the logfile')
    args =argumentparser.parse_args()
    loggingfunction(args.logfile)
    server(8887) 


    