📇 Adressenverwaltung 2026

Ein modernes Python-Tool mit Amiga-Heritage

Dieses Programm ist eine moderne Portierung einer klassischen Adressenverwaltung. Es verbindet die Effizienz von Python 3 und Tkinter mit der Datenintegrität historischer .adr-Datenbestände.
🌟 Highlights

    Retro-Kompatibilität: Liest und schreibt das klassische Amiga-Adressformat (.adr) mit Latin-1 Kodierung.

    Plattformunabhängig: Läuft unter Linux (inkl. WSL), Windows und macOS.

    Rechtesicher: Nutzt pathlib, um Exporte im Benutzer-Home-Verzeichnis zu speichern – ideal für Installationen in geschützten Verzeichnissen wie /opt/.

    Dynamische Tabellen: Exportiert gefilterte Adresslisten als sauber formatierte Text-Tabellen mit automatischer Spaltenbreiten-Berechnung.

🛠 Features

    Suchen & Sortieren: Schnelle Volltextsuche und Sortierung nach beliebigen Feldern (Name, PLZ, Ort, etc.).

    Übernahme-Logik: Erkennt ungespeicherte Änderungen und bietet eine Sicherheitsabfrage beim Beenden.

    GUI-Komfort: Inklusive Tastenkürzel (Shortcuts) für Laden (Strg+L), Speichern (Strg+S) und Suchen (Strg+F).

    Zentrierte Darstellung: Das Hauptfenster startet immer perfekt zentriert auf dem Bildschirm.

📂 Installation & Nutzung
Voraussetzungen

    Python 3.x

    Tkinter (Standardmäßig in Python enthalten; unter Linux: sudo apt install python3-tk)

Start

    Lade das Repository herunter oder klone es:
    Bash

    git clone https://github.com/DEIN_USERNAME/adressenverwaltung.git

    Starte die Anwendung:
    Bash

    python3 adressen.py

📋 Technische Details

Das Programm erwartet eine spezifische Ordnerstruktur für das Icon-Handling:
Plaintext

/Adressenverwaltung
├── adressen.py      # Hauptprogramm
├── functions.py     # Hilfsfunktionen (Fenster-Zentrierung)
├── adressen.png     # Anwendungs-Icon
└── daten.adr        # Deine Adressdaten

🔗 Projekt-Kontext

Dieses Tool ist Teil der Software-Sammlung auf michael2211967.de. Es dient als Brückentechnologie, um wertvolle Datenbestände aus der Amiga-BASIC-Zeit (ca. 1999) in modernen Betriebsumgebungen (2026) produktiv weiterzuführen.

Lizenz: Frei zur privaten Nutzung.