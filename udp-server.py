import socket #Die bibliothek brauche ich natürlich um Zugriff auf Netzwerksockets zu erhalten und einen Netzwerkserver zu erstellen.
import logging #Damit ein feedback zum client via file entsteht
import json #Nachrichtenformat
import argparse
def loggingfunction(log_file_path=None):
    if log_file_path:
        logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s%(levelname)s%(message)s')
        logging.info("UDP Server startet")
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s%(levelname)s%(message)s')   
def server(port): #hier mach ich den Port als parameter mal lieber in eine funktion um das ganze dynamischer und bisschen ordentlicher zu gestalten 
    buffersize = 4096 # Hier wird dann die Buffer size deklariert in höhe von 4096 bytes, da dies eine standartmässige verwendung für UDP Datagramme hat und ich die Puffregrösse definitv auch für die recvform methode brauchen werde
    try:
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Hier wird dann halt das Socket als UDP Socket erstellt, der IPv4-Adressem benutzt.
        print("Benachrichtigung eines neuen erstellten sockets")
        logging.info ("Ein neues Socket wurde erstellt") #Für die bessere Übersicht dann einfach nh response, dass das Socket erstellt worden ist, wenn alles glatt läuft
    except Exception as socketfehler:
        logging.error(f"Das Erstellen des Sockets mit Port : {port} hat nicht funktioniert")
        return
    try:
        adresse=('localhost', port) #Hier deklariere ich eine neue variable, die einfach die server adresse ist. Port wie gesagt, die portnummer, die in der funktion vom user deklariert wird und dann ein leerer string, wodurch dann alle IP-Adressen eine Verbindung zum Server aufbauen können. Ausserdem ist ein Tupel hier glaube ich erforderlich, weil die methode bind soweit ich weiss nur bei tupel funktioniert
        socket1.bind(adresse) #Damit das Betriebssystem dann weiss, dass alle packets, die an dem vom user gegebenen Ports gesendet werden auch an das Socket weitergeschickt werden sollen.
        logging.info(f"Socket wurde an die Adresse {adresse} gebunden")
        print("Benachrichtigung, dass das socket an die adresse gebindet wurde")
    except Exception as bindfehlgeschlagen:
         logging.error(f"Das Binden des Sockets an die Adresse {adresse} hat nicht geklappt")
         return
    
    while True: #Hier geht es dann in die Schleife, wodurch der Server dann permanent auf eine neue Nachricht warten kann.  
        try:
                nachricht, adresseclient = socket1.recvfrom(buffersize) #Hier ist eine Methode, die quasi den Code anhält und unterbricht, bis eine Nachricht ankommt. Bisher nur als Bytearray
        except Exception as nachrichtempfangen:
                logging.error("Die Nachricht konnte nicht Empfangen werden")
                continue

        try:    
                    konkretenachricht = nachricht.decode() #Hier wird die nachricht dann decodiert, weil sie normalerweise als Binärdaten empfangen wird.
                    logging.info(f"Empfangene Nachricht von {adresseclient}: {nachricht.decode()}") 
        except Exception as Dekodierungsfehler:
                   logging.error("Die nachricht konnte nicht entschlüsselt werden")
                   continue
        antwort = {
                "status":"success",
                "message":"Ihre Nachricht wurde entgegengenommen",
                "data": konkretenachricht
                } 
        try:
                jsonantwort = json.dumps(antwort)
        except Exception as Jsonantowrtfehler:
                logging.error("Die Json-Antwort konnte nicht erstellt werden")
                jsonantwort=json.dumps({"status": "error", "message": "Antwort konnte nicht erstellt werden"})   
        try:
            loadbalanceradresse = ('localhost', 8888)
            socket1.sendto(jsonantwort.encode(), loadbalanceradresse) 
            print("Die nachricht sollte nun versendet worden sein an den Client")
            logging.info(f"Die Antwort {jsonantwort} wurden an {loadbalanceradresse} gesendet")
        except Exception as sendefehler:
            logging.error("Die Antwort konnte nicht versendet werden") 
            print(sendefehler)   
            
if __name__=="__main__": #Das hier ist quasi eine Sicherheitsvorkehrung dass das Skript hier nur in bestimmten massen ausgeführt wird, damit mien code nicht einfach startet ohne beispielsweise eine portnummer zu haben
    argumentparser = argparse.ArgumentParser(description="UDP-Server")
    argumentparser.add_argument('-logdatei', dest='logdatei', type=str, required=True, help='Pfad und Name der Lodatei')
    args =argumentparser.parse_args()
    loggingfunction(args.logdatei)
    server(8887) 


    