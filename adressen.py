#!/usr/bin/python3
import sys

# Definition der Feldnamen aus Ihrem Amiga-Original
fields = [
    "Anrede", 
    "Vorname", 
    "Name", 
    "Straße", 
    "PLZ_Ort", 
    "Telefon", 
    "Bemerkung"
]

def load_file(path):
    adresses = []
    try:
        # 'latin-1' stellt sicher, dass Amiga-Umlaute korrekt interpretiert werden
        with open(path, 'r', encoding='latin-1') as file:
            first_line = file.readline()

            if first_line:
                count = int(first_line.strip())

                for _ in range(count):
                    entry = {}
                    for field in fields:
                        # Zeile lesen, Zeilenumbruch entfernen und Anführungszeichen säubern
                        content = file.readline().strip().replace('"', '')
                        entry[field] = content

                    # Das fertige Dictionary in die Liste einfügen
                    adresses.append(entry)

        print(f"Erfolg: {len(adresses)} Datensätze wurden in das Dictionary geladen.")
        return adresses

    except FileNotFoundError:
        print(f"Die Datei '{path}' wurde im aktuellen Verzeichnis nicht gefunden.")
    except ValueError:
        print("Die erste Zeile der Datei enthält keine gültige Anzahl.")

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    print("Das Tool wird mit")
    print(f"{sys.argv[0]} Datei")
    print("gestartet")
    path = input("Bitte Datei eingeben: ").strip()

if path and not path.lower().endswith('.adr'):
    path += '.adr'
adresses = load_file(path)

if not adresses:
    print("Keine Daten zum Anzeigen vorhanden.")
    sys.exit() # Beendet das Skript sauber

col_widths = {}
for field in fields:
    # Länge des Feldnamens als Startwert
    max_len = len(field)
    # Alle Treffer durchgehen und die maximale Länge im aktuellen Feld finden
    for adress in adresses:
        val_len = len(str(adress.get(field, "")))
        if val_len > max_len:
            max_len = val_len
    # Speichern mit 3 Leerzeichen Puffer
    col_widths[field] = max_len + 3

# 1. Spaltenbreite für die Nummer festlegen
nr_width = 6

# 2. Header ausgeben (Nr. wird linksbündig eingereiht)
header_str = "Nr.".ljust(nr_width) + "".join([field.ljust(col_widths[field]) for field in fields])
print(f"\033[1m{header_str}\033[0m")
print("-" * len(header_str))

# 3. Daten mit enumerate ausgeben
for i, adress in enumerate(adresses, start=1):
    # Der Index bekommt die gleiche feste Breite wie im Header
    nr_str = f"{i}".ljust(nr_width)
    line = "".join([str(adress.get(field, "")).ljust(col_widths[field]) for field in fields])
    print(nr_str + line)