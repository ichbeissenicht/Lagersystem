import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime, timedelta
import os

DATEI_PFAD = 'produkte.json'

def lade_produkte():
    if os.path.exists(DATEI_PFAD):
        with open(DATEI_PFAD, 'r') as f:
            return json.load(f)
    return []

def speichere_produkte(produkte):
    with open(DATEI_PFAD, 'w') as f:
        json.dump(produkte, f, indent=2)

def finde_abgelaufene(produkte):
    heute = datetime.today().date()
    return [p for p in produkte if datetime.strptime(p['ablaufdatum'], '%Y-%m-%d').date() == heute]

def aktualisiere_gui():
    for widget in frame.winfo_children():
        widget.destroy()

    abgelaufene = finde_abgelaufene(produkte)

    if not abgelaufene:
        tk.Label(frame, text="Keine Produkte sind heute abgelaufen.").pack()
        return

    for produkt in abgelaufene:
        name = produkt['name']
        label = tk.Label(frame, text=f"{name} - abgelaufen am {produkt['ablaufdatum']}")
        label.pack()

        btn_half = tk.Button(frame, text="+0.5 Jahr", command=lambda p=produkt: verlaengere(p, 0.5))
        btn_half.pack()

        btn_one = tk.Button(frame, text="+1 Jahr", command=lambda p=produkt: verlaengere(p, 1))
        btn_one.pack()

        btn_two = tk.Button(frame, text="+2 Jahre", command=lambda p=produkt: verlaengere(p, 2))
        btn_two.pack()

        btn_delete = tk.Button(frame, text="Löschen", fg="red", command=lambda p=produkt: loesche(p))
        btn_delete.pack()

def verlaengere(produkt, jahre):
    tage = int(jahre * 365.25)
    neues_datum = datetime.strptime(produkt['ablaufdatum'], '%Y-%m-%d') + timedelta(days=tage)
    produkt['ablaufdatum'] = neues_datum.strftime('%Y-%m-%d')
    speichere_produkte(produkte)
    aktualisiere_gui()

def loesche(produkt):
    produkte.remove(produkt)
    speichere_produkte(produkte)
    aktualisiere_gui()

# GUI Setup
produkte = lade_produkte()
root = tk.Tk()
root.title("Abgelaufene Produkte")
frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

aktualisiere_gui()
root.mainloop()
