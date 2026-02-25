#!/usr/bin/python3
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
from pathlib import Path
import functions
script_dir = os.path.dirname(os.path.abspath(__file__))

class AdressenGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Adressenverwaltung")
        self.geometry = functions.center_window(1100, 500, self.root)
        self.root.geometry(self.geometry)
        self.icon_path = os.path.join(script_dir, 'adressen.png')
        self.img = tk.PhotoImage(file=self.icon_path)
        self.root.iconphoto(False, self.img)
        self.fields = ["Anrede", "Vorname", "Name", "Straße", "PLZ_Ort", "Telefon", "Bemerkung"]
        self.adressen = []
        self.widgets = {}
        self.current_index = 0
        self.__addMenu()
        self.__addFileMenu()
        self.__addEditMenu()
        self.__addFields()
        self.__addButtons()
        self.root.wm_protocol("WM_DELETE_WINDOW", self.quit)
        self.current_path = ""
        self.update_title()
        self.root.mainloop()

    def __addMenu(self):
        self.menu = tk.Menu(self.root)
        self.root.configure(menu=self.menu)

    def __addFileMenu(self):
        self.filemenu = tk.Menu(master=self.menu)
        self.menu.add_cascade(label="Datei", font=("Arial",15), menu=self.filemenu)
        self.filemenu.add_command(label="Neu", font=("Arial", 15), command=self.new_adresse_dialog, accelerator="Strg+N")
        self.filemenu.add_command(label="Datei laden", font=("Arial", 15), command=self.load_adresses, accelerator="Strg+L")
        self.filemenu.add_command(label="Speichern", font=("Arial", 15),command=self.save_adresses, accelerator="Strg+S")
        self.filemenu.add_command(label="Speichern unter...", font=("Arial", 15), command=self.save_as_adresses)
        self.filemenu.add_command(label="Ausgabe (über Filter)", font=("Arial", 15), command=self.export_filtered_adresses)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Beenden", font=("Arial", 15), command=self.quit, accelerator="Strg+B")

        self.root.bind("<Control-n>", self.new_adresse_dialog)
        self.root.bind("<Control-l>", self.load_adresses)
        self.root.bind("<Control-s>", self.save_adresses)
        self.root.bind("<Control-b>", self.quit)

    def __addEditMenu(self):
        self.editmenu = tk.Menu(master=self.menu)
        self.menu.add_cascade(label="Bearbeiten", font=("Arial",15), menu=self.editmenu)
        self.editmenu.add_command(label="Löschen", font=("Arial",15), command=self.delete_adresse, accelerator="Strg+Entf")
        self.editmenu.add_command(label="Suchen", font=("Arial",15), command=self.search_adresse, accelerator="Strg+F")
        self.editmenu.add_command(label="Sortieren", font=("Arial",15), command=self.ask_sort_criterion)

        self.root.bind("<Control-Delete>", self.delete_adresse)
        self.root.bind("<Control-f>", self.search_adresse)

    def __addFields(self):
        # Wir erstellen für jedes Feld ein Label und ein Entry
        for i, field in enumerate(self.fields):
            # Label (links)
            lbl = tk.Label(self.root, text=f"{field}:", font=("Arial",15), width=12, anchor="w")
            lbl.grid(row=i, column=0, padx=10, pady=2)
            
            # Entry (rechts)
            ent = tk.Entry(self.root, font=("Arial", 15), width=80)
            ent.grid(row=i, column=1, padx=10, pady=2)
            
            # Wir speichern das Entry-Widget im Dictionary 'widgets', 
            # damit wir später über den Namen darauf zugreifen können
            self.widgets[field] = ent

    def __addButtons(self):
        button_frame = tk.Frame(self.root)
        # Wir platzieren den Frame in der Zeile nach dem letzten Feld (Index 7)
        button_frame.grid(row=len(self.fields), column=0, columnspan=2, pady=15)
        # 1. Button: Zurück (links)
        tk.Button(button_frame, text="<< Zurück", font=("Arial", 15), command=self.prev_adresse).pack(side="left", padx=5)
        # 2. ÜBERNEHMEN (Neu hinzugefügt)
        # Er ruft save_to_list auf und könnte optional eine Info ausgeben
        tk.Button(button_frame, text="Übernehmen", font=("Arial", 15), command=self.save_to_list, bg="#e1e1e1").pack(side="left", padx=5)
        # 2. Label: Status (Mitte) - Jetzt zwischen den Buttons
        self.lbl_status = tk.Label(button_frame, text="", font=("Arial", 15), width=10)
        self.lbl_status.pack(side="left", padx=10)

        # 3. Button: Vor (rechts)
        tk.Button(button_frame, text="Vor >>", font=("Arial", 15), command=self.next_adresse).pack(side="left", padx=5)
        self.root.bind("<Up>", self.next_adresse)
        self.root.bind("<Down>", self.prev_adresse)
        
    def load_adresses(self, event=None):
        # Dialog öffnen
        path = filedialog.askopenfilename(filetypes=[("Adressen", "*.adr")])
    
        if not path: 
            return

        self.adressen = []
        self.current_index = 0

        # Einlesen ohne Sicherheitsnetz
        with open(path, 'r', encoding='latin-1') as file:
            count = int(file.readline().strip())
        
            for _ in range(count):
                entry = {}
                for field in self.fields:
                    entry[field] = file.readline().strip().replace('"', '')
                self.adressen.append(entry)
            self.current_path = path
            self.update_title()
            
        # Zeige direkt den ersten Datensatz an, wenn vorhanden
        if self.adressen:
            self.show_adresse(0)
            messagebox.showinfo("Laden", f"{len(self.adressen)} Adressen geladen!")

    def save_adresses(self, event=None):
        """Speichert die Daten im Amiga-kompatiblen Format."""
        # Sicherheits-Check: Haben wir überhaupt einen Pfad?
        if not hasattr(self, 'current_path') or not self.current_path:
            self.save_as_adresses()
            if not self.current_path:
                return

        with open(self.current_path, 'w', encoding='latin-1') as file:
            # 1. Anzahl der Datensätze ermitteln
            count = len(self.adressen)
            
            # 2. Die Anzahl in die erste Zeile schreiben
            file.write(f"{count}\n")
            
            # 3. Jetzt müssen wir durch die Liste gehen...
            for entry in self.adressen:
                for field in self.fields:
                    value = entry.get(field, "")
                    # Amiga-Logik: Ein Leerzeichen schreiben, wenn das Feld leer ist
                    if value == "":
                        file.write(" \n")
                    else:
                        file.write(f"{value}\n")
            self.data_has_changed = False

    def save_as_adresses(self):
        path = filedialog.asksaveasfilename(filetypes=[("Adressen", "*.adr")], defaultextension=".adr")
        if path != "":
            self.current_path = path
            self.update_title()
            self.save_adresses()

    def show_adresse(self, index):
        if not self.adressen:
            self.lbl_status.config(text="")
            return
        # Diese Methode füllt die Maske mit den Daten eines Datensatzes
        daten = self.adressen[index]
        for field in self.fields:
            self.widgets[field].delete(0, tk.END)      # Altes löschen
            self.widgets[field].insert(0, daten[field]) # Neues schreiben
        # Punkt 1 gelöst: Das Label hier explizit aktualisieren
        # Wir addieren 1 zum Index, damit der User "1 / 15" sieht statt "0 / 15"
        anzahl = len(self.adressen)
        self.lbl_status.config(text=f"{self.current_index + 1} / {anzahl}")

    def next_adresse(self, event=None):
        if self.adressen and self.current_index < len(self.adressen) - 1:
            self.save_to_list() # Änderungen am aktuellen Datensatz prüfen/sichern
            self.current_index += 1
            self.show_adresse(self.current_index)

    def prev_adresse(self, event=None):
        if self.adressen and self.current_index > 0:
            self.save_to_list() # Änderungen am aktuellen Datensatz prüfen/sichern
            self.current_index -= 1
            self.show_adresse(self.current_index)

    def save_to_list(self):
        if not self.adressen:
            return

        # Wir greifen uns den Datensatz
        record = self.adressen[self.current_index]
        
        # Wir sammeln die aktuellen Werte aus der GUI in einem neuen Dictionary
        gui_values = {field: self.widgets[field].get().strip() for field in self.fields}
        
        # Jetzt kommt deine IF-Abfrage: Hat sich gegenüber dem Speicher etwas geändert?
        # Wir vergleichen Feld für Feld
        has_changed = False
        for field in self.fields:
            if gui_values[field] != record.get(field, "").strip():
                has_changed = True
                break # Eine Änderung reicht uns schon
        
        if has_changed:
            # Nur wenn sich wirklich was getan hat, aktualisieren wir das Dictionary
            for field in self.fields:
                record[field] = gui_values[field]
            
            self.data_has_changed = True

    def quit(self, event=None):
        # Wir prüfen nur, ob ungespeicherte Änderungen vorliegen
        if hasattr(self, 'data_has_changed') and self.data_has_changed:
            # Nur dann kommt die Sicherheitsabfrage
            message = "Es gibt ungespeicherte Änderungen! Wirklich beenden?"
            if not messagebox.askyesno('Beenden', message):
                return # User hat "Nein" gewählt, also nicht beenden

        # Wenn keine Änderungen da sind ODER der User "Ja" geklickt hat:
        self.root.quit()
        self.root.destroy()

    def new_adresse_dialog(self, event=None):
        # 1. Neues Fenster erstellen
        self.new_win = tk.Toplevel(self.root)
        self.new_win.title("Neue Adresse hinzufügen")
        geometry = functions.center_window(1075, 350, self.new_win)
        self.new_win.geometry(geometry)
        
        # Dictionary für die neuen Widgets in DIESEM Fenster
        new_widgets = {}

        # 2. Felder aufbauen (wie im Hauptfenster)
        for i, field in enumerate(self.fields):
            tk.Label(self.new_win, text=f"{field}:", width=12, font=("Arial",15), anchor="w").grid(row=i, column=0, padx=10, pady=5)
            ent = tk.Entry(self.new_win, font=("Arial", 15), width=80)
            ent.grid(row=i, column=1, padx=10, pady=5)
            new_widgets[field] = ent

        # 3. Button-Frame für OK und Abbrechen
        btn_frame = tk.Frame(self.new_win)
        btn_frame.grid(row=len(self.fields), column=0, columnspan=2, pady=20)

        # OK-Button: Daten übernehmen
        tk.Button(btn_frame, text="OK", width=10, font=("Arial",15),
                  command=lambda: self.add_new_entry(new_widgets)).pack(side="left", padx=10)
        
        # Abbrechen-Button: Fenster schließen
        tk.Button(btn_frame, text="Abbrechen", width=10, font=("Arial", 15), 
                  command=self.new_win.destroy).pack(side="left", padx=10)

    def add_new_entry(self, widgets):
        # Daten aus dem neuen Fenster einsammeln
        new_entry = {field: widgets[field].get().strip() for field in self.fields}
        
        # Nur hinzufügen, wenn nicht alles leer ist
        if any(new_entry.values()):
            self.adressen.append(new_entry)
            self.data_has_changed = True
            self.new_win.destroy()
            
            # Zum neuen (letzten) Eintrag springen und anzeigen
            self.current_index = len(self.adressen) - 1
            self.show_adresse(self.current_index)
        else:
            self.new_win.destroy()

    def delete_adresse(self, event=None):
        if not self.adressen:
            return

        # Sicherheitsabfrage
        msg = "Diesen Datensatz wirklich unwiderruflich löschen?"
        if messagebox.askyesno("Löschen", msg):
            # 1. Datensatz aus der Liste entfernen
            self.adressen.pop(self.current_index)
            self.data_has_changed = True

            # 2. Index korrigieren
            # Falls wir den letzten gelöscht haben, müssen wir eins zurück
            if self.current_index >= len(self.adressen) and self.current_index > 0:
                self.current_index -= 1
            
            # 3. Anzeige aktualisieren
            if not self.adressen:
                # Liste ist jetzt leer -> leere Felder zeigen
                for field in self.fields:
                    self.widgets[field].delete(0, tk.END)
                self.lbl_status.config(text="0 / 0")
            else:
                self.show_adresse(self.current_index)

    def search_adresse(self, event=None):
        if not self.adressen:
            return

        # 1. Den User nach dem Namen fragen
        search_term = simpledialog.askstring("Suche", "Nach welchem Namen suchen Sie?")
        
        if search_term:
            search_term = search_term.lower()
            
            # 2. Die Liste durchlaufen
            for i, entry in enumerate(self.adressen):
                # Wir suchen im Feld 'Name' (oder Vorname, falls gewünscht)
                if search_term in entry.get("Name", "").lower() or \
                   search_term in entry.get("Vorname", "").lower():
                    
                    # 3. Treffer gefunden!
                    self.current_index = i
                    self.show_adresse(self.current_index)
                    return # Suche beenden nach dem ersten Treffer

            # 4. Nichts gefunden
            messagebox.showinfo("Suche", f"Kein Eintrag für '{search_term}' gefunden.")

    def ask_sort_criterion(self):
        if not self.adressen:
            self.no_data_available("Sortieren")
            return

        # 1. Ein kleines modales Fenster erstellen
        sort_win = tk.Toplevel(self.root)
        sort_win.title("Sortieren nach...")
        sort_win.geometry(functions.center_window(300, 380, sort_win))
        sort_win.grab_set() # Fokus erzwingen

        tk.Label(sort_win, text="Feld auswählen:", font=("Arial", 15), pady=10).pack()

        # 2. Für jedes Feld einen Button erstellen
        for field in self.fields:
            tk.Button(sort_win, text=field, width=20, font=("Arial", 15),
                      command=lambda f=field: self.execute_sort(f, sort_win)).pack(pady=2)

    def execute_sort(self, field, window):
        # Aktuellen Stand sichern
        self.save_to_list()
        
        # Sortieren (nach dem gewählten Feld 'field')
        self.adressen.sort(key=lambda x: x.get(field, "").lower())
        
        self.current_index = 0
        self.show_adresse(0)
        self.data_has_changed = True
        
        window.destroy() # Auswahlfenster schließen
        messagebox.showinfo("Sortieren", f"Sortiert nach: {field}")

    def export_filtered_adresses(self):
        if not self.adressen:
            self.no_data_available("Ausgabe (über Filter)")
            return

        # 1. Das Toplevel-Fenster erstellen
        filter_win = tk.Toplevel(self.root)
        filter_win.title("Export-Filter (Suchbegriffe)")
        
        # Geometrie setzen mit deiner Zentrierungs-Funktion
        geo = functions.center_window(400, 450, filter_win)
        filter_win.geometry(geo)
        
        filter_win.transient(self.root)
        filter_win.grab_set()
        filter_win.focus_set()

        filter_entries = {}

        # Labels und Felder für die 7 Suchbegriffe erstellen
        for i, field in enumerate(self.fields):
            tk.Label(filter_win, text=f"{field}:", font=("Arial", 15)).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = tk.Entry(filter_win, font=("Arial", 15))
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            filter_entries[field] = entry

        # 2. Die interne Logik-Funktion zum Filtern und Speichern
        def start_export():
            # Filterkriterien einsammeln
            maske = {f: e.get().lower().strip() for f, e in filter_entries.items() if e.get().strip()}
            
            # Die Amiga "Pruef=7" Logik: Alle ausgefüllten Felder müssen matchen
            results = []
            for adr in self.adressen:
                match = True
                for field, value in maske.items():
                    if not str(adr.get(field, "")).lower().startswith(value):
                        match = False
                        break
                if match:
                    results.append(adr)

            if not results:
                messagebox.showinfo("Suche", "Keine passenden Adressen gefunden.")
                return

            # 3. Spaltenbreiten dynamisch berechnen (dein bewährter Code)
            col_widths = {}
            for field in self.fields:
                max_len = len(field)
                for res in results:
                    val_len = len(str(res.get(field, "")))
                    if val_len > max_len:
                        max_len = val_len
                col_widths[field] = max_len + 3

            # 4. Datei-Speichern Dialog
            home = str(Path.home())
            save_path = filedialog.asksaveasfilename(
                initialdir=home,
                initialfile="Gefilterte_Adressen.txt",
                defaultextension=".txt",
                filetypes=[("Textdateien", "*.txt"), ("Alle Dateien", "*.*")],
                title="Export-Tabelle speichern"
            )

            if not save_path:
                return

            # Datei schreiben (im Amiga-freundlichen latin-1)
            try:
                with open(save_path, "w", encoding="utf8") as f:
                    # Kopfzeile
                    header = "".join([field.ljust(col_widths[field]) for field in self.fields])
                    f.write(header + "\n")
                    f.write("-" * len(header) + "\n")

                    # Datenzeilen
                    for entry in results:
                        line = "".join([str(entry.get(field, "")).ljust(col_widths[field]) for field in self.fields])
                        f.write(line + "\n")
                
                messagebox.showinfo("Erfolg", f"Export mit {len(results)} Treffern erstellt.")
                filter_win.destroy() # Fenster erst bei Erfolg schließen
            except Exception as e:
                messagebox.showerror("Fehler", f"Datei konnte nicht gespeichert werden: {e}")
        # 3. DER BUTTON (muss hier stehen, eingerückt unter filter_entries!)
        # Jetzt kennt er filter_win, da wir uns noch in der Methode befinden.
        tk.Button(filter_win, text="Export-Datei erstellen", font=("Arial", 15), command=start_export, 
                  bg="#e0e0e0").grid(row=len(self.fields), columnspan=2, pady=20)

    def update_title(self):
        if hasattr(self, 'current_path') and self.current_path:
            self.root.title("Adressenverwaltung: " + self.current_path)
        else:
            self.root.title("Adressenverwaltung")

    def no_data_available(self, reason):
        messagebox.showwarning("Warnung", f"Für {reason} bitte erst Daten Laden!")
        return

adressen = AdressenGUI()
