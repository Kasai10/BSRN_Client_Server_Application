import socket #Die bibliothek brauche ich natürlich um Zugriff auf Netzwerksockets zu erhalten und einen Netzwerkserver zu erstellen.
import sys # Damit man kommandozeilenargumente lesen kann und das Programm beenden kann
def server(port): #hier mach ich den Port als parameter mal lieber in eine funktion um das ganze dynamischer und bisschen ordentlicher zu gestalten 
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Hier wird dann halt das Socket als UDP Socket erstellt, der IPv4-Adressem benutzt.
    print ("Ein neues Socket wurde erstellt") #Für die bessere Übersicht dann einfach nh response, dass das Socket erstellt worden ist, wenn alles glatt läuft
          
adresse=('', port) #Hier deklariere ich eine neue variable, die einfach die server adresse ist. Port wie gesagt, die portnummer, die in der funktion vom user deklariert wird und dann ein leerer string, wodurch dann alle IP-Adressen eine Verbindung zum Server aufbauen können. Ausserdem ist ein Tupel hier glaube ich erforderlich, weil die methode bind soweit ich weiss nur bei tupel funktioniert
socket1.bind(adresse) #Damit das Betriebssystem dann weiss, dass alle packets, die an dem vom user gegebenen Ports gesendet werden auch an das Socket weitergeschickt werden sollen.
buffersize = 4096 # Hier wird dann die Buffer size deklariert in höhe von 4096 bytes, da dies eine standartmässige verwendung für UDP Datagramme hat und ich die Puffregrösse definitv auch für die recvform methode brauchen werde
while True: #Hier geht es dann in die Schleife, wodurch der Server dann permanent auf eine neue Nachricht warten kann. 
    nachricht, adresseclient = socket1.recvfrom(buffersize) #Hier ist eine Methode, die quasi den Code anhält und unterbricht, bis eine Nachricht ankommt. Bisher nur als Bytearray
    konkretenachricht = nachricht.decode() #Hier wird die nachricht dann decodiert, weil sie normalerweise als Binärdaten empfangen wird.
    print(f"Empfangene Nachricht von {adresseclient}: {nachricht.decode()}") #