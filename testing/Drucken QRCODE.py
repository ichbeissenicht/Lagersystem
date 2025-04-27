from win32com.client import Dispatch
import pathlib


barcode_val = "0"
barcode_path = r"C:\Users\Josi\Desktop\Address.label" #Wenn adress.label im selben ordner liegt wie die ausführende .py kann auch mit ./adress.label ausgeführt werden
my_printer = 'DYMO LabelWriter 450 DUO Label'

printer_com = Dispatch("Dymo.DymoAddIn")
printer_com.SelectPrinter(my_printer)
printer_com.Open(barcode_path)

printer_label = Dispatch("Dymo.DymoLabels")
printer_label.SetField("Barcode",barcode_val)

printer_com.StartPrintJob()
printer_com.Print(1,False)
printer_com.EndPrintJob()