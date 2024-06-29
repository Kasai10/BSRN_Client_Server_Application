import socket #Die bibliothek brauche ich natürlich um Zugriff auf Netzwerksockets zu erhalten und einen Netzwerkserver zu erstellen.
import logging #Damit ein feedback zum client via file entsteht
import argparse #Bibliothek fürs Logging
def loggingfunction(log_file_path): #Funktion, die das logging implementiert
        logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s%(levelname)s%(message)s')
        logging.info("UDP Server startet")
def server(port): #Hier eine Function, die dann die gesamte funktionalität des Servers umfasst
    buffersize = 4096 #Deklarieren von Buffersize für n die recvfrom Methode
    try:
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Hier wird dann halt das Socket als UDP Socket erstellt, der IPv4-Adressem benutzt.
        logging.info ("Ein neues Socket wurde erstellt") #Für die bessere Übersicht dann einfach nh response, dass das Socket erstellt worden ist, wenn alles glatt läuft
    except Exception as socketerror:
        logging.error(f"Das Erstellen des Sockets mit Port : {port} hat nicht funktioniert")
        return
    try:
        address=('localhost', port) #Festlegen  von Serveradresse und des Ports als Tupel für die bind methode
        socket1.bind(address) #Bindet das Socket an die Adresse.
        logging.info(f"Socket wurde an die Adresse {address} gebunden")
    except Exception as bindfailed:
         logging.error(f"Das Binden des Sockets an die Adresse {address} hat nicht geklappt")
         return
    
    while True: #Endlosschleife, wo der Server permanent auf neue Nachrichten wartet.
        try:
                message, addressloadbalancer = socket1.recvfrom(buffersize) #Wartet auf Nachricht, empfängt diese und gibt die nachricht und die Adresse zurück
        except Exception as receiveerror:
                logging.error("Die Nachricht konnte nicht Empfangen werden")
                continue
        try:    
                    decodedmessage = message.decode() #Hier wird die nachricht dann decodiert, weil sie normalerweise als Binärdaten empfangen wird.
                    logging.info(f"Empfangene Nachricht von {addressloadbalancer}: {decodedmessage}") 
        except Exception as decodeerror:
                   logging.error("Die nachricht konnte nicht entschlüsselt werden")
                   continue
        answer = f"status:success, message: Ihre Nachricht wurde entgegengenommen,data: {decodedmessage}"
                
        try:
            socket1.sendto(answer.encode(), addressloadbalancer) #Hier wird die antwort message zurück an den Loabalancer geleitet.
            logging.info(f"Die Antwort {answer} wurden an {addressloadbalancer} gesendet")
        except Exception as senderror:
            logging.error("Die Antwort konnte nicht versendet werden")    
            
if __name__=="__main__": #Das hier ist quasi eine Sicherheitsvorkehrung dass der Code nur ausgeführt wird wenn das Skript direkt ausgeführt wird, damit mien code nicht einfach startet.
    argumentparser = argparse.ArgumentParser(description="UDP-Server")
    argumentparser.add_argument('-logfile', dest='logfile', type=str, required=True, help='Pfad und Name der Lodatei')
    args =argumentparser.parse_args()
    loggingfunction(args.logfile)
    server(8887) 


    