import socket #Die bibliothek brauche ich natürlich um Zugriff auf Netzwerksockets zu erhalten und einen Netzwerkserver zu erstellen.
import sys # Damit man kommandozeilenargumente lesen kann und das Programm beenden kann
def server(ports): #hier mach ich den Port als parameter mal lieber in eine funktion um das ganze dynamischer und bisschen ordentlicher zu gestalten 
    buffersize = 4096 # Hier wird dann die Buffer size deklariert in höhe von 4096 bytes, da dies eine standartmässige verwendung für UDP Datagramme hat und ich die Puffregrösse definitv auch für die recvform methode brauchen werde
    socketlist = []
    for port in ports:    #Nun soll der server nicht nur auf eine portnummer sondern auf mehreren lauschen, weswegen ich hier nh schleife eingebaut habe die immer aus der liste ports die portnnummern entnimmt und in die variable port steckt und dann die nachricht durchgeht
     socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Hier wird dann halt das Socket als UDP Socket erstellt, der IPv4-Adressem benutzt.
     print ("Ein neues Socket wurde erstellt") #Für die bessere Übersicht dann einfach nh response, dass das Socket erstellt worden ist, wenn alles glatt läuft
   
     adresse=('', port) #Hier deklariere ich eine neue variable, die einfach die server adresse ist. Port wie gesagt, die portnummer, die in der funktion vom user deklariert wird und dann ein leerer string, wodurch dann alle IP-Adressen eine Verbindung zum Server aufbauen können. Ausserdem ist ein Tupel hier glaube ich erforderlich, weil die methode bind soweit ich weiss nur bei tupel funktioniert
     socket1.bind(adresse) #Damit das Betriebssystem dann weiss, dass alle packets, die an dem vom user gegebenen Ports gesendet werden auch an das Socket weitergeschickt werden sollen.
    
    while True: #Hier geht es dann in die Schleife, wodurch der Server dann permanent auf eine neue Nachricht warten kann. 
        for socket1 in socketlist: #Da wir nun mit mehreren Ports arbeiten wollen, brauchen wir auch mehrere sockets, weswegen wir zuvor eine liste implementiert haben, welche hier iteriert wird.
            nachricht, adresseclient = socket1.recvfrom(buffersize) #Hier ist eine Methode, die quasi den Code anhält und unterbricht, bis eine Nachricht ankommt. Bisher nur als Bytearray
            konkretenachricht = nachricht.decode() #Hier wird die nachricht dann decodiert, weil sie normalerweise als Binärdaten empfangen wird.
            print(f"Empfangene Nachricht von {adresseclient}: {nachricht.decode()}") 
            antwort = "UDP: Ihre Nachricht wurde entgegengenommen"#Hier wird dann eine variable erstellt, die später dann als feedback an den client geschickt wird
            socket1.sendto(antwort.encode(), adresseclient) 
    
if __name__=="__main__": #Das hier ist quasi eine Sicherheitsvorkehrung dass das Skript hier nur in bestimmten massen ausgeführt wird, damit mien code nicht einfach startet ohne beispielsweise eine portnummer zu haben
    if len(sys.argv)<2: #Da ja immer skript name und das skript selbst sowie die portnumer angegeben werden müssen, kann man durch die if anweisung hier prüfen ob eine portnummer vorhanden ist
        print ("Geben Sie eine Portnumber an")
        sys.exit(2) #Hab jetzt einfach 2 als rückgabewert zurückgeben lassen als feedback 


    portnummern = [int(port) for port in sys.argv[1:]] #List-comprehension 
    server(portnummern) 


    