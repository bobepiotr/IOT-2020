import paho.mqtt.client as mqtt
terminal_id = "0"

broker = "hostname" #nazwa hosta
port = 8883 #port
client_m = mqtt.Client() #konstruktor dla klienta


def call_server(mess): #Wysłanie wiadomości do brokera
    client_m.publish("worker/name", mess) #Wysłanie wiadomości do brokera


def process_message(client, userdata, message):
    message_decoded = (str(message.payload.decode("utf-8"))).split(", ")  # dekodowanie wiadomości
    print(message_decoded[0])


def connect_to_broker(): #Połączenie z brokerem
    client_m.tls_set("ca.crt") #Uruchomienie TLS
    client_m.username_pw_set(username='client', password='password') #Autoryzacja
    client_m.connect(broker, port)  #Połączenie z brokerem
    client_m.on_message = process_message
    client_m.loop_start() #Uruchomienie głównego wątku
    client_m.subscribe("server/name")  #Zasubskrybowanie tematu "server/name"
    call_server("Client connected, TERMINAL "+terminal_id)   #Wysłanie wiadomości o połączeniu


def disconnect_from_broker():  #Odłączenie od brokera
    call_server("Client disconnected, TERMINAL "+terminal_id) #Wysłanie wiadomości do brokera
    client_m.disconnect()  #Odłączenie od brokera


def scan_card(card_id): #Symulacja skanowania karty
    #Wysyła do borkera wiadomość z numerem karty i numerem terminala
    call_server(str(card_id)+", "+terminal_id)
    return True


def run_client():
    connect_to_broker()
    main_app()   #uruchomienie interfejsu wiersza poleceń
    disconnect_from_broker()


def main_app():
    inp = ["tmp"] #tablica do któej zapisywane będą komendy
    pred = True #wartośc logiczna warunkująca zatrzymanie interfejsu
    print("----------TERMINAL----------")

    while pred: #Główna pętla
        inp = input().split(" ") #Wczytywanie komend z klawiatury

        if inp[0] == "scan":
            if scan_card(inp[1]):
                continue

        if inp[0] == "quit":
            pred = False

        else:
            print("Unknown command...")


if __name__ == "__main__":
    run_client()



