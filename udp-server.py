import socket #Die bibliothek brauche ich natürlich um Zugriff auf Netzwerksockets zu erhalten und einen Netzwerkserver zu erstellen.
import sys # Damit man kommandozeilenargumente lesen kann und das Programm beenden kann
import logging #Damit ein feedback zum client via file entsteht
import json #Nachrichtenformat
def server(ports): #hier mach ich den Port als parameter mal lieber in eine funktion um das ganze dynamischer und bisschen ordentlicher zu gestalten 
    buffersize = 4096 # Hier wird dann die Buffer size deklariert in höhe von 4096 bytes, da dies eine standartmässige verwendung für UDP Datagramme hat und ich die Puffregrösse definitv auch für die recvform methode brauchen werde
    socketlist = []
    for port in ports:    #Nun soll der server nicht nur auf eine portnummer sondern auf mehreren lauschen, weswegen ich hier nh schleife eingebaut habe die immer aus der liste ports die portnnummern entnimmt und in die variable port steckt und dann die nachricht durchgeht
     try:
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Hier wird dann halt das Socket als UDP Socket erstellt, der IPv4-Adressem benutzt.
        print ("Ein neues Socket wurde erstellt") #Für die bessere Übersicht dann einfach nh response, dass das Socket erstellt worden ist, wenn alles glatt läuft
        socketlist.append(socket1) #Brauchen natürlich noch eine methode, wo ein neues socket dann überhaupt erst in die Liste hinzugefügt wird.
     except Exception as socketfehler:
        print("Das Erstellen des Sockets mit Port : {Port} hat nicht funktioniert")
        continue
     adresse=('', port) #Hier deklariere ich eine neue variable, die einfach die server adresse ist. Port wie gesagt, die portnummer, die in der funktion vom user deklariert wird und dann ein leerer string, wodurch dann alle IP-Adressen eine Verbindung zum Server aufbauen können. Ausserdem ist ein Tupel hier glaube ich erforderlich, weil die methode bind soweit ich weiss nur bei tupel funktioniert
     socket1.bind(adresse) #Damit das Betriebssystem dann weiss, dass alle packets, die an dem vom user gegebenen Ports gesendet werden auch an das Socket weitergeschickt werden sollen.
    
    while True: #Hier geht es dann in die Schleife, wodurch der Server dann permanent auf eine neue Nachricht warten kann. 
        for socket1 in socketlist: #Da wir nun mit mehreren Ports arbeiten wollen, brauchen wir auch mehrere sockets, weswegen wir zuvor eine liste implementiert haben, welche hier iteriert wird.
            

            nachricht, adresseclient = socket1.recvfrom(buffersize) #Hier ist eine Methode, die quasi den Code anhält und unterbricht, bis eine Nachricht ankommt. Bisher nur als Bytearray
            try:    
                    konkretenachricht = nachricht.decode() #Hier wird die nachricht dann decodiert, weil sie normalerweise als Binärdaten empfangen wird.
                    print(f"Empfangene Nachricht von {adresseclient}: {nachricht.decode()}") 
            except Exception as Dekodierungsfehler:
                   print("Die nachricht konnte nicht entschlüsselt werden")
                   continue
            antwort = {
                "status":"success",
                "message":"Ihre Nachricht wurde entgegengenommen",
                "data": konkretenachricht
                } 
            try:
                jsonantwort = json.dumps(antwort)
            except Exception as Jsonantowrtfehler:
                print("Die Json-Antwort konnte nicht erstellt werden")
            continue
        try:
            socket1.sendto(antwort.encode(), adresseclient) 
        except Exception as sendefehler:
            print("Die Antwort konnte nicht versendet werden")    
            
if __name__=="__main__": #Das hier ist quasi eine Sicherheitsvorkehrung dass das Skript hier nur in bestimmten massen ausgeführt wird, damit mien code nicht einfach startet ohne beispielsweise eine portnummer zu haben
    portnummern = [8000, 8001, 8002] #Ich hab hier einfach mal eine kleiner gruppe an Ports ausgewählt, da der loadbalacner ja wissen muss welche Ports zum UDP server führen.
    server(portnummern) 


    