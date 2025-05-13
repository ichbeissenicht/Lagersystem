import tksimple as tk
import lagerLib as lib
import re
from afktimer import afk_reset, afk_clear, afk_logout, enter_login, state_Switch
from constants import sg, sgnew, Constants, LOAD_STYLE, contrastcolorsg
from widgets import CustomCheckbutton, Counterwidget, Ask_for_wafer_name_and_amount, CheckButtonGroup, \
    PickWaferToOutSource, PickAmountToOutSource, PickWaferToOutSource, AmountToOutSource
from excel import convertToExcel

lib.productStorageConfigPath = r"L:\AENE\ne-pm\01_EPC\60_labor\60_Lagerhaltung\Musterlager\storage.json"
lib.productLibraryConfigPath = r"L:\AENE\ne-pm\01_EPC\60_labor\60_Lagerhaltung\Musterlager\library.json"
lib.readConfigStorage()
lib.readConfigLibrary()



# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
class Mainpage(tk.MenuPage):
    def __init__(self, master):
        super().__init__(master, sg)
        self.admin = False




        self.button_suchen = tk.Button(self, group=sg)
        self.button_suchen.setText("Suchen")
        self.button_suchen.setFont(30)
        self.button_suchen.placeRelative(centerX=True, centerY=True, changeY=-450 * Constants.resolution,
                                         fixWidth=400 * Constants.resolution, fixHeight=200 * Constants.resolution,
                                         changeX=450 * Constants.resolution)
        self.button_suchen.attachToolTip("Mit diesem Button können Sie nach Ware suchen", group=sg)
        self.button_suchen.setCommand(self.open_search)

        self.button_einlagern = tk.Button(self, group=sg)
        self.button_einlagern.setText("Einlagern")
        self.button_einlagern.setFont(30)
        self.button_einlagern.placeRelative(centerX=True, centerY=True, changeY=-450 * Constants.resolution,
                                            changeX=-450 * Constants.resolution, fixWidth=400 * Constants.resolution,
                                            fixHeight=200 * Constants.resolution)
        self.button_einlagern.attachToolTip("Mit diesem Button können Sie Ware Einlagern", group=sg)
        self.button_einlagern.setCommand(self.open_einlagern)

        self.abgelaufeneWareFrame = tk.LabelFrame(self, group=sg)
        self.abgelaufeneWareFrame.placeRelative(centerY=True, centerX=True, fixWidth=1200 * Constants.resolution,
                                           fixHeight=300 * Constants.resolution)







        self.textAbgelaufeneWare = tk.Text(self.abgelaufeneWareFrame, group=sg)
        self.textAbgelaufeneWare.setStyle(tk.Style.FLAT)
        self.textAbgelaufeneWare.setText("Aktuell keine ausgelaufene Ware ")
        self.textAbgelaufeneWare.setFont(30)
        self.textAbgelaufeneWare.placeRelative(centerX=True, centerY=True, fixHeight=60, fixWidth=600)

        self.colorswitch_button = tk.Button(self, sg)
        self.colorswitch_button.placeRelative(stickDown=True, fixWidth=200, fixHeight=75, changeX=25, changeY=-25)
        self.colorswitch_button.setFont(20)
        self.colorswitch_button.setCommand(self.farbeWechseln)

        self.getExcel = tk.Button(self,sg)
        self.getExcel.setFont(20)
        self.getExcel.setText("Excel herunterladen")
        self.getExcel.placeRelative(stickDown=True,centerX=True,fixWidth=300,fixHeight=50, changeY=-25)
        self.getExcel.setCommand(convertToExcel)
        self.getExcel.setCommand(self.excelSaveConfirm)




        self.label_admin = tk.Label(self, text="°", group=sgnew)
        self.label_admin.placeRelative(fixWidth=100, fixHeight=120, stickDown=True, stickRight=True,
                                       changeY=+45)  # TODO:Anpassbar
        self.label_admin.setFont(100)
        self.label_admin.bind(enter_login, tk.EventType.LEFT_CLICK)
        if Constants.whitemode is True:
            self.colorswitch_button.setText("Darkmode")
        else:
            self.colorswitch_button.setText("Whitemode")

        self.showAbgelaufeneWare()
    def excelSaveConfirm(self):
        self.excelSaveConfirm = tk.SimpleDialog.askInfo(self,
                                                       "Ihre Excel liegt nun im Download Ordner bereit!",
                                                       "Info")
    def showAbgelaufeneWare(self):
        self.abgelaufeneWareListe = self.checkDateForExpiringDate()
        if self.abgelaufeneWareListe == []:
            pass
        else:
            self.index = 0

            self.waferinfo = tk.Label(self.abgelaufeneWareFrame,sg)
            self.waferinfo.setText("Typ: " +lib.readUuid(self.abgelaufeneWareListe[self.index])["typ"]+ "\n" + "Charge: " +lib.readUuid(self.abgelaufeneWareListe[self.index])["charge"]+ "\n" +lib.readUuid(self.abgelaufeneWareListe[self.index])["protokoll"][0]+ "\n" + "Verpackung: " +lib.readUuid(self.abgelaufeneWareListe[self.index])["verpackung"])

            self.waferinfo.setFont(20)
            self.waferinfo.placeRelative(0,0,600,215)

            self.verlaengerungsdauer0 = tk.Button(self.abgelaufeneWareFrame,sg)
            self.verlaengerungsdauer0.setFont(20)
            self.verlaengerungsdauer0.setText("Zwei Jahre verlängern")
            self.verlaengerungsdauer0.setCommand(self.verlaengernundnaechsterwafer)
            self.verlaengerungsdauer0.placeRelative(0,0,300,110, stickRight=True, changeX=-3)

            self.verlaengerungsdauer2 = tk.Button(self.abgelaufeneWareFrame, sg)
            self.verlaengerungsdauer2.setFont(20)
            self.verlaengerungsdauer2.setText("Nicht verlängern")
            self.verlaengerungsdauer2.setCommand(self.nichtverlaengernundnaechsterwafer)
            self.verlaengerungsdauer2.placeRelative(0, 110, 300, 110, stickRight=True , changeX=-3)

    def verlaengernundnaechsterwafer(self):


        if self.index <= len(self.abgelaufeneWareListe)-1:

            self.waferinfo.setText(self.abgelaufeneWareListe[self.index])
            lib.readUuid(self.abgelaufeneWareListe[self.index])["ablaufdatum"] = lib.getTimeInTwoYears()
            self.index += 1
            lib.writeConfigLibary()
            lib.writeConfigStorage()

            self.waferinfo.placeForget()
            self.verlaengerungsdauer0.placeForget()
            self.verlaengerungsdauer2.placeForget()
            self.showAbgelaufeneWare()
        else:

            self.waferinfo.placeForget()
            self.verlaengerungsdauer0.placeForget()
            self.verlaengerungsdauer2.placeForget()

    def nichtverlaengernundnaechsterwafer(self):
        print("1")
        if self.index <= len(self.abgelaufeneWareListe)-1:
            print("2")
            self.waferinfo.setText(self.abgelaufeneWareListe[self.index])
            lib.readUuid(self.abgelaufeneWareListe[self.index])["ablaufdatum"] = lib.getTimeInTwoYears()
            lib.delEntry(self.abgelaufeneWareListe[self.index])
            lib.delLibraryEntry(self.abgelaufeneWareListe[self.index])

            self.index += 1
            lib.writeConfigLibary()
            lib.writeConfigStorage()
            self.waferinfo.placeForget()
            self.verlaengerungsdauer0.placeForget()
            self.verlaengerungsdauer2.placeForget()
            self.showAbgelaufeneWare()
        else:
            print("3")
            self.waferinfo.placeForget()
            self.verlaengerungsdauer0.placeForget()
            self.verlaengerungsdauer2.placeForget()









    def checkDateForExpiringDate(self):

        daten = lib.readConfigLibrary()
        gefundene_uuids = []
        for eintrag in daten.values():
            if eintrag.get("ablaufdatum") == str(lib.getDate()):
                gefundene_uuids.append(eintrag["uuid"])
        return gefundene_uuids



    def farbeWechseln(self):
        Constants.whitemode = not Constants.whitemode
        if Constants.whitemode is True:
            self.colorswitch_button.setText("Darkmode")
        else:
            self.colorswitch_button.setText("Whitemode")
        LOAD_STYLE()

    def onShow(self, **kwargs):
        self.placeRelative()

    def onHide(self):
        self.placeForget()

    def open_einlagern(self):
        self.openNextMenuPage(choice_page)

    def open_search(self):
        lib.readConfigLibrary()
        lib.readConfigStorage()
        self.openNextMenuPage(search_page)

    def open_auslagern(self):
        self.openNextMenuPage(auslagern_page)

button_neue_ware = None
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


class Einlagern_page(tk.MenuPage):
    def __init__(self, master):
        super().__init__(master, sg)

        self.button_neue_ware = tk.Button(self, group=sg)
        self.button_neue_ware.setText("Neue Ware")
        self.button_neue_ware.setFont(30)
        self.button_neue_ware.placeRelative(centerX=True, centerY=True, changeY=-500 * Constants.resolution,
                                            fixWidth=400 * Constants.resolution, fixHeight=200 * Constants.resolution)
        self.button_neue_ware.attachToolTip("Ware welche noch nie im Lager war, neu Einlagern", group=sg)
        self.button_neue_ware.setCommand(self.open_neue_ware_einlagern_page)

        self.button_alte_ware = tk.Button(self, group=sg)

        self.button_alte_ware.setText("Alte Ware")
        self.button_alte_ware.setFont(30)
        self.button_alte_ware.placeRelative(centerX=True, centerY=True, changeY=-500 * Constants.resolution,
                                            changeX=800 * Constants.resolution, fixWidth=400 * Constants.resolution,
                                            fixHeight=200 * Constants.resolution)
        self.button_alte_ware.attachToolTip("Ware welche bereits im Lager eingelagert war", group=sg)
        self.button_alte_ware.setCommand(self.open_alte_ware_einlagern_page)

        self.button_zurueck_einlagern = tk.Button(self, group=sg)
        self.button_zurueck_einlagern.setText("Zurück")
        self.button_zurueck_einlagern.setFont(30)
        self.button_zurueck_einlagern.placeRelative(centerX=True, centerY=True, changeY=-500 * Constants.resolution,
                                                    changeX=-800 * Constants.resolution,
                                                    fixWidth=400 * Constants.resolution,
                                                    fixHeight=200 * Constants.resolution)
        self.button_zurueck_einlagern.attachToolTip("Zurück", group=sg)
        self.button_zurueck_einlagern.setCommand(self.openLastMenuPage)

        self.label_admin = tk.Label(self, text="°", group=sgnew)
        self.label_admin.placeRelative(fixWidth=100, fixHeight=120, stickDown=True, stickRight=True,
                                       changeY=+45)  # TODO:Anpassbar
        self.label_admin.setFont(100)
        self.label_admin.bind(enter_login, tk.EventType.LEFT_CLICK)

    def onShow(self, **kwargs):
        self.placeRelative()

    def onHide(self):
        self.placeForget()

    def open_neue_ware_einlagern_page(self):
        self.openNextMenuPage(neue_ware_einlagern_page)

    def open_alte_ware_einlagern_page(self):
        self.openNextMenuPage(alte_ware_einlagern_page)


# ------------------------------------------------------------------------------------------------------------------------
class Neue_ware_einlagern_page(tk.MenuPage):
    def __init__(self, master):
        super().__init__(master, sg)
        self.master = master

        self.root = Ask_for_wafer_name_and_amount(self.master, sg)
        self.root.onSave(self.wafer_eintrag_hinzufuegen_speichern)

        self.button_zurueck_einlagern = tk.Button(self, group=sg)
        self.button_zurueck_einlagern.setText("Zurück")
        self.button_zurueck_einlagern.setFont(30)
        self.button_zurueck_einlagern.placeRelative(centerX=True, centerY=True, changeY=-500 * Constants.resolution,
                                                    changeX=-800 * Constants.resolution,
                                                    fixWidth=400 * Constants.resolution,
                                                    fixHeight=200 * Constants.resolution)
        self.button_zurueck_einlagern.attachToolTip("Zurück", group=sg)
        self.button_zurueck_einlagern.setCommand(self.openLastMenuPage)

        self.eingabeFelder = tk.Frame(self, group=sg)
        self.eingabeFelder.placeRelative(centerX=True, centerY=True, changeX=300 * Constants.resolution,
                                         changeY=-50 * Constants.resolution, fixWidth=1800 * Constants.resolution,
                                         fixHeight=1100 * Constants.resolution)

        self.label_typ = tk.Label(self.eingabeFelder, group=sg)
        self.label_typ.setText("Typ:")
        self.label_typ.setFont(30)
        self.label_typ.place(height=50, width=300)

        self.entry_typ = tk.Entry(self.eingabeFelder, group=sg)
        self.entry_typ.place(x=300, width=500, height=50)
        self.entry_typ.setFont(30)
        self.entry_typ.attachToolTip("Typ eingeben")

        self.label_charge = tk.Label(self.eingabeFelder, group=sg)
        self.label_charge.setText("Charge:")
        self.label_charge.setFont(30)
        self.label_charge.place(y=60, width=300, height=50)

        self.entry_charge = tk.Entry(self.eingabeFelder, group=sg)
        self.entry_charge.place(y=60, x=300, width=500, height=50)
        self.entry_charge.setFont(30)
        self.entry_charge.attachToolTip("Charge eingeben")

        self.label_verpackung = tk.Label(self.eingabeFelder, group=sg)
        self.label_verpackung.setText("Verpackung:")
        self.label_verpackung.setFont(30)
        self.label_verpackung.place(y=120, width=300, height=50)

        self.dropdown_frame = tk.LabelFrame(self.eingabeFelder, group=sg)
        self.dropdown_frame.place(x=300, y=120, width=500, height=50)

        self.dropdown_verpackung = tk.DropdownMenu(self.dropdown_frame, group=sg,
                                                   optionList=["Single-Frameshipper","Frameshipper", "Tape & Reel", "8 Zoll Box", " 6 Zoll Box", "Andere"])
        self.dropdown_verpackung.place(x=0, y=0, width=497, height=46)
        self.dropdown_verpackung.setFont(30)
        self.dropdown_verpackung.attachToolTip("Verpackung auswählen")

        self.entry_stueckzahl_label = tk.Label(self.eingabeFelder, group=sg)
        self.entry_stueckzahl_label.setFont(30)
        self.entry_stueckzahl_label.setText("Stueckzahl:")
        self.entry_stueckzahl_label.place(x=0, y=240, width=350, height=50)

        self.entry_stueckzahl = tk.Entry(self.eingabeFelder, group=sg)
        self.entry_stueckzahl.setFont(30)
        self.entry_stueckzahl.attachToolTip("Stueckzahl eingeben")
        self.entry_stueckzahl.place(x=300, y=240, width=500, height=50)

        self.frame = tk.Frame(self.eingabeFelder, group=sg)

        self.label_durchmesser = tk.Label(self.frame, group=sg)
        self.label_durchmesser.setText("Durchmesser:")
        self.label_durchmesser.setFont(30)
        self.label_durchmesser.place(-100, 0, 500, 50)

        self.dropdown_durchmesser_frame = tk.LabelFrame(self.frame, group=sg)
        self.dropdown_durchmesser_frame.place(x=300, y=0, width=500, height=50)

        self.dropdown_durchmesser = tk.DropdownMenu(self.dropdown_durchmesser_frame, group=sg,
                                                    optionList=["50mm", "100mm", "120mm"])
        self.dropdown_durchmesser.place(x=0, y=0, width=497, height=46)
        self.dropdown_durchmesser.setFont(30)
        self.dropdown_durchmesser.attachToolTip("Durchmesser des Wafers auswählen")

        def checkbox_wafer_abfrage():
            is_check_box_wafer_ticked = self.checkbox_wafer.getValue()
            if is_check_box_wafer_ticked:
                self.frame.placeRelative(fixY=240)
                master.updateDynamicWidgets()
                self.entry_stueckzahl.placeForget()
                self.entry_stueckzahl_label.placeForget()
                self.entry_stueckzahl.clear()
            else:
                self.frame.placeForget()
                self.entry_stueckzahl.place(x=300, y=240, width=500, height=50)
                self.entry_stueckzahl_label.place(x=0, y=240, width=350, height=50)

        self.checkbox_group_wafer = CheckButtonGroup(True)

        self.checkbox_wafer = CustomCheckbutton(self.eingabeFelder, group=sg, checkButton=self.checkbox_group_wafer)
        self.checkbox_wafer.setCommand(checkbox_wafer_abfrage)
        self.checkbox_wafer.setText("Wafer:")
        self.checkbox_wafer.place(x=0, y=180, width=350, height=50)
        self.checkbox_wafer.setFont(30)
        self.checkbox_wafer.attachToolTip("Bitte ankreuzen wenn es sich um Wafer handelt")

        self.sperrvermerk_name_label = tk.Label(self.frame, group=sg)
        self.sperrvermerk_name_label.setText("Name: ")
        self.sperrvermerk_name_label.setFont(30)

        self.sperrvermerk_name_entry = tk.Entry(self.frame, group=sg)
        self.sperrvermerk_name_entry.setFont(30)
        self.sperrvermerk_name_label.place(x=325, y=60, width=200, height=50)
        self.sperrvermerk_name_entry.place(x=500, y=60, width=300, height=50)

        self.checkbox_group_sperrvermerk = CheckButtonGroup(True)

        def checkbox_sperrvermerk_abfrage():
            is_checkbox_sperrvermerk_ticked = self.checkbox_sperrvermerk.getValue()
            if is_checkbox_sperrvermerk_ticked:
                master.updateDynamicWidgets()

            else:
                pass

        self.checkbox_sperrvermerk = CustomCheckbutton(self.frame, group=sg,
                                                       checkButton=self.checkbox_group_sperrvermerk)

        self.checkbox_sperrvermerk.setCommand(checkbox_sperrvermerk_abfrage)

        self.checkbox_sperrvermerk.setText("Sperrvermerk: ")
        self.checkbox_sperrvermerk.place(x=0, y=60, width=350, height=50)
        self.checkbox_sperrvermerk.setFont(30)



        self.vermerk_label = tk.Label(self.frame, group=sg)
        self.vermerk_label.setText("Notiz:")
        self.vermerk_label.setFont(30)
        self.vermerk_label.place(0, 120, 300, 50)

        self.vermerk_entry = tk.Entry(self.frame, group=sg)
        self.vermerk_entry.attachToolTip("Notiz: ")
        self.vermerk_entry.setFont(30)
        self.vermerk_entry.place(300, 120, 500, 50)

        self.frame_wafer_entry = tk.LabelFrame(self.frame, group=sg)
        self.frame_wafer_entry.placeRelative(fixWidth=600 * Constants.resolution, fixHeight=750 * Constants.resolution,
                                             changeX=-50 * Constants.resolution, stickRight=True, changeY=0)

        self.wafereintraege_wafer = tk.TreeView(self.frame_wafer_entry, group=sg)
        self.wafereintraege_wafer.setSingleSelect()
        self.wafereintraege_wafer.placeRelative(changeY=-2 * Constants.resolution, changeX=-2 * Constants.resolution,
                                                changeHeight=-50 * Constants.resolution)
        self.wafereintraege_wafer.setTableHeaders("Name", "Menge")

        self.wafer_eingabe_add = tk.Button(self.frame_wafer_entry, group=sg)
        self.wafer_eingabe_add.placeRelative(changeY=-2 * Constants.resolution, changeX=-2 * Constants.resolution,
                                             fixHeight=50 * Constants.resolution, stickDown=True,
                                             xOffsetRight=65 * Constants.resolution)
        self.wafer_eingabe_add.setText("Hinzufügen")
        self.wafer_eingabe_add.setFont(20)
        self.wafer_eingabe_add.attachToolTip("Mit diesem Button können Sie einen Wafer hinzufuegen")
        self.wafer_eingabe_add.setCommand(self.wafer_eintrag_hinzufuegen_oeffnen)

        self.wafer_eingabe_remove = tk.Button(self.frame_wafer_entry, group=sg)
        self.wafer_eingabe_remove.placeRelative(changeY=-2 * Constants.resolution, changeX=-2 * Constants.resolution,
                                                fixHeight=50 * Constants.resolution, stickDown=True,
                                                xOffsetLeft=65 * Constants.resolution)
        self.wafer_eingabe_remove.setText("Entfernen")
        self.wafer_eingabe_remove.setFont(20)
        self.wafer_eingabe_remove.attachToolTip("Mit diesem Button können Sie einen Wafer Entfernen")
        self.wafer_eingabe_remove.setCommand(self.wafer_eintrag_entfernen)

        self.uebernehmen_button = tk.Button(self, group=sg)
        self.uebernehmen_button.setText("Speichern und \nSchließen")
        self.uebernehmen_button.setFont(30)
        self.uebernehmen_button.place(980 * Constants.resolution, 1275 * Constants.resolution,
                                      600 * Constants.resolution, 150 * Constants.resolution)
        self.uebernehmen_button.setCommand(self.speichern)
        self.uebernehmen_button.setCommand(self.einloggen)

        self.label_admin = tk.Label(self, text="°", group=sgnew)
        self.label_admin.placeRelative(fixWidth=100, fixHeight=120, stickDown=True, stickRight=True,
                                       changeY=+45)  # TODO:Anpassbar
        self.label_admin.setFont(100)
        self.label_admin.bind(enter_login, tk.EventType.LEFT_CLICK)

    def einloggen(self):
        uuid = lib.newID32()
        anzahl_eintraege = self.wafereintraege_wafer.length()

        def natural_sort_key(item):
            """Sortierschlüssel für Dictionaries mit 'Name'-Feld."""
            name = str(item.get("Name", "")).strip()
            if name.isdigit():
                return (0, int(name))

            parts = re.split(r'(\d+)', name)
            key = []
            for part in parts:
                if part.isdigit():
                    key.append(int(part))
                else:
                    key.append(str(part).lower())
            return (1, key)

        new_list = []

        for i in range(anzahl_eintraege):
            wafereintraege = self.wafereintraege_wafer.getDataByIndex(i)
            new_list.append(wafereintraege)
        lagerplatz_eingabe = tk.SimpleDialog.askString(Constants.master, "Bitte Einscannen!", "Lagerplatz")
        sorted_data = sorted(new_list, key=natural_sort_key)
        if lagerplatz_eingabe == "":
            self.fehlermeldung2 = tk.SimpleDialog.askWarning(self, "Kein Lagerplatz angegeben!", "Fehler")
            return

        if lagerplatz_eingabe is None:
            return
        sperrvermerkvalue = self.checkbox_sperrvermerk.getValue()

        product = lib.newWafer(uuid,
                               self.entry_typ.getValue(),
                               self.entry_charge.getValue(),
                               self.entry_stueckzahl.getValue(),
                               self.dropdown_verpackung.getValue(),
                               ["Eingelagert am: " + lib.getTime()],
                               sorted_data,
                               sperrvermerkvalue,
                               self.sperrvermerk_name_entry.getValue(),
                               self.vermerk_entry.getValue(),
                               self.dropdown_durchmesser.getValue(),
                               "",
                               lib.getTimeInTwoYears()
                               )

        lib.addEntry(lagerplatz_eingabe, product)
        lib.protocoll(lib.getTime(), "Eingelagert")
        lib.writeConfigLibary()
        lib.writeConfigStorage()
        lib.print_uuid(uuid)

        self.wafereintraege_wafer.clear()
        self.entry_typ.clear()
        self.entry_charge.clear()
        self.dropdown_verpackung.clear()
        self.entry_charge.clear()
        self.entry_stueckzahl.clear()

    def onShow(self, **kwargs):
        self.placeRelative()

    def onHide(self):
        self.placeForget()

    def speichern(self):
        self.openHomePage(mainpage)

    def wafer_eintrag_hinzufuegen_oeffnen(self):
        self.root.open()

    def wafer_eintrag_hinzufuegen_speichern(self):
        if self.root.wafer_stueckzahl_unbekannt_checkbox.getValue():
            wafer_stueckzahl = "Unbekannt"
        else:

            wafer_stueckzahl = self.root.entry_wafer_stueckzahl.getValue()

        wafer_name = self.root.entry_wafer_name.getValue()

        if wafer_name == "":
            self.root.printerror("Name kann nicht leer bleiben!")
            return

        if not self.root.wafer_stueckzahl_unbekannt_checkbox.getValue():

            if not wafer_stueckzahl.isnumeric():
                self.root.printerror("Stückzahl muss eine Zahl sein!")

                return
            wafer_stueckzahl = int(wafer_stueckzahl)
            if wafer_stueckzahl < 0:
                self.root.printerror("Stückzahl kann nicht Negativ sein!")

                return
        else:
            pass

        self.wafereintraege_wafer.addEntry(wafer_name.lower(), str(wafer_stueckzahl))
        self.root.hide()

    def wafer_eintrag_entfernen(self):
        getselected = self.wafereintraege_wafer.getSelectedIndex()

        if getselected is None:
            return

        self.wafereintraege_wafer.deleteItemByIndex(getselected)
# ------------------------------------------------------------------------------------------------------------------------


class Alte_ware_einlagern_page(tk.MenuPage):
    def __init__(self, master):
        super().__init__(master, sg)

        self.button_zurueck_einlagern = tk.Button(self, group=sg)
        self.button_zurueck_einlagern.setText("Zurück")
        self.button_zurueck_einlagern.setFont(30)
        self.button_zurueck_einlagern.placeRelative(centerX=True, centerY=True, changeY=-500 * Constants.resolution,
                                                    changeX=-800 * Constants.resolution,
                                                    fixWidth=400 * Constants.resolution,
                                                    fixHeight=200 * Constants.resolution)
        self.button_zurueck_einlagern.attachToolTip("Zurück", group=sg)
        self.button_zurueck_einlagern.setCommand(self.zurueck_button)

        self.label_admin = tk.Label(self, text="°", group=sgnew)
        self.label_admin.placeRelative(fixWidth=100, fixHeight=120, stickDown=True, stickRight=True,
                                       changeY=+45)  # TODO:Anpassbar
        self.label_admin.setFont(100)
        self.label_admin.bind(enter_login, tk.EventType.LEFT_CLICK)

        self.entry = tk.Entry(self, group=sg)
        self.entry.placeRelative(centerX=True, centerY=True, changeY=-500 * Constants.resolution,
                                 changeX=100 * Constants.resolution, fixWidth=1000 * Constants.resolution,
                                 fixHeight=100 * Constants.resolution)
        self.entry.setFont(40)
        self.entry.attachToolTip("Erwarte QR-CODE")
        self.entry.bind(self.get_on_search, tk.EventType.RETURN)

        self.label_admin = tk.Label(self, text="°", group=sgnew)
        self.label_admin.placeRelative(fixWidth=100, fixHeight=120, stickDown=True, stickRight=True,
                                       changeY=+45)  # TODO:Anpassbar
        self.label_admin.setFont(100)
        self.label_admin.bind(enter_login, tk.EventType.LEFT_CLICK)

        self.uebernehmen_button = tk.Button(self, group=sg)
        self.uebernehmen_button.setText("Speichern und \nSchließen")
        self.uebernehmen_button.setFont(30)

        self.uebernehmen_button.setCommand(self.abspeichern)

        self.label_typ = tk.Label(self, group=sg)

        self.label_charge = tk.Label(self, group=sg)

        self.stueckzahl_label = tk.Label(self, group=sg)

        self.stueckzahl = tk.Entry(self, group=sg)

    def onShow(self, **kwargs):
        self.placeRelative()
        self.entry.setFocus()

    def onHide(self):
        self.placeForget()

    def get_on_search(self):

        uuid = self.entry.getValue()

        data = lib.storageData

        storageData = {}
        # print(data)
        for values in data.values():
            for value in values:
                storageData[value] = value

        if uuid not in storageData and uuid in lib.libraryData:
            dataDict = lib.readUuid(uuid)

            self.label_typ.placeRelative(centerX=True, centerY=True, changeY=-300, fixWidth=500, fixHeight=50,
                                         changeX=-20)
            self.label_typ.setText("Typ: " + dataDict["typ"])
            self.label_typ.setFont(20)
            self.label_typ.setStyle(tk.Style.FLAT)

            self.label_charge.placeRelative(centerX=True, centerY=True, changeY=-240, fixWidth=500, fixHeight=50,
                                            changeX=-45)
            self.label_charge.setText("Charge: " + dataDict["charge"])
            self.label_charge.setFont(20)
            self.label_charge.setStyle(tk.Style.FLAT)

            self.uebernehmen_button.place(980 * Constants.resolution, 1275 * Constants.resolution,
                                          600 * Constants.resolution, 150 * Constants.resolution)

            self.stueckzahl_label.setText("Stückzahl:")
            self.stueckzahl_label.setFont(20)
            self.stueckzahl_label.setStyle(tk.Style.FLAT)

            self.stueckzahl.setText(dataDict["stueckzahl"])
            self.stueckzahl._get()["justify"] = "right"
            self.stueckzahl.setFont(20)

            self.dropdown_frame_verpackung_label = tk.Label(self, sg)
            self.dropdown_frame_verpackung_label.setFont(20)
            self.dropdown_frame_verpackung_label.setText("Verpackung: ")

            self.dropdown_frame = tk.LabelFrame(self, group=sg)


            self.dropdown_verpackung = tk.DropdownMenu(self.dropdown_frame, group=sg,
                                                       optionList=["Single-Frameshipper", "Frameshipper", "Tape & Reel",
                                                                   "8 Zoll Box", " 6 Zoll Box", "Andere"])

            self.dropdown_verpackung.setFont(20)
            self.dropdown_verpackung.attachToolTip("Verpackung auswählen")

            if dataDict["wafer"] == []:
                self.stueckzahl.placeRelative(centerX=True, centerY=True, changeY=-180, fixWidth=150, fixHeight=50,
                                              changeX=80)
                self.stueckzahl_label.placeRelative(centerX=True, centerY=True, changeY=-180, fixWidth=150,
                                                    fixHeight=50, changeX=-80)

            else:
                a =lib.readUuid(uuid)

                if a["abspaltung"] == "":
                    self.dropdown_verpackung.setValue(a["verpackung"])
                else:
                    self.dropdown_verpackung.setValue(lib.readUuid(a["abspaltung"])["verpackung"])

                self.entries = []
                self.labels = []
                self.list_entries_and_labels = []
                self.headline = tk.Label(self, group=sg)
                self.dropdown_frame_verpackung_label.placeRelative(centerX=True, changeY=100,changeX=-125,centerY=True, fixWidth=300, fixHeight=30)
                self.headline.setText(" Nummer:                Stückzahl:   ")
                self.headline.setFont(20)
                self.headline.placeRelative(centerX=True, fixHeight=50, fixWidth=600, changeY=340)
                self.dropdown_frame.placeRelative(centerX=True, changeY=100,changeX=125,centerY=True, fixWidth=300, fixHeight=30)
                self.dropdown_verpackung.place(x=0, y=0, width=297, height=26)
                self.wafer_frame = tk.ScrollableFrame(self,1000,600,contrastcolorsg)

                self.wafer_frame.placeRelative(centerX=True,centerY=True, fixWidth=600,fixHeight=200,changeY=-50)
                self.label_unbekannt = tk.Label(self.wafer_frame, contrastcolorsg)
                self.label_unbekannt.setText("Unbekannt")
                self.label_unbekannt.setFont(20)
                selectedEntries = lib.readUuid(uuid)["wafer"]

                for i in range(len(selectedEntries)):
                    entry = tk.Entry(self.wafer_frame, contrastcolorsg)
                    label = tk.Label(self.wafer_frame, contrastcolorsg)
                    if selectedEntries[i]["Menge"] == "Unbekannt":

                        entry.setStyle(tk.Style.FLAT)
                        label.setText(str(selectedEntries[i]["Name"]))
                        entry.setText("Unbekannt")
                        self.label_unbekannt.placeRelative(fixHeight=30, fixWidth=250, fixY=10 + i * 50, fixX=330)
                        label.placeRelative(fixHeight=30, fixWidth=250, fixY=10 + i * 50, fixX=0)
                    else:
                        label.setText(str(selectedEntries[i]["Name"]))
                        entry.setText(selectedEntries[i]["Menge"])
                        entry.placeRelative(fixHeight=30, fixWidth=100, fixY=10 + i * 50, fixX=400)
                        label.placeRelative(fixHeight=30, fixWidth=250, fixY=10 + i * 50, fixX=0)

                    entry.setFont(20)
                    label.setFont(20)
                    self.labels.append(label)
                    self.entries.append(entry)
                    self.list_entries_and_labels = []

        elif uuid in storageData and uuid in lib.libraryData:
            self.entry.clear()
            self.fehlermeldung = tk.SimpleDialog.askWarning(self, "Bereits einglagert!", "Fehler")

        else:
            self.entry.clear()
            self.fehlermeldung2 = tk.SimpleDialog.askWarning(self, "Scan unbekannt", "Fehler")

    def lagerplatz_eingabe(self):
        lagerplatz_eingabe = tk.SimpleDialog.askString(Constants.master, "Bitte Einscannen!", "Lagerplatz",
                                                       hideWith="*")
        return str(lagerplatz_eingabe)

    def abspeichern(self):

        uuid = self.entry.getValue()
        data = lib.readUuid(uuid)["abspaltung"]
        if lib.readUuid(uuid)["wafer"] == []:
            if len(data) == 32 and any(data in sublist for sublist in lib.storageData.values()):  # Wenn in "abspaltungen" eine uuid ist und diese Uuid in storage ist

                for keys in lib.libraryData:
                    if uuid == keys:
                        lib.readUuid(data)["stueckzahl"] = str(
                            int(lib.readUuid(data)["stueckzahl"]) + int(self.stueckzahl.getValue()))

                        del lib.libraryData[uuid]
                        #Blankes label priten zum überkleben der alten uuid
                        lib.writeConfigLibary()
                        lib.writeConfigStorage()
                        self.entry.clear()
                        #self.dropdown_frame.placeForget()
                        self.stueckzahl_label.placeForget()
                        self.label_charge.placeForget()
                        self.stueckzahl.placeForget()
                        self.label_typ.placeForget()
                        #self.label_verpackung.placeForget()
                        self.uebernehmen_button.placeForget()
                        self.openHomePage(mainpage)
                        print("Fall 1")

                        self.lagerplatz_info = tk.SimpleDialog.askInfo(self,
                                                                       "Einzulagern in Fach " + lib.getAblagePlatz(data) + "\n"+"Aktuellen QR-Code bitte überkleben",
                                                                       "Info")
                        break

            elif any(uuid in sublist for sublist in lib.abspaltungenZurueckgeben()):  # Wenn der Eintrag in einer der Abspaltungen aller storage einträge
                a = list(lib.abspaltungenZurueckgebenMitUuid().keys())[0]
                lib.readUuid(uuid)["stueckzahl"] = str(int(lib.readUuid(uuid)["stueckzahl"]) + int(
                    lib.readUuid(list(lib.abspaltungenZurueckgebenMitUuid().keys())[0])["stueckzahl"]))

                lib.reEntry(lib.getAblagePlatz(list(lib.abspaltungenZurueckgebenMitUuid().keys())[0]), uuid)
                lib.delEntry(list(lib.abspaltungenZurueckgebenMitUuid().keys())[0])

                del lib.libraryData[a]

                lib.writeConfigLibary()
                lib.writeConfigStorage()
                self.entry.clear()
                print("Fall 2")
                #self.dropdown_frame.placeForget()
                self.stueckzahl_label.placeForget()
                self.label_charge.placeForget()
                self.stueckzahl.placeForget()
                self.label_typ.placeForget()
                #self.label_verpackung.placeForget()
                self.uebernehmen_button.placeForget()
                self.openHomePage(mainpage)

            elif any(lib.readUuid(uuid)["abspaltung"] in sublist for sublist in lib.abspaltungenZurueckgeben()):
                wantedUuid = lib.readUuid(list(lib.abspaltungenZurueckgebenMitUuid().keys())[0])["uuid"]
                lib.readUuid(wantedUuid)["stueckzahl"] = str(
                    int(lib.readUuid(wantedUuid)["stueckzahl"]) + int(lib.readUuid(uuid)["stueckzahl"]))

                del lib.libraryData[uuid]

                lib.writeConfigLibary()
                lib.writeConfigStorage()
                self.entry.clear()
                print("Fall 3")
                #self.dropdown_frame.placeForget()
                self.stueckzahl_label.placeForget()
                self.label_charge.placeForget()
                self.stueckzahl.placeForget()
                self.label_typ.placeForget()
                #self.label_verpackung.placeForget()
                self.uebernehmen_button.placeForget()
                self.openHomePage(mainpage)
            else:
                # print(lib.readUuid(uuid)["stueckzahl"])
                lib.readUuid(uuid)["stueckzahl"] = self.stueckzahl.getValue()
                #lib.readUuid(uuid)["verpackung"] = self.dropdown_verpackung.getValue()
                lib.reEntry(self.lagerplatz_eingabe(), uuid)
                lib.writeConfigLibary()
                lib.writeConfigStorage()
                self.entry.clear()
                #self.dropdown_frame.placeForget()
                self.stueckzahl_label.placeForget()
                self.label_charge.placeForget()
                self.stueckzahl.placeForget()
                self.label_typ.placeForget()
                #self.label_verpackung.placeForget()
                self.uebernehmen_button.placeForget()
                self.openHomePage(mainpage)
                print("Fall 4")
        else:
            print("Wafer Sonderbehandlung")
            if len(data) == 32 and any(data in sublist for sublist in lib.storageData.values()):
                for keys in lib.libraryData:

                    if uuid == keys:

                        if lib.readUuid(data)["verpackung"] == self.dropdown_verpackung.getValue():
                            print(self.dropdown_verpackung.getValue())
                            #data ist die hauptcharge die bearbeitet werden muss
                            #uuid ist die charge die wieder eingelagert wird

                            for i in range(len(self.labels)):
                                if self.entries[i].getValue() != "Unbekannt":

                                    self.list_entries_and_labels.append(
                                        {"Name": self.labels[i].getText(), "Menge": int(self.entries[i].getValue())})
                                elif self.entries[i].getValue() == "Unbekannt":
                                    self.list_entries_and_labels.append(
                                        {"Name": self.labels[i].getText(), "Menge": str("Unbekannt")})
                                else:
                                    print("Fehler")



                            list1 = lib.readUuid(data)["wafer"]
                            list2 = self.list_entries_and_labels
                            print(list1 + list2)

                            dict1 = {item['Name']: item['Menge'] for item in list1}
                            dict2 = {item['Name']: item['Menge'] for item in list2}

                            # Alle eindeutigen Namen sammeln
                            alle_namen = set(dict1.keys()).union(dict2.keys())

                            result = []

                            for name in alle_namen:
                                menge1 = dict1.get(name)
                                menge2 = dict2.get(name)

                                if isinstance(menge1, (int, float)) and isinstance(menge2, (int, float)):
                                    menge_sum = menge1 + menge2
                                elif menge1 is None:
                                    menge_sum = menge2
                                elif menge2 is None:
                                    menge_sum = menge1
                                else:
                                    menge_sum = "Unbekannt"

                                result.append({'Name': name, 'Menge': menge_sum})

                            def natural_sort_key(item):
                                """Sortierschlüssel für Dictionaries mit 'Name'-Feld."""
                                name = str(item.get("Name", "")).strip()
                                if name.isdigit():
                                    return (0, int(name))

                                parts = re.split(r'(\d+)', name)
                                key = []
                                for part in parts:
                                    if part.isdigit():
                                        key.append(int(part))
                                    else:
                                        key.append(str(part).lower())
                                return (1, key)

                            result_sorted = sorted(result, key=natural_sort_key)
                            lib.readUuid(data)["wafer"] = result_sorted
                            self.lagerplatz_info = tk.SimpleDialog.askInfo(self,
                                                                           "Einzulagern in Fach " + lib.getAblagePlatz(
                                                                               data) + "\n" + "Aktuellen QR-Code bitte überkleben",
                                                                           "Info")

                            del lib.libraryData[uuid]
                            # Blankes label priten zum überkleben der alten uuid
                        else:

                            lib.readUuid(uuid)["abspaltung"] = ""
                            lib.readUuid(uuid)["verpackung"] = self.dropdown_verpackung.getValue()
                            lib.reEntry(self.lagerplatz_eingabe(),uuid)

                        lib.writeConfigLibary()
                        lib.writeConfigStorage()

                        self.entry.clear()
                        self.dropdown_frame_verpackung_label.placeForget()
                        self.stueckzahl_label.placeForget()
                        self.label_charge.placeForget()
                        self.stueckzahl.placeForget()
                        self.label_typ.placeForget()
                        self.dropdown_frame.placeForget()
                        self.headline.placeForget()
                        self.wafer_frame.getOuterFrame().placeForget()
                        self.uebernehmen_button.placeForget()
                        self.openHomePage(mainpage)
                        print("Fall 1 Wafer")
                        break

            elif any(uuid in sublist for sublist in lib.abspaltungenZurueckgeben()):  # Wenn der Eintrag in einer der Abspaltungen aller storage einträge
                a = list(lib.abspaltungenZurueckgebenMitUuid().keys())[0]
                print("Fall 2 Wafer")
                if lib.readUuid(data)["verpackung"] == self.dropdown_verpackung.getValue():
                    print(self.dropdown_verpackung.getValue())
                    # data ist die hauptcharge die bearbeitet werden muss
                    # uuid ist die charge die wieder eingelagert wird
                    list1 = lib.readUuid(uuid)["wafer"]
                    list2 = lib.readUuid(data)["wafer"]

                    dict1 = {item['Name']: item['Menge'] for item in list1}
                    dict2 = {item['Name']: item['Menge'] for item in list2}

                    # Alle eindeutigen Namen sammeln
                    alle_namen = set(dict1.keys()).union(dict2.keys())

                    result = []

                    for name in alle_namen:
                        menge1 = dict1.get(name)
                        menge2 = dict2.get(name)

                        if isinstance(menge1, (int, float)) and isinstance(menge2, (int, float)):
                            menge_sum = menge1 + menge2
                        elif menge1 is None:
                            menge_sum = menge2
                        elif menge2 is None:
                            menge_sum = menge1
                        else:
                            menge_sum = "Unbekannt"

                        result.append({'Name': name, 'Menge': menge_sum})
                    result_sorted = sorted(result,
                                           key=lambda x: int(x['Name']) if x['Name'].isdigit() else x['Name'])
                    lib.readUuid(data)["wafer"] = result_sorted
                    self.lagerplatz_info = tk.SimpleDialog.askInfo(self,
                                                                   "Einzulagern in Fach " + lib.getAblagePlatz(
                                                                       data) + "\n" + "Aktuellen QR-Code bitte überkleben",
                                                                   "Info")
                    del lib.libraryData[uuid]
                    # Blankes label priten zum überkleben der alten uuid
                else:

                    lib.readUuid(uuid)["abspaltung"] = ""
                    lib.readUuid(uuid)["verpackung"] = self.dropdown_verpackung.getValue()
                    lib.reEntry(self.lagerplatz_eingabe(), uuid)
                lib.reEntry(lib.getAblagePlatz(list(lib.abspaltungenZurueckgebenMitUuid().keys())[0]), uuid)
                lib.delEntry(list(lib.abspaltungenZurueckgebenMitUuid().keys())[0])

                del lib.libraryData[a]

                lib.writeConfigLibary()
                lib.writeConfigStorage()

                self.entry.clear()
                self.dropdown_frame_verpackung_label.placeForget()
                self.stueckzahl_label.placeForget()
                self.label_charge.placeForget()
                self.stueckzahl.placeForget()
                self.label_typ.placeForget()
                self.dropdown_frame.placeForget()
                self.headline.placeForget()
                self.wafer_frame.getOuterFrame().placeForget()
                self.uebernehmen_button.placeForget()
                self.openHomePage(mainpage)

            elif any(lib.readUuid(uuid)["abspaltung"] in sublist for sublist in lib.abspaltungenZurueckgeben()):
                wantedUuid = lib.readUuid(list(lib.abspaltungenZurueckgebenMitUuid().keys())[0])["uuid"]
                print("Fall 3 Wafer")
                if lib.readUuid(data)["verpackung"] == self.dropdown_verpackung.getValue():
                    print(self.dropdown_verpackung.getValue())
                    # data ist die hauptcharge die bearbeitet werden muss
                    # uuid ist die charge die wieder eingelagert wird
                    list1 = lib.readUuid(uuid)["wafer"]
                    list2 = lib.readUuid(wantedUuid)["wafer"]

                    dict1 = {item['Name']: item['Menge'] for item in list1}
                    dict2 = {item['Name']: item['Menge'] for item in list2}

                    # Alle eindeutigen Namen sammeln
                    alle_namen = set(dict1.keys()).union(dict2.keys())

                    result = []

                    for name in alle_namen:
                        menge1 = dict1.get(name)
                        menge2 = dict2.get(name)

                        if isinstance(menge1, (int, float)) and isinstance(menge2, (int, float)):
                            menge_sum = menge1 + menge2
                        elif menge1 is None:
                            menge_sum = menge2
                        elif menge2 is None:
                            menge_sum = menge1
                        else:
                            menge_sum = "Unbekannt"

                        result.append({'Name': name, 'Menge': menge_sum})
                    result_sorted = sorted(result,
                                           key=lambda x: int(x['Name']) if x['Name'].isdigit() else x['Name'])
                    lib.readUuid(data)["wafer"] = result_sorted
                    self.lagerplatz_info = tk.SimpleDialog.askInfo(self,
                                                                   "Einzulagern in Fach " + lib.getAblagePlatz(
                                                                       data) + "\n" + "Aktuellen QR-Code bitte überkleben",
                                                                   "Info")

                    del lib.libraryData[uuid]
                    # Blankes label priten zum überkleben der alten uuid
                else:

                    lib.readUuid(uuid)["abspaltung"] = ""
                    lib.readUuid(uuid)["verpackung"] = self.dropdown_verpackung.getValue()
                    lib.reEntry(self.lagerplatz_eingabe(), uuid)

                del lib.libraryData[uuid]

                lib.writeConfigLibary()
                lib.writeConfigStorage()

                self.entry.clear()
                self.dropdown_frame_verpackung_label.placeForget()
                self.stueckzahl_label.placeForget()
                self.label_charge.placeForget()
                self.stueckzahl.placeForget()
                self.label_typ.placeForget()
                self.dropdown_frame.placeForget()
                self.headline.placeForget()
                self.wafer_frame.getOuterFrame().placeForget()
                self.uebernehmen_button.placeForget()
                self.openHomePage(mainpage)

            else:
                print("Fall 4 Wafer")
                lib.reEntry(self.lagerplatz_eingabe(), uuid)
                lib.readUuid(uuid)["verpackung"] = self.dropdown_verpackung.getValue()
                lib.writeConfigLibary()
                lib.writeConfigStorage()
                self.entry.clear()
                self.dropdown_frame_verpackung_label.placeForget()
                self.stueckzahl_label.placeForget()
                self.label_charge.placeForget()
                self.stueckzahl.placeForget()
                self.label_typ.placeForget()
                self.dropdown_frame.placeForget()
                self.headline.placeForget()
                self.wafer_frame.getOuterFrame().placeForget()
                self.uebernehmen_button.placeForget()
                self.openHomePage(mainpage)

    def zurueck_button(self):
        self.openLastMenuPage()
        self.dropdown_frame.placeForget()
        self.headline.placeForget()
        self.wafer_frame.getOuterFrame().placeForget()
        self.entry.clear()
        self.dropdown_frame_verpackung_label.placeForget()
        self.stueckzahl_label.placeForget()
        self.label_charge.placeForget()
        self.stueckzahl.placeForget()
        self.label_typ.placeForget()
        self.uebernehmen_button.placeForget()
        self.entry.clear()
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
class Search_page(tk.MenuPage):
    def __init__(self, master):
        super().__init__(master, sg)
        self.fehlermeldung = None
        Constants.adminLoginUpdateHook.append(self.onAdminChange)
        Constants.adminLoginUpdateHook.append(self.update_treeview)
        Constants.adminLoginUpdateHook.append(self.clearWhenAdminFalse)
        self.master = master
        self.treeview_content = []
        self.rootWafer = PickWaferToOutSource(self.master, sg)
        self.rootNoWafer = PickAmountToOutSource(self.master, sg)


        self.entry = tk.Entry(self, group=sg)
        self.entry.placeRelative(centerX=True, centerY=True, changeY=-500 * Constants.resolution,
                                 changeX=100 * Constants.resolution, fixWidth=1000 * Constants.resolution,
                                 fixHeight=100 * Constants.resolution)
        self.entry.setFont(40)
        self.entry.attachToolTip("Erwarte Suche")
        self.entry.onUserInputEvent(self.get_on_search)

        self.button_zurueck_einlagern = tk.Button(self, group=sg)
        self.button_zurueck_einlagern.setText("Zurück")
        self.button_zurueck_einlagern.setFont(30)
        self.button_zurueck_einlagern.placeRelative(centerX=True, centerY=True, changeY=-500 * Constants.resolution,
                                                    changeX=-800 * Constants.resolution,
                                                    fixWidth=400 * Constants.resolution,
                                                    fixHeight=200 * Constants.resolution)
        self.button_zurueck_einlagern.attachToolTip("Zurück", group=sg)
        self.button_zurueck_einlagern.setCommand(self.openLastMenuPage)
        self.button_zurueck_einlagern.setCommand(self.druckerButtonForget)


        self.label_admin = tk.Label(self, text="°", group=sgnew)
        self.label_admin.placeRelative(fixWidth=100, fixHeight=120, stickDown=True, stickRight=True,
                                       changeY=+45)  # TODO:Anpassbar
        self.label_admin.setFont(100)
        self.label_admin.bind(enter_login, tk.EventType.LEFT_CLICK)

        self.filter_label = tk.Label(self, group=sg)
        self.filter_label.setText("Filter\nauswählen:")
        self.filter_label.setFont(20)
        self.filter_label.place(1950, 150, 150, 75)

        self.uuid_frame = tk.LabelFrame(self, group=sg)

        def checkbox_uuid_abfrage():
            is_check_box_uuid_ticked = self.checkbox_uuid.getValue()

            if is_check_box_uuid_ticked:
                self.charge_frame.place()
            else:
                self.charge_frame.placeForget()

        self.checkbox_group = CheckButtonGroup(False)

        self.checkbox_uuid = CustomCheckbutton(self, group=sg, checkButton=self.checkbox_group)
        self.checkbox_uuid.setFont(20)
        self.checkbox_uuid.place(2350 * Constants.resolution, 150 * Constants.resolution, 40 * Constants.resolution,
                                 40 * Constants.resolution)
        self.checkbox_uuid.setCommand(checkbox_uuid_abfrage)
        self.checkbox_uuid.setCommand(self.update_treeview)
        self.checkbox_uuid_label = tk.Label(self, group=sg)
        self.checkbox_uuid_label.setText("Scan")
        self.checkbox_uuid_label.setFont(20)
        self.checkbox_uuid_label.place(2137 * Constants.resolution, 150 * Constants.resolution,
                                       200 * Constants.resolution, 40 * Constants.resolution)

        self.lagerplatz_frame = tk.LabelFrame(self, group=sg)

        def checkbox_lagerplatz_abfrage():
            is_check_box_lagerplatz_ticked = self.checkbox_uuid.getValue()

            if is_check_box_lagerplatz_ticked:
                self.lagerplatz_frame.place()
            else:
                self.lagerplatz_frame.placeForget()

        self.checkbox_lagerplatz = CustomCheckbutton(self, group=sg, checkButton=self.checkbox_group)
        self.checkbox_lagerplatz.setFont(20)

        self.checkbox_lagerplatz.setCommand(self.update_treeview)
        self.checkbox_lagerplatz_label = tk.Label(self, group=sg)
        self.checkbox_lagerplatz_label.setText("Lagerplatz")
        self.checkbox_lagerplatz_label.setFont(20)

        self.typ_frame = tk.LabelFrame(self, group=sg)

        def checkbox_typ_abfrage():
            is_check_box_typ_ticked = self.checkbox_charge.getValue()

            if is_check_box_typ_ticked:
                self.typ_frame.place()
            else:
                self.typ_frame.placeForget()

        self.checkbox_typ = CustomCheckbutton(self, group=sg, checkButton=self.checkbox_group)
        self.checkbox_typ.setFont(20)
        self.checkbox_typ.setCommand(self.update_treeview)
        # self.checkbox_typ.setCommand(checkbox_typ_abfrage)
        self.checkbox_typ.place(2350 * Constants.resolution, 250 * Constants.resolution, 40 * Constants.resolution,
                                40 * Constants.resolution)
        self.checkbox_typ_label = tk.Label(self, group=sg)
        self.checkbox_typ_label.setText("Typ")
        self.checkbox_typ_label.setFont(20)
        self.checkbox_typ_label.place(2200 * Constants.resolution, 250 * Constants.resolution,
                                      60 * Constants.resolution, 40 * Constants.resolution)

        self.charge_frame = tk.LabelFrame(self, group=sg)

        def checkbox_charge_abfrage():
            is_check_box_charge_ticked = self.checkbox_charge.getValue()

            if is_check_box_charge_ticked:
                self.charge_frame.place()
            else:
                self.charge_frame.placeForget()

        self.checkbox_charge = CustomCheckbutton(self, group=sg, checkButton=self.checkbox_group)
        self.checkbox_charge.setFont(20)
        self.checkbox_charge.place(2350 * Constants.resolution, 200 * Constants.resolution, 40 * Constants.resolution,
                                   40 * Constants.resolution)
        self.checkbox_charge.setCommand(self.update_treeview)
        self.checkbox_charge_label = tk.Label(self, group=sg)
        self.checkbox_charge_label.setText("Charge")
        self.checkbox_charge_label.setFont(20)
        self.checkbox_charge_label.place(2150 * Constants.resolution, 200 * Constants.resolution,
                                         200 * Constants.resolution, 40 * Constants.resolution)

        self.treeview_suche = tk.TreeView(self, group=sg)
        self.treeview_suche.setSingleSelect()
        self.treeview_suche.placeRelative(centerX=True, centerY=True, changeY=125 * Constants.resolution,
                                          changeX=100 * Constants.resolution, fixWidth=1000 * Constants.resolution,
                                          fixHeight=1100 * Constants.resolution)

        self.treeview_suche.onSingleSelectEvent(self.printtest)

        self.scrollbar = tk.ScrollBar(self)
        self.treeview_suche.attachVerticalScrollBar(self.scrollbar)
        self.treeview_suche.setTableHeaders("Typ", "Charge", "Im Lager", "SV")

        self.ausgabetext = tk.Text(self, group=sg,readOnly= True)
        self.ausgabetext.setStyle(tk.Style.FLAT)
        self.ausgabetext.setFont(20)
        self.ausgabetext.placeRelative(centerY=True, stickRight=True, fixHeight=525 * Constants.resolution,
                                       fixWidth=630 * Constants.resolution, changeX=-10)


        self.auslagern_button = tk.Button(self, group=sg)
        self.auslagern_button.setFont(20)
        self.auslagern_button.setText("Auslagern")
        self.auslagern_button.setCommand(self.outsourceTreeview)
        self.rootNoWafer.button_wafer_auslagern.setCommand(self.abspaltenNoWafer)
        self.rootWafer.button_wafer_auslagern.setCommand(self.abspalten)

        self.protocoll = tk.Text(self, group=sg, readOnly=True)
        self.protocoll.setFont(20)
        self.printUuidSticker = tk.Button(self,group = sg)
        self.printUuidSticker.setText("QR Code Drucken")
        self.printUuidSticker.setFont(15)
        self.printUuidSticker.setCommand(self.printUuidStickr)


        self.protocollButton = tk.Button(self, group=sg)
        self.protocollButton.setText("Protokoll")
        self.protocollButton.setFont(20)
        self.treeview_suche.onSingleSelectEvent(self.auslagern_button.placeForget)
        self.protocollButton.setCommand(self.showProtocol)
        self.protocollButton.setCommand(self.writeProtocol)

        self.protocollButtonState = 0

    def printUuidStickr(self):
        uuid = self.getSelectedUuid()
        lib.testPrint(uuid)
        lib.print_uuid(uuid)


    def writeProtocol(self):
        uuid = self.getSelectedUuid()
        dict = lib.readUuid(uuid)

        self.protocoll.clear()

        for i in range(len(dict["protokoll"])):
            self.protocoll.addText(dict.get("protokoll")[i])
            self.protocoll.addText(2*"\n")

    def showProtocol(self):
        if self.protocollButtonState == 0:
            self.protocoll.placeRelative(changeX=175 * Constants.resolution, stickDown=True,
                                         changeY=-190 * Constants.resolution, fixWidth=625 * Constants.resolution,
                                         fixHeight=700 * Constants.resolution)
            self.protocollButtonState = 1
        else:
            self.protocoll.clear()
            self.protocoll.placeForget()

            self.protocollButtonState = 0

    def outsourceTreeview(self):
        uuid = self.getUuid()
        content = lib.readUuid(uuid)
        if content["wafer"] == []:
            self.rootNoWafer.open()
            self.rootNoWafer.stueckzahl_alt_von.setText("von " + content["stueckzahl"])
            self.rootNoWafer.stueckzahl_alt.setText(content["stueckzahl"])

        else:

            self.rootWafer.open()
            self.rootWafer.wafer_treeview_auswahl.clear()

            for i in content["wafer"]:

                self.rootWafer.wafer_treeview_auswahl.addEntry(i["Name"], i["Menge"])

    def printtest(self):
        uuid = self.getSelectedUuid()
        if uuid is None:
            return
        self.ausgabe_anzeigen(uuid)
        self.printUuidSticker.placeRelative(centerX=True,stickDown=True,fixWidth=200,fixHeight=100, changeX=-600, changeY = -10)
    def getUuid(self):
        return self.getSelectedUuid()

    def abspalten(self):

        # print(self.wafer_treeview_auswahl.getSelectedItem())
        data_list = self.rootWafer.wafer_treeview_auswahl.getSelectedItem()
        if data_list is None:
            self.rootWafer.cancel()
            return
        self.root = AmountToOutSource(self.master, sg, self, data_list)
        self.root.button_wafer_auslagern.setCommand(self.auslesen)
        self.rootWafer.hide()
        self.root.open()

    def auslesen(self):
        uuid = self.getSelectedUuid()
        self.data = []
        for i in range(len(self.root.labels)):
            if self.root.entries[i].getValue() != "Unbekannt":

                self.data.append({"Name": self.root.labels[i].getText(), "Menge": int(self.root.entries[i].getValue())})
            elif self.root.entries[i].getValue() == "Unbekannt":
                self.data.append({"Name": self.root.labels[i].getText(), "Menge": str("Unbekannt")})
            else:
                print("Fehler")

        neue_stueckzahl = 0
        for eintrag in self.data:
            menge = eintrag["Menge"]
            if isinstance(menge, (int, float)):
                neue_stueckzahl = neue_stueckzahl + menge

        print(neue_stueckzahl)
        gesamtmenge = sum(item["Menge"] for item in lib.readUuid(uuid)["wafer"] if isinstance(item["Menge"], int))

        print(gesamtmenge)
        if int(gesamtmenge)-int(neue_stueckzahl) < 0:
            self.fehlermeldung = tk.SimpleDialog.askWarning(self.rootWafer,
                                                            "Soviele können nicht ausgelagert werden!", "Fehler")
        elif int(gesamtmenge) == int(neue_stueckzahl):
            lib.delEntry(uuid)
            lib.writeConfigStorage()
            lib.writeConfigLibary()

        else:


            newuuid = lib.newID32()

            product = lib.newWafer(
                newuuid,
                lib.readUuid(self.getSelectedUuid())["typ"],
                lib.readUuid(self.getSelectedUuid())["charge"],
                lib.readUuid(self.getSelectedUuid())["stueckzahl"],
                lib.readUuid(self.getSelectedUuid())["verpackung"],
                ["Ausgelagert am: " + lib.getTime()],
                self.data,
                lib.readUuid(self.getSelectedUuid())["sperr_vermerk"],
                lib.readUuid(self.getSelectedUuid())["sperr_vermerk_nummer"],
                self.root.vermerk_entry.getValue(),
                lib.readUuid(self.getSelectedUuid())["durchmesser"],
                self.getSelectedUuid(),
                lib.getTimeInTwoYears()
                )

            lib.libraryData[product["uuid"]] = product

            liste = self.data

            liste2 = lib.readUuid(self.getSelectedUuid())["wafer"]

            result1 = {item['Name']: item['Menge'] for item in liste}

            result2 = {item['Name']: item['Menge'] for item in liste2}

            def to_int(value):
                try:
                    return int(value)
                except (ValueError, TypeError):
                    return "Unbekannt"  # Falls der Wert nicht konvertierbar ist

            # Alle Schlüssel aus beiden Dictionaries sammeln
            all_keys = set(result1.keys()).union(result2.keys())

            # Berechnung der Differenzen mit Fehlerprüfung
            result = {}
            for key in all_keys:
                val_1 = to_int(result1.get(key))
                val_2 = to_int(result2.get(key))

                if val_1 == "Unbekannt" and val_2 == "Unbekannt":
                    result[key] = "Unbekannt"
                elif val_1 == "Unbekannt" and val_2 != "Unbekannt":
                    result[key] = val_2
                else:
                    diff = val_2 - val_1
                    if diff < 0:
                        self.fehlermeldung = tk.SimpleDialog.askWarning(self.rootWafer,
                                                                        "Soviele können nicht ausgelagert werden!",
                                                                        "Fehler")

                        return
                    result[key] = diff

            def natural_sort_key(item):
                """Sortierschlüssel für Dictionaries mit 'Name'-Feld."""
                name = str(item.get("Name", "")).strip()
                if name.isdigit():
                    return (0, int(name))

                parts = re.split(r'(\d+)', name)
                key = []
                for part in parts:
                    if part.isdigit():
                        key.append(int(part))
                    else:
                        key.append(str(part).lower())
                return (1, key)

            liste = [{"Name": str(key), "Menge": value} for key, value in result.items()]

            sorted_data = sorted(liste, key=natural_sort_key)

            lib.readUuid(self.getSelectedUuid())["wafer"] = sorted_data

            waferstueckzahlcounter = 0

            for i in lib.readUuid(newuuid)["wafer"]:

                if i["Menge"] != "Unbekannt":

                    waferstueckzahlcounter = waferstueckzahlcounter + (
                        int(i["Menge"]))
                    if waferstueckzahlcounter == 0:
                        waferstueckzahlcounter = "Unbekannt"


            lib.readUuid(uuid)["protokoll"] = [
                "Am " + lib.getTime() + " wurden " + str(
                    waferstueckzahlcounter) + " Stueck ausgelagert, Notiz: " + self.root.vermerk_entry.getValue()]+lib.readUuid(uuid)["protokoll"]

        lib.writeConfigStorage()
        lib.writeConfigLibary()
        self.update_treeview()
        self.root.hide()

    def abspaltenNoWafer(self):

        uuid = self.getSelectedUuid()
        neue_stueckzahl = int(lib.readUuid(uuid)["stueckzahl"]) - int(self.rootNoWafer.stueckzahl_alt.getValue())

        if neue_stueckzahl < 0:
            self.fehlermeldung = tk.SimpleDialog.askWarning(self.rootNoWafer,
                                                            "Soviele können nicht ausgelagert werden!", "Fehler")

        elif neue_stueckzahl == 0:

            lib.delEntry(uuid)
            lib.writeConfigStorage()
            lib.writeConfigLibary()
            self.rootNoWafer.hide()
            self.update_treeview()

        else:
            lib.readUuid(uuid)["protokoll"] = ["Am " + lib.getTime() +" wurden " + self.rootNoWafer.stueckzahl_alt.getValue() + " Stueck ausgelagert, Notiz: " + self.rootNoWafer.vermerk_entry.getValue()] + lib.readUuid(uuid)["protokoll"]
            lib.readUuid(uuid)["stueckzahl"] = str(neue_stueckzahl)
            lib.writeConfigLibary()
            lib.writeConfigStorage()

            if lib.readUuid(uuid)["abspaltung"] != "":
                uuid = lib.readUuid(uuid)["abspaltung"]
            new_uuid = lib.newID32()
            contentData = lib.newWafer(
                new_uuid,
                lib.readUuid(uuid)["typ"],
                lib.readUuid(uuid)["charge"],
                self.rootNoWafer.stueckzahl_alt.getValue(),
                self.rootNoWafer.dropdown_verpackung.getValue(),
                ["Ausgelagert am: " + lib.getTime()],
                [],
                "",
                "",
                self.rootNoWafer.vermerk_entry.getValue(),
                "",
                uuid,
                lib.getTimeInTwoYears()
            )
            lib.print_uuid(new_uuid)
            self.rootNoWafer.dropdown_verpackung.clear()
            self.rootNoWafer.vermerk_entry.clear()
            self.rootNoWafer.hide()
            lib.libraryData[contentData["uuid"]] = contentData
            lib.protocoll(lib.getTime(), "Eingelagert")
            lib.writeConfigLibary()
            lib.writeConfigStorage()
            self.update_treeview()

    def getSelectedUuid(self):
        a = self.treeview_suche.getSelectedIndex()
        if a is None:
            return
        b = self.treeview_content[a]
        if a is None:
            return
        return (b)

    def ausgabe_anzeigen(self, regalplatzoderware):
        dataDict = lib.readUuid(regalplatzoderware)
        if any(regalplatzoderware in sublist for sublist in lib.storageData.values()):
            self.auslagern_button.placeRelative(centerY=True, stickRight=True, changeY=600 * Constants.resolution,
                                                changeX=-400 * Constants.resolution,
                                                fixWidth=200 * Constants.resolution,
                                                fixHeight=100 * Constants.resolution)
        self.protocollButton.placeRelative(stickDown=True, fixWidth=200 * Constants.resolution,
                                           fixHeight=100 * Constants.resolution, changeX=375 * Constants.resolution,
                                           changeY=-900 * Constants.resolution)
        self.protocoll.clear()
        self.writeProtocol()
        self.ausgabetext.clear()
        uuid = self.getUuid()
        waferstueckzahlcounter = 0
        wafercounter = 0
        if lib.readUuid(uuid)["wafer"] != []:
            for i in lib.readUuid(uuid)["wafer"]:

                if i["Menge"] != "Unbekannt":

                    waferstueckzahlcounter = waferstueckzahlcounter + (
                        int(i["Menge"]))
                wafercounter = wafercounter + 1

        if any(uuid in sublist for sublist in lib.storageData.values()):
            if Constants.admin == True:
                self.lagerzustand = "Im Lager: Ja,  " + "Lagerplatz: " + lib.getAblagePlatz(regalplatzoderware)
            else:
                self.lagerzustand = "Im Lager: Ja"
        else:
            self.lagerzustand = "Im Lager: Nein"

        if dataDict["wafer"] == []:
            self.mengenangabe = "Stückzahl: " + dataDict["stueckzahl"]
            self.waferinfos = ""
        else:
            self.mengenangabe= "Anzahl Wafer: " + str(wafercounter) + "\n" + "Gesamtstückzahl: " + str(waferstueckzahlcounter)
            if dataDict["sperr_vermerk"] == True:
                sperrvermerk="Sperrvermerk : Ja"
            else:
                sperrvermerk="Sperrvermerk : Nein"

            self.waferinfos= "Waferdurchmesser: " +dataDict["durchmesser"]+ "\n" + sperrvermerk+ "\n" + "Reservierung: " + dataDict["sperr_vermerk_nummer"] + "\n" + "Notiz: " + dataDict["vermerk"]
        self.ausgabetext.setText("Typ: " + dataDict["typ"]
                                + "\n" +
                                dataDict["protokoll"][0]
                                + "\n" +
                                "Charge: " + dataDict["charge"]
                                + "\n" +
                                "Verpackung: " + dataDict["verpackung"] + "\n" +self.lagerzustand+ "\n" +self.mengenangabe + "\n" + self.waferinfos)
    def onAdminChange(self):
        uuid = self.getSelectedUuid()
        if uuid is None:
            return
        self.ausgabe_anzeigen(uuid)

    def auslagern(self):

        uuid = self.getUuid()

        if uuid in lib.storageData.values():
            print("print")

        lib.delEntry(uuid)
        lib.writeConfigStorage()
        lib.writeConfigLibary()
        self.update_treeview()

    def clearWhenAdminFalse(self):
        if self.checkbox_lagerplatz.getValue():
            self.ausgabetext.clear()
            self.treeview_suche.clear()
            self.treeview_content.clear()

    def update_treeview(self):
        self.auslagern_button.placeForget()
        self.protocollButton.placeForget()
        self.protocoll.placeForget()
        self.ausgabetext.clear()
        self.treeview_suche.clear()
        self.treeview_content.clear()
        suche = self.entry.getText()
        if Constants.admin == True:
            self.checkbox_lagerplatz_label.place(2150 * Constants.resolution, 300 * Constants.resolution,
                                                 200 * Constants.resolution, 40 * Constants.resolution)
            self.checkbox_lagerplatz.place(2350 * Constants.resolution, 300 * Constants.resolution,
                                           40 * Constants.resolution, 40 * Constants.resolution)
        elif Constants.admin == False:
            self.checkbox_lagerplatz_label.placeForget()
            self.checkbox_lagerplatz.placeForget()
        if self.checkbox_uuid.getValue():
            print("UUID Filter Aktiv")
            for keys in lib.libraryData.keys():
                dict = lib.readUuid(keys)
                if suche in dict["uuid"]:
                    uuid = dict["uuid"]
                    self.treeview_content.append(uuid)

        if self.checkbox_charge.getValue():

            print("Charge Filter Aktiv")
            for keys in lib.libraryData.keys():
                dict = lib.readUuid(keys)
                if suche in dict["charge"]:
                    uuid = dict["uuid"]
                    self.treeview_content.append(uuid)

        if self.checkbox_typ.getValue():
            print("Typ Filter Aktiv")
            for keys in lib.libraryData.keys():
                dict = lib.readUuid(keys)
                if suche in dict["typ"]:
                    uuid = dict["uuid"]
                    self.treeview_content.append(uuid)

        if self.checkbox_lagerplatz.getValue():
            print("Lagerplatz Filter Aktiv")

            if suche in lib.storageData.keys():
                dictStorage = lib.readLagerplatz(suche)
                for i in dictStorage:
                    dict = lib.readUuid(i)
                    uuid = dict["uuid"]
                    self.treeview_content.append(uuid)
        self.protocollButtonState = 0

        for value in self.treeview_content:
            if any(value in sublist for sublist in lib.storageData.values()):
                lagerStatus = "Ja"
            else:
                lagerStatus = "Nein"
            a = lib.readUuid(value)
            if a["sperr_vermerk"]:
                sv = "X"
            else:
                sv = ""
            self.treeview_suche.addEntry(a["typ"], a["charge"],lagerStatus, sv)

    def onShow(self, **kwargs):
        self.placeRelative()
        self.entry.setFocus()
        self.entry.clear()
        self.checkbox_typ.clearAll()
        self.checkbox_typ.setOn()
        self.ausgabetext.clear()
        self.protocoll.placeForget()
        self.protocollButtonState = 0
        self.update_treeview()

    def onHide(self):
        self.placeForget()

    def get_on_search(self):
        self.treeview_suche.clear()
        self.treeview_content.clear()

        self.update_treeview()

    def druckerButtonForget(self):
        self.printUuidSticker.placeForget()
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
class Auslagern_page(tk.MenuPage):
    def __init__(self, master):
        super().__init__(master, sg)

        self.button_zurueck_auslagern = tk.Button(self, group=sg)
        self.button_zurueck_auslagern.setText("Zurück")
        self.button_zurueck_auslagern.setFont(30)
        self.button_zurueck_auslagern.placeRelative(centerX=True, centerY=True, changeY=-500 * Constants.resolution,
                                                    changeX=-800 * Constants.resolution,
                                                    fixWidth=400 * Constants.resolution,
                                                    fixHeight=200 * Constants.resolution)
        self.button_zurueck_auslagern.attachToolTip("Zurück", group=sg)
        self.button_zurueck_auslagern.setCommand(self.openLastMenuPage)

        self.auslagern_entry = tk.Entry(self, group=sg)
        self.auslagern_entry.placeRelative(centerX=True, centerY=True, changeY=-500 * Constants.resolution,
                                           changeX=100 * Constants.resolution, fixWidth=1000 * Constants.resolution,
                                           fixHeight=100 * Constants.resolution)
        self.auslagern_entry.setFont(40)
        self.auslagern_entry.attachToolTip("Erwarte QR-CODE")
        self.auslagern_entry.bind(self.get_on_search, tk.EventType.RETURN)

        self.label_admin = tk.Label(self, text="°", group=sgnew)
        self.label_admin.placeRelative(fixWidth=100, fixHeight=120, stickDown=True, stickRight=True,
                                       changeY=+45)
        self.label_admin.setFont(100)
        self.label_admin.bind(enter_login, tk.EventType.LEFT_CLICK)

    def onShow(self, **kwargs):
        self.placeRelative()
    def onHide(self):
        self.placeForget()

    def get_on_search(self):
        eintrag = self.auslagern_entry.getValue()
        # print(eintrag)
        self.auslagern_entry.clear()
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------




def main():
    global mainpage, search_page,choice_page,auslagern_page,alte_ware_einlagern_page,neue_ware_einlagern_page
    master = tk.Tk(group=sg)
    LOAD_STYLE()
    Constants.master = master
    sg.executeCommands()
    master.bind(afk_reset, tk.EventType.LEFT_CLICK)
    master.bind(afk_reset, tk.EventType.RETURN)

    master.setFullscreen(True)
    master.setTitle("Eingabe Fenster")
    master.setWindowSize(x=1000, y=1000, minsize=True)
    master.setPositionOnScreen(x=0, y=0)

    alte_ware_einlagern_page = Alte_ware_einlagern_page(master)
    neue_ware_einlagern_page = Neue_ware_einlagern_page(master)

    auslagern_page = Auslagern_page(master)
    choice_page = Einlagern_page(master)
    search_page = Search_page(master)
    mainpage = Mainpage(master)

    mainpage.openMenuPage()

    state_Switch()
    master.mainloop()
