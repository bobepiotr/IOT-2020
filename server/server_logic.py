import csv
from datetime import datetime

terminals = []
cards = {}


def open_card_db():  # dodwanie do listy danych z pliku z numerami kart
    with open('./simple_db/cards_db.csv') as file:
        rdr = csv.reader(file, delimiter=',')
        for line in rdr:
            cards[int(line[0])] = line[1]


def open_terminals_db():  # dodawanie do listy danych z pliku z numerami terminali
    with open('./simple_db/terminals_db.csv') as file:
        for line in file:
            terminals.append(int(line[0]))


def save_terminals_db():  # zapisywanie listy terminali do pliku z numerami terminali
    with open('./simple_db/terminals_db.csv', 'w') as file:
        for i in range(len(terminals)):
            file.write(str(terminals[i]))
            if i != len(terminals) - 1:
                file.write("\n")
    return True


def save_cards_db():  # zapisywanie listy kart do pliku z numerami kart
    with open('./simple_db/cards_db.csv', 'w') as file:
        for key in cards:
            file.write(str(key) + "," + cards[key] + "\n")
    return True


def add_terminal(terminal_id):  # dodawanie terminala do listy terminali
    if terminal_id in terminals:
        return False
    else:
        terminals.append(terminal_id)
        return True


def remove_terminal(terminal_id):  # usuwanie terminala
    if terminal_id in terminals:
        terminals.remove(terminal_id)
        return True
    else:
        return False


def add_card(card_id):  # dodawanie karty
    if card_id not in cards.keys():
        cards[card_id] = "unknown"  # karta po jej dodaniu nie ma przypisanego pracownika
        return True
    else:
        return False


def remove_card(card_id):  # usuwanie karty
    if card_id in cards.keys():
        del cards[card_id]
        return True
    else:
        return False


def attach_card(user_name, card_id):  # przypisywanie karty do użytkownika
    if card_id in cards.keys():
        if cards[card_id] != "unknown":
            return False
        else:
            cards[card_id] = user_name
            return True
    else:
        return False


def unattach_card(card_id):  # anulowanie przypisania karty do użytkownika
    if card_id in cards.keys():
        cards[card_id] = "unknown"
        return True
    else:
        return False


def scan_card(terminal_id, card_id):  # symulacja skanowania karty
    if terminal_id in terminals:
        if card_id in cards.keys():
            update_history(terminal_id, card_id, cards[card_id])
        else:
            update_history(terminal_id, card_id, "UNKNOWN CARD ")
        return True
    return False


def update_history(terminal_id, card_id, user_name):  # aktualizacja historii, czyli pliku z historią zdarzeń
    with open('./simple_db/history.csv', 'a') as file:
        file.write(user_name + ", " + str(card_id) + ", " + str(terminal_id) + ", " + datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S") + '\n')


def print_history():  # drukuje historię
    h = get_history()
    print("{0:20s} {1:15s} {2:15s} {3:15s}".format("nazwisko", "id_karty", "id_terminala", "data i czas"))
    for line in h:
        print("{0:20s} {1:15s} {2:15s} {3:15s}".format(line[0], line[1], line[2], line[3]))


def print_report(user_name):  # generuje raport o pracowniku
    h = get_user_history(user_name)

    print("{0:20s} {1:15s} {2:15s} {3:15s}".format("nazwisko", "id_karty", "id_terminala", "data i czas"))
    for i in range(len(h)):
        print("{0:20s} {1:15s} {2:15s} {3:15s}".format(h[i][0], h[i][1], h[i][2], h[i][3]))
        if i == len(h) - 1 and i % 2 == 0:
            print("Working time: " + str(datetime.now() - datetime.strptime(h[i - 1][3], " %d/%m/%Y %H:%M:%S")))
        elif i % 2 != 0:
            print("Working time: " + str(
                datetime.strptime(h[i][3], " %d/%m/%Y %H:%M:%S") - datetime.strptime(h[i - 1][3],
                                                                                     " %d/%m/%Y %H:%M:%S")))


def generate_report(user_name):
    with open("report " + user_name + ".csv", "w", newline='\n') as file:
        h = get_user_history(user_name)
        wrt = csv.writer(file, delimiter=",")
        for i in range(len(h)):
            wrt.writerow(h[i])
            if i == len(h) - 1 and i % 2 == 0:
                file.write("Working time: " +
                           str(datetime.now() - datetime.strptime(h[i - 1][3], " %d/%m/%Y %H:%M:%S")) + "\n")

            elif i % 2 != 0:
                file.write("Working time: " + str(datetime.strptime(h[i][3],
                                                                    " %d/%m/%Y %H:%M:%S") - datetime.strptime(
                    h[i - 1][3],
                    " %d/%m/%Y %H:%M:%S")) + "\n")
    return True


def get_user_history(user_name):  # pobiera dane z pliku z historią zdarzeń i zwraca listę z historią uzytkownika
    hist = []
    with open("./simple_db/history.csv", "r") as file:
        freader = csv.reader(file, delimiter=',')
        for line in freader:
            if line[0] == user_name:
                hist.append(line)
    return hist


def get_history():  # dodaje do listy dane z pliku z historią zdarzeń i zwraca tą listę
    hist = []
    with open("./simple_db/history.csv", "r") as file:
        freader = csv.reader(file, delimiter=',')
        for line in freader:
            hist.append(line)
    return hist


if __name__ == '__main__':
    open_terminals_db()
    print(terminals)