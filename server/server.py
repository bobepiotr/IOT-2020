import server_logic as ser
from datetime import datetime

import paho.mqtt.client as mqtt


broker = "hostname" #nazwa hosta
port = 8883 #numer portu
client = mqtt.Client() #konstruktor dla klienta


def call_client(mess):
    client.publish("server/name", mess)


def process_message(client, userdata, message):  #deodowanie i przetworzenie wiadomości
    message_decoded = (str(message.payload.decode("utf-8"))).split(", ") #dekodowanie wiadomości
    if message_decoded[0] != "Client connected" and message_decoded[0] != "Client disconnected":
        # drukowanie komunikatu
        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ", " +
              message_decoded[0] + " used on the terminal "+message_decoded[1]+".")
        #aktualizacja historii zdarzeń
        if ser.scan_card(int(message_decoded[1]), int(message_decoded[0])):
            call_client("Card " + message_decoded[0] + " scanned.")
        else:
            call_client("Something went wrong")
    else:
        print(message_decoded[0] + " : " + message_decoded[1])


def connect_to_broker(): #Połączenie z brokerem
    client.tls_set("ca.crt") #Uruchomienie TLS
    client.username_pw_set(username='server', password='pass') #Autoryzacja
    client.connect(broker, port) #Połączenie z brokerem
    client.on_message = process_message #Odpowiedź serwera na wiadomość
    client.loop_start() #Uruchomienie głównego wątku
    client.subscribe("worker/name") #Subskrybowanie tematu "worker/name"
    call_client("Server ON")


def disconnect_from_broker():   #Odłączenie od brokera
    call_client("Server OFF")
    client.loop_stop()  #Zatrzymanie wątku głównego
    client.disconnect()  #odłączenie od brokera


def run_receiver():   #Rozpoczęcie pracy serwera
    connect_to_broker()
    main_app()  #Uruchamia menu wiersza poleceń
    disconnect_from_broker()


def initialize():
    ser.open_terminals_db()
    ser.open_card_db()
    print("Terminals: "+str(ser.terminals))
    print("Registered cards: "+str(ser.cards))


def main_app():
    initialize()
    inp = ["tmp"] #Tablica do któej zapisywane będą komendy
    pred = True #Wartośc logiczna warunkująca zatrzymanie interfejsu
    print("----------SERWER----------")
    while pred: #Pętla główna
        inp = input().split(" ")
        print(">")
        if inp[0] == "save": #zapisywanie
            if inp[1] == "terminals":
                if ser.save_terminals_db():
                    print("List of terminals has been saved")
                    continue
            elif inp[1] == "cards":
                if ser.save_cards_db():
                    print("List of cards has been saved")
                    continue
            elif inp[1] == "all":
                if ser.save_cards_db() and ser.save_terminals_db():
                    print("Both lists were saved")
                    continue
        if inp[0] == "add": #dodawanie nowych terminali i kart
            if inp[1] == "terminal":
                if ser.add_terminal(int(inp[2])):
                    print("Terminal " + inp[2] + " has been added")
                    continue
            elif inp[1] == "card":
                if ser.add_card(int(inp[2])):
                    print("Card " + inp[2] + " has been added")
                    continue
        if inp[0] == "del": #usuwanie terminali i kart
            if inp[1] == "terminal":
                if ser.remove_terminal(int(inp[2])):
                    print("Terminal "+inp[2]+" has been removed")
                    continue
            elif inp[1] == "card":
                if ser.remove_card(int(inp[2])):
                    print("Card " + inp[2] + " has been removed")
                    continue
        if inp[0] == "attach": #przypisywanie karty do użytkownika
            if inp[1] == "card":
                if ser.attach_card(inp[2]+" "+inp[3], int(inp[4])):
                    print("Card "+inp[4]+" has been assigned to the employee named "+inp[2]+" "+inp[3])
                    continue
        if inp[0] == "unattach": #odpisywanie karty od użytkownika
            if inp[1] == "card":
                if ser.unattach_card(int(inp[2])):
                    print("Employee has been removed from card " + str(inp[2]))
                    continue
        '''if inp[0] == "scan":                                   #skanowanie karty
            if (ser.scan_card(int(inp[1]), int(inp[2]))):
                print("Card has been scanned.")
                continue'''
        if inp[0] == "print": #wyświetlanie listy terminali, kart i historii
            if inp[1] == "terminals":
                print(ser.terminals)
                continue
            elif inp[1] == "cards":
                print(ser.cards)
                continue
            elif inp[1] == "log":
                ser.print_history()
                continue
            elif inp[1] == "report":
                print("--------------REPORT--------------")
                ser.print_report(inp[2]+" "+inp[3])
                print("----------------------------------")
                continue
        if inp[0] == "generate": #generowanie raportu
            if inp[1] == "report":
                if ser.generate_report(inp[2]+" "+inp[3]):
                    print("Report has been generated")
                continue
        if inp[0] == "quit":
            pred = False
            continue
        else:
            print("Unknown command")


if __name__ == "__main__":
    run_receiver()