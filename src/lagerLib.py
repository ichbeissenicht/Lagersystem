from json import dumps, loads
from string import ascii_letters, digits
from random import choice
from win32com.client import Dispatch
import time
import pathlib

productStorageConfigPath = ""
productLibraryConfigPath = ""
userDataPath = ""
storageData = {}
libraryData = {}
userData = {}


def printConfig():
    print(storageData)

def newID32():
    return "".join([str(choice(ascii_letters+digits)) for _ in range(32)])



def newProduct(uuid:str, name:str, charge:int, typ:int, verpackung:str)->dict:
    return {
        "uuid":uuid,
        "name": name,
        "charge": charge,
        "typ": typ,
        "verpackung": verpackung
    }

def newWafer(uuid:str, typ:str, charge:str, stueckzahl:str, verpackung:str, protokoll:list, wafer:list, sperrVermerk:str, sperrVermerkNummer:str, vermerk:str, durchmesser:str, abspaltung:str, ablaufdatum:str)->dict:
    return {
        "uuid":uuid,
        "typ": typ,
        "charge": charge,
        "stueckzahl": stueckzahl,
        "verpackung":verpackung,
        "protokoll": protokoll,
        "wafer": wafer,
        "durchmesser": durchmesser,
        "sperr_vermerk": sperrVermerk,
        "sperr_vermerk_nummer":sperrVermerkNummer,
        "vermerk": vermerk,
        "abspaltung": abspaltung,
        "ablaufdatum": ablaufdatum



    }
def protocoll(timeStamp, lagerzustand):
    protocollDict = []
    protocollDict.append(timeStamp)


def addEntry(id_:str, contentData:dict): # format "<int>:<str>"

    if id_ in storageData.keys():
        storageData[id_].append(contentData["uuid"])

    else:
        storageData[id_] = [contentData["uuid"]]
    libraryData[contentData["uuid"]] = contentData

def reEntry(lagerplatz:str, uuid:str):

    if lagerplatz in storageData.keys():
        storageData[lagerplatz].append(uuid)
    else:
        storageData[lagerplatz] = [uuid]



def delEntry(uuid:str):
    for key, value_list in storageData.items():
        if uuid in value_list:
            value_list.remove(uuid)
def delLibraryEntry(uuid:str):
    del libraryData[uuid]
    writeConfigLibary()

def abspaltungenZurueckgeben():                 #gibt von jeder Uuid in storage die Abspaltung zurück wenn vorhanden
    alleAbspaltungen= []

    for i in storageData.values():

        if i != [] and readUuid(i[0])["abspaltung"] != "":

            alleAbspaltungen.append(readUuid(i[0])["abspaltung"])
    return alleAbspaltungen


def abspaltungenZurueckgebenMitUuid():      #gibt von jeder Uuid in storage die Abspaltung mit uuid zurück wenn vorhanden
    alleAbspaltungenMitUuid = {}
    for i in storageData.values():
        if i != [] and readUuid(i[0])["abspaltung"] != "":
            alleAbspaltungenMitUuid.update({i[0]: readUuid(i[0])["abspaltung"]})


    return alleAbspaltungenMitUuid




def writeConfigStorage():
    file = open(productStorageConfigPath, "w")
    file.write(dumps(storageData, indent=4))
    file.close()
def writeConfigLibary():
    file = open(productLibraryConfigPath, "w")
    file.write(dumps(libraryData, indent=4))
    file.close()

def readConfigStorage()->dict:
    global storageData
    file = open(productStorageConfigPath, "r")
    content = file.read()
    file.close()
    storageData = loads(content)
    return storageData

def readConfigLibrary()->dict:
    global libraryData
    file = open(productLibraryConfigPath, "r")
    content = file.read()
    file.close()
    libraryData = loads(content)
    return libraryData

def readAblagePlatz(regalplatz:str):
    return storageData[regalplatz]

def readUuid(uuid:str):
    #print(uuid,type(uuid))
    return libraryData[uuid]

def readLagerplatz(lagerplatz:str):
    return storageData[lagerplatz]



def waitForScan():
    pass

def newWaferFromData(uuid:str):
    return libraryData[uuid]


def getTime():
    return time.strftime("%d.%m.%Y %H:%M:%S")

def getDate():
    return time.strftime("%Y-%m-%d")
def getTimeInTwoYears():
    def datum_in_zwei_jahren():
        heute = time.localtime()
        neues_jahr = heute.tm_year + 2
        monat = heute.tm_mon
        tag = heute.tm_mday

        # Versuche das Datum zu bauen, fallback auf 28. Februar wenn nötig
        try:
            neues_datum = time.strptime(f"{neues_jahr}-{monat:02d}-{tag:02d}", "%Y-%m-%d")
        except ValueError:
            # Wenn z. B. 29. Februar in einem Nicht-Schaltjahr, nimm 28. Februar
            neues_datum = time.strptime(f"{neues_jahr}-02-28", "%Y-%m-%d")

        return time.strftime("%Y-%m-%d", neues_datum)

    return datum_in_zwei_jahren()



def getAblagePlatz(uuid:str):
    for slotID in storageData.keys():
        content = storageData[slotID]
        if uuid in content:
            return slotID
    return "Kein Ablageplatz gefunden"



def ersetzeWortDurchUuid(uuid:str):
    try:
        # Datei öffnen und den Inhalt lesen
        dateipfad = "Label.dymo"
        with open(dateipfad, 'r') as datei:
            text = datei.read()
        # Das gesuchte Wort durch das neue Wort ersetzen
        platzhalter = "platzhalter"
        neuer_text = text.replace(platzhalter, uuid)

        # Die Datei im Schreibmodus öffnen und den neuen Text schreiben
        with open(dateipfad, 'w') as datei:
            datei.write(neuer_text)

        print(f'Das Wort "{platzhalter}" wurde erfolgreich durch "{uuid}" ersetzt.')
    except FileNotFoundError:
       print(f'Die Datei {dateipfad} wurde nicht gefunden.')


    """
        with open("lagerLib", "r") as file:
        daten = productLibraryConfigPath.load(file)
        print(daten)
    """
def changeAmount(stueckzahl:str,newuuid:str):
    wafer=readUuid(newuuid)
    wafer["stueckzahl"] = stueckzahl
def changePackage(verpackung:str,newuuid:str):
    wafer=readUuid(newuuid)
    wafer["verpackung"] = verpackung
def anzahlWafer(anzahl_eintraege):
    my_dict = {}

    for i in range(anzahl_eintraege):

        if i == 0:
            key = input(f"Name erster Wafer: ")
        elif i >= 1:
            key = input(f"Name nächster Wafer: ")
        value = input(f"Stueckzahl des Wafer {key}: ")
        my_dict[key] = value

    return my_dict

def readUserLogin()->dict:
    global userData
    file = open(userDataPath, "r")
    content = file.read()
    file.close()
    userData = loads(content)
    return userData

def changeValue(uuid:str, variable:str, value:str):
    wafer = readUuid(uuid)
    wafer[variable] = value

def print_uuid(uuid:str):
    barcode_val = uuid
    barcode_path = r"C:\Users\lenna\Desktop\Address.label"  # Wenn adress.label im selben ordner liegt wie die ausführende .py kann auch
    # mit ./adress.label ausgeführt werden
    my_printer = 'DYMO LabelWriter 450 DUO Label'

    printer_com = Dispatch("Dymo.DymoAddIn")
    printer_com.SelectPrinter(my_printer)
    printer_com.Open(barcode_path)

    printer_label = Dispatch("Dymo.DymoLabels")
    printer_label.SetField("Barcode", barcode_val)
    printer_label.SetField("TEXT_1", readUuid(uuid)["charge"])
    printer_label.SetField("TEXT_2", readUuid(uuid)["typ"])

    printer_com.StartPrintJob()
    printer_com.Print(1, False)
    printer_com.EndPrintJob()

def testPrint(rnztx):
    print(rnztx)