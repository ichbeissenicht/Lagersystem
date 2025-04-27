# from pymupdf.mupdf import fz_new_image_from_compressed_buffer
# from pyrect import CENTER, CENTERX
from tkinter.constants import SUNKEN

import constants
import lagerLib as lib
import tksimple as tk
from tksimple import FontType
from constants import Color, sg


class CheckButtonGroup:
    def __init__(self, isMultipleTicks):
        self.isMultipleTicks = isMultipleTicks
        self.liste = []


class CustomCheckbutton(tk.Frame):
    def __init__(self, master, group, checkButton):
        super().__init__(master, group)

        self.checkButton = checkButton
        self.checkButton.liste.append(self)
        self.func = None
        self.check = tk.OnOffButton(self, group=group, colorsActive=False, reliefActive=False)
        self.check.setOnText("X")
        self.check.setOffText("")
        self.check.setStyle(tk.Style.SUNKEN)
        self.labl = tk.Label(self, group)

    def placeRelative(self, fixX: int = None, fixY: int = None, fixWidth: int = None, fixHeight: int = None, xOffset=0,
                      yOffset=0, xOffsetLeft=0, xOffsetRight=0, yOffsetUp=0, yOffsetDown=0, stickRight=False,
                      stickDown=False, centerY=False, centerX=False, changeX=0, changeY=0, changeWidth=0,
                      changeHeight=0, nextTo=None, updateOnResize=True):
        raise NotImplementedError()

    def setText(self, text):
        self.labl.setText(text)

    def place(self, x=None, y=None, width=None, height=None, anchor: tk.Anchor = tk.Anchor.UP_LEFT):
        super().place(x, y, width, height, anchor)
        self.check.place(width - height, 0, height, height)
        self.labl.place(0, 0, width - height, height)

    def _run(self):
        if self.func is not None:
            if not self.checkButton.isMultipleTicks:
                self.clearAll()
                self.check.setOn()

            self.func()

    def clearAll(self):
        for i in self.checkButton.liste:
            i.check.setOff()

    def setCommand(self, c):
        self.check.setCommand(self._run)

        self.func = c

    def getValue(self):
        return self.check.getValue()

    def setOn(self):
        self.check.setOn()

    def setFont(self, size: int = 10, art=FontType.ARIAL, underline=False, bold=False, slant=False, overstrike=False):
        self.labl.setFont(size)
        self.check.setFont(size)


class Counterwidget(tk.Frame):
    def __init__(self, master, sg, initial_value=0):
        super().__init__(master, sg)
        self.initial_value = initial_value
        self.counter_anzeige = tk.Label(self, group=sg)
        self.update_value()

        self.counter_minus = tk.Button(self, group=sg)

        self.counter_minus.setText("-")
        self.counter_minus.setFont(30)
        self.counter_minus.setCommand(self.change_value, args=["-"])

        self.counter_plus = tk.Button(self, group=sg)

        self.counter_plus.setText("+")
        self.counter_plus.setFont(30)
        self.counter_plus.setCommand(self.change_value, args=["+"])
        # self.counter_plus.setCommand(self.entry_windows)

    def update_value(self):
        self.counter_anzeige.setText(self.initial_value)
        self.counter_anzeige.setFont(30)

    def change_value(self, e: tk.Event):
        value = e.getArgs(0)
        if value == "+":
            self.initial_value += 1
        elif value == "-" and self.initial_value > 0:
            self.initial_value -= 1

        self.update_value()

    def getValueWafer(self):
        return self.initial_value

    def place(self, x=None, y=None, width=None, height=None, anchor: tk.Anchor = tk.Anchor.UP_LEFT):
        super().place(x, y, width, height, anchor)
        self.counter_plus.place(width - height, 0, height, height)
        self.counter_minus.place(0, 0, height, height)
        self.counter_anzeige.place(height, 0, width - height * 2, height)


class Ask_for_wafer_name_and_amount(tk.Dialog):
    def __init__(self, master, sg):
        super().__init__(master, sg)

        self.setWindowSize(550, 400)
        self.setCloseable(False)
        self.setResizeable(False)
        self.centerWindowOnScreen(True)
        self.setTitle("Wafer Hinzufuegen")

        self.label_error = tk.Label(self, group=sg)
        self.label_error.setFont(20)
        self.label_error.placeRelative(stickDown=True, changeY=-70, fixHeight=30, fixWidth=540, centerX=True)

        self.label_wafer_name = tk.Label(self, text="Wafer Nummer eingeben:", group=sg)
        self.label_wafer_name.setFont(30)
        self.label_wafer_name.placeRelative(fixY=0, fixHeight=50)

        self.entry_wafer_name = tk.Entry(self, group=sg)
        self.entry_wafer_name.setFont(30)
        self.entry_wafer_name.placeRelative(fixY=50, fixHeight=50, fixWidth=450, centerX=True)

        self.label_wafer_stueckzahl = tk.Label(self, text="Stückzahl eingeben:", group=sg)
        self.label_wafer_stueckzahl.setFont(30)
        self.label_wafer_stueckzahl.placeRelative(fixY=125, fixHeight=50, fixWidth=450, centerX=True)

        self.entry_wafer_stueckzahl = tk.Entry(self, group=sg)
        self.entry_wafer_stueckzahl.setFont(30)
        self.entry_wafer_stueckzahl.placeRelative(fixY=175, fixHeight=50, fixWidth=450, centerX=True)

        self.button_wafer_save = tk.Button(self, group=sg)
        self.button_wafer_save.setText("Speichern")
        self.button_wafer_save.setFont(20)
        self.button_wafer_save.placeRelative(stickDown=True, changeY=-2, changeX=2, fixHeight=50, fixWidth=200)

        self.wafer_stueckzahl_unbekannt_label = tk.Label(self, group=sg)
        self.wafer_stueckzahl_unbekannt_label.setText("Menge unbekannt:")
        self.wafer_stueckzahl_unbekannt_label.setFont(20)
        self.wafer_stueckzahl_unbekannt_label.placeRelative(fixX=120, fixY=253, fixWidth=250, fixHeight=40)

        self.wafer_stueckzahl_unbekannt_checkbox = CustomCheckbutton(self, group=sg, checkButton=CheckButtonGroup(True))
        self.wafer_stueckzahl_unbekannt_checkbox.place(height=30 * constants.Constants.resolution,
                                                       width=30 * constants.Constants.resolution,
                                                       y=350 * constants.Constants.resolution,
                                                       x=500 * constants.Constants.resolution)
        self.wafer_stueckzahl_unbekannt_checkbox.setFont(20)

        def wafer_stueckzahl_unbekannt_checkbox_abfrage():
            is_checkbox_stueckzahl_unbekannt_ticked = self.wafer_stueckzahl_unbekannt_checkbox.getValue()
            if is_checkbox_stueckzahl_unbekannt_ticked:
                self.entry_wafer_stueckzahl.placeForget()
                self.entry_wafer_stueckzahl.clear()
                self.label_wafer_stueckzahl.placeForget()
            else:
                self.entry_wafer_stueckzahl.placeRelative(fixY=175, fixHeight=50, fixWidth=450, centerX=True)
                self.label_wafer_stueckzahl.placeRelative(fixY=125, fixHeight=50, fixWidth=450, centerX=True)

        self.wafer_stueckzahl_unbekannt_checkbox.setCommand(wafer_stueckzahl_unbekannt_checkbox_abfrage)

        self.button_wafer_cancel = tk.Button(self, group=sg)
        self.button_wafer_cancel.setText("Abbrechen")
        self.button_wafer_cancel.setFont(20)
        self.button_wafer_cancel.placeRelative(stickDown=True, stickRight=True, changeY=-2, changeX=-2, fixHeight=50,
                                               fixWidth=200)
        self.button_wafer_cancel.setCommand(self.cancel)

        self.hide()  # TODO wenn ich bibliothek aktualisiere, kann die zeile weg!

    def onSave(self, c):
        self.button_wafer_save.setCommand(c)

    def cancel(self):
        self.hide()

    def printerror(self, param):
        self.label_error.setText(param)
        self.label_error.setBg("red")

    def open(self):
        self.label_error.setText("")
        self.label_error.setBg(Color.primarycolor)
        self.entry_wafer_name.clear()
        self.entry_wafer_stueckzahl.clear()
        self.show()
        self.setFocus()
        self.entry_wafer_name.setFocus()


class PickWaferToOutSource(tk.Dialog):
    def __init__(self, master, sg):
        super().__init__(master, sg)
        self.master = master
        self.setWindowSize(1000, 700)
        self.setCloseable(True)
        self.setResizeable(False)
        self.centerWindowOnScreen(True)
        self.setTitle("Wafer auslagern")

        self.button_wafer_cancel = tk.Button(self, group=sg)
        self.button_wafer_cancel.setText("Abbrechen")
        self.button_wafer_cancel.setFont(20)
        self.button_wafer_cancel.placeRelative(stickDown=True, stickRight=True, changeY=-2, changeX=-2, fixHeight=50,
                                               fixWidth=200)
        self.button_wafer_cancel.setCommand(self.cancel)

        self.wafer_treeview_auswahl = SingleSelectTreeview(self, group=sg)
        self.wafer_treeview_auswahl.setMultipleSelect()
        self.wafer_treeview_auswahl.placeRelative(centerX=True, centerY=True,
                                                  fixWidth=650 * constants.Constants.resolution,
                                                  fixHeight=400 * constants.Constants.resolution)
        self.scrollbar = tk.ScrollBar(self)
        self.wafer_treeview_auswahl.attachVerticalScrollBar(self.scrollbar)
        self.wafer_treeview_auswahl.setTableHeaders("Nummer", "Stückzahl")

        self.button_wafer_auslagern = tk.Button(self, group=sg)
        self.button_wafer_auslagern.setText("Auswählen")
        self.button_wafer_auslagern.setFont(20)
        self.button_wafer_auslagern.placeRelative(stickDown=True, stickRight=False, changeY=-2, changeX=-2,
                                                  fixHeight=50,
                                                  fixWidth=200)

        self.button_wafer_zurueck = tk.Button(self, group=sg)
        self.button_wafer_zurueck.setText("Zurück")
        self.button_wafer_zurueck.setFont(20)
        self.button_wafer_zurueck.setCommand(self.zurueck)

        self.wafer_auswahl_label = tk.Label(self, group=sg)
        self.wafer_auswahl_label.setFont(30)
        self.wafer_auswahl_label.setText("Bitte wählen Sie die Auszulagernden Wafer aus!")
        self.wafer_auswahl_label.placeRelative(centerY=True, centerX=True, changeY=-275, fixWidth=1000, fixHeight=100)

    def zurueck(self):
        self.button_wafer_zurueck.placeForget()
        self.wafer_treeview_auswahl.placeRelative(centerX=True, centerY=True,
                                                  fixWidth=650 * constants.Constants.resolution,
                                                  fixHeight=400 * constants.Constants.resolution)
        self.button_wafer_auslagern.placeRelative(stickDown=True, stickRight=False, changeY=-2, changeX=-2,
                                                  fixHeight=50,
                                                  fixWidth=200)

        # self.wafer_stueckzahl_frame.placeForget()

    def cancel(self):
        self.wafer_treeview_auswahl.clear()

        self.hide()

    def open(self):
        # print(self._data)
        self.show()
        self.setFocus()


class PickAmountToOutSource(tk.Dialog):
    def __init__(self, master, sg):
        super().__init__(master, sg)
        self.master = master
        self.setWindowSize(1000, 700)
        self.setCloseable(True)
        self.setResizeable(False)
        self.centerWindowOnScreen(True)
        self.setTitle("Stückzahl auslagern")

        self.button_wafer_cancel = tk.Button(self, group=sg)
        self.button_wafer_cancel.setText("Abbrechen")
        self.button_wafer_cancel.setFont(20)
        self.button_wafer_cancel.placeRelative(stickDown=True, stickRight=True, changeY=-2, changeX=-2, fixHeight=50,
                                               fixWidth=200)

        self.button_wafer_auslagern = tk.Button(self, group=sg)
        self.button_wafer_auslagern.setText("Auslagern")
        self.button_wafer_auslagern.setFont(20)
        self.button_wafer_auslagern.placeRelative(stickDown=True, stickRight=False, changeY=-2, changeX=-2,
                                                  fixHeight=50,
                                                  fixWidth=200)

        self.label_verpackung = tk.Label(self, group=sg)
        self.label_verpackung.setFont(20)
        self.label_verpackung.setText("Verpackung: ")
        self.dropdown_frame = tk.LabelFrame(self, group=sg)

        self.dropdown_verpackung = tk.DropdownMenu(self.dropdown_frame, group=sg,
                                                   optionList=["Singleframeshipper","Frameshipper", "Tape & Reel", "8 Zoll Box","6 Zoll Box", "Andere"])
        self.dropdown_verpackung.attachToolTip("Nur relevant wenn selbe Ware nicht bereits eingelagert ist")
        self.dropdown_verpackung.setFont(20)
        self.label_verpackung.placeRelative(centerX=True, centerY=True, changeY=-100, fixWidth=250, fixHeight=50,
                                            changeX=-120)
        self.dropdown_frame.placeRelative(centerX=True, centerY=True, changeY=-100, fixWidth=250, fixHeight=52,
                                          changeX=100)
        self.dropdown_verpackung.placeRelative(centerX=True, centerY=True, fixWidth=250, fixHeight=50, changeX=-1,
                                               changeY=-2)

        self.label_info = tk.Label(self, group=sg)
        self.label_info.setFont(30)
        self.label_info.setText("Auslagern")
        self.label_info.placeRelative(centerY=True, centerX=True, changeY=-200, fixWidth=400, fixHeight=100)

        self.stueckzahl_label = tk.Label(self, group=sg)
        self.stueckzahl_label.setFont(20)
        self.stueckzahl_label.setText("Auslagern")
        self.stueckzahl_label.placeRelative(centerX=True, centerY=True, changeX=-140, fixWidth=150, fixHeight=50)

        self.stueckzahl_alt_von = tk.Label(self, group=sg)
        self.stueckzahl_alt_von.setFont(20)
        self.stueckzahl_alt_von.placeRelative(centerX=True, centerY=True, changeX=130, fixWidth=200, fixHeight=50)
        self.stueckzahl_alt_von.setTextOrientation(tk.Anchor.LEFT)

        self.stueckzahl_alt = tk.Entry(self, group=sg)
        self.stueckzahl_alt.setFont(20)
        self.stueckzahl_alt.placeRelative(centerX=True, centerY=True, changeX=-25, fixWidth=100, fixHeight=50)

        self.vermerk_entry = tk.Entry(self, group=sg)
        self.vermerk_entry.setFont(20)
        self.vermerk_entry.placeRelative(centerX=True, centerY=True, changeX=70, fixWidth=300, fixHeight=50,
                                         changeY=100)

        self.vermerk_label = tk.Label(self, group=sg)
        self.vermerk_label.setFont(20)
        self.vermerk_label.setText("Notiz: ")
        self.vermerk_label.placeRelative(centerX=True, centerY=True, changeX=-140, fixWidth=120, fixHeight=50,
                                         changeY=100)

        self.button_wafer_cancel.setCommand(self.cancel)

    def cancel(self):
        self.hide()

    def open(self):
        self.show()
        self.setFocus()


class AmountToOutSource(tk.Dialog):
    def __init__(self, master, sg, lastDialog, selectedEntries):
        super().__init__(master, sg)
        self.lastDialog = lastDialog

        self.setWindowSize(1000, 700)
        self.setCloseable(True)
        self.setResizeable(False)
        self.centerWindowOnScreen(True)
        self.setTitle("Stückzahl auswählen")

        self.button_wafer_cancel = tk.Button(self, group=sg)
        self.button_wafer_cancel.setText("Zurück")
        self.button_wafer_cancel.setFont(20)
        self.button_wafer_cancel.placeRelative(stickDown=True, stickRight=True, changeY=-2, changeX=-2, fixHeight=50,
                                               fixWidth=200)
        self.button_wafer_cancel.setCommand(self.back)

        self.button_wafer_auslagern = tk.Button(self, group=sg)
        self.button_wafer_auslagern.setText("Auslagern")
        self.button_wafer_auslagern.setFont(20)
        self.button_wafer_auslagern.placeRelative(stickDown=True, stickRight=False, changeY=-2, changeX=-2,
                                                  fixHeight=50, fixWidth=200)
        self.headline = tk.Label(self,group=sg)
        self.headline.setText(" Nummer:             Stückzahl:   ")
        self.headline.setFont(30)
        self.headline.placeRelative(centerX=True, fixHeight=50, fixWidth=600)



        self.vermerk_entry = tk.Entry(self,group = sg)
        self.vermerk_entry.setFont(20)
        self.vermerk_entry.placeRelative(centerX=True,stickDown=True,changeY=-100,fixHeight=50,fixWidth=300, changeX=75)

        self.vermerk_label = tk.Label(self,group=sg)
        self.vermerk_label.setFont(20)
        self.vermerk_label.setText("Notiz:")
        self.vermerk_label.placeRelative(centerX=True,stickDown=True,changeY=-100,fixHeight=50,fixWidth=130, changeX=-150)

        self.entries = []
        self.labels = []





        for i in range(len(selectedEntries)):
            entry = tk.Entry(self, sg)
            label = tk.Label(self, sg)
            label_unbekannt = tk.Label(self, sg)
            if selectedEntries[i]["Stückzahl"] == "Unbekannt":

                entry.setStyle(tk.Style.FLAT)
                label.setText(str(selectedEntries[i]["Nummer"]))
                entry.setText("Unbekannt")
                label_unbekannt.setText("Unbekannt")
                label_unbekannt.placeRelative(fixHeight=50, fixWidth=250, fixY=60 + i * 60, fixX=550)
                label.placeRelative(fixHeight=50, fixWidth=250, fixY=60 + i * 60, fixX=200)
            else:
                label.setText(str(selectedEntries[i]["Nummer"]))
                entry.setText(selectedEntries[i]["Stückzahl"])
                entry.placeRelative(fixHeight=50, fixWidth=250, fixY=60 + i * 60, fixX=550)
                label.placeRelative(fixHeight=50, fixWidth=250, fixY=60 + i * 60, fixX=200)

            label_unbekannt.setFont(30)
            entry.setFont(30)
            label.setFont(30)
            self.labels.append(label)
            self.entries.append(entry)  # In der Liste speichern

    # Funktion zum Auslesen der Einträge





    # Button zum Auslesen der Einträge


    def back(self):
        self.destroy()
        # self.lastDialog.open()

    def auslagern(self):
        pass

    def cancel(self):
        self.destroy()

    def open(self):
        self.show()
        self.setFocus()


class SingleSelectTreeview(tk.TreeView):
    def __init__(self, _master, group=None):
        super().__init__(_master, group)
        self._selectedIndices = []
        self.setMultipleSelect()
        self.onSingleSelectEvent(self._onSelectEvent, useIndex=True)

    def _updateSelection(self):
        self.clearSelection()
        for ind in self._selectedIndices: self.setItemSelectedByIndex(ind, False)

    def _onSelectEvent(self, e: tk.Event):
        index = self.getSelectedIndex()
        if index is None: return
        if len(index) == 1:
            if index[0] in self._selectedIndices:
                self._selectedIndices.remove(index[0])
            else:
                self._selectedIndices.append(index[0])
            self._updateSelection()
