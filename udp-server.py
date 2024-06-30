import socket #Library to access sockets and create an network server
import logging #Library to create a logfile which provides us with feedback 
import argparse #Library to parse commandline arguments
def loggingfunction(log_file_path): #Function which implements logging
        logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s%(levelname)s%(message)s')
        logging.info("UDP Server startet")
def server(port): #Function that has the main server operations
    buffersize = 4096 #Sets buffersize for the receiving method
    try:
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Creates a UDP socket for IPv4 addresses.
        logging.info ("Ein neues Socket wurde erstellt") 
    except Exception as socketerror:
        logging.error(f"Das Erstellen des Sockets mit Port : {port} hat nicht funktioniert")
        return
    try:
        address=('localhost', port) #Sets the server address and the port
        socket1.bind(address) #Binds the socket to the address
        logging.info(f"Socket wurde an die Adresse {address} gebunden")
    except Exception as bindfailed:
         logging.error(f"Das Binden des Sockets an die Adresse {address} hat nicht geklappt")
         return
    
    while True: #Infinite loop where the server waits for new messages
        try:
                message, addressloadbalancer = socket1.recvfrom(buffersize) #Waits for a message, receives it and returns the message and address.
        except Exception as receiveerror:
                logging.error("Die Nachricht konnte nicht Empfangen werden")
                continue
        try:    
                    decodedmessage = message.decode() #Decodes message since it will be received as binary data.
                    logging.info(f"Empfangene Nachricht von {addressloadbalancer}: {decodedmessage}") 
        except Exception as decodeerror:
                   logging.error("Die nachricht konnte nicht entschlüsselt werden")
                   continue
        answer = f"status:success, message: Ihre Nachricht wurde entgegengenommen,data: {decodedmessage}"
                
        try:
            socket1.sendto(answer.encode(), addressloadbalancer) #Here the message will be send back to the loadbalancer
            logging.info(f"Die Antwort {answer} wurden an {addressloadbalancer} gesendet")
        except Exception as senderror:
            logging.error("Die Antwort konnte nicht versendet werden")    
            
if __name__=="__main__": #This part ensures the code runs only if the script is executed directly
    argumentparser = argparse.ArgumentParser(description="UDP-Server")
    argumentparser.add_argument('-logfile', dest='logfile', type=str, required=True, help='Pfad und Name der Lodatei')
    args =argumentparser.parse_args()
    loggingfunction(args.logfile)
    server(8887) 


    