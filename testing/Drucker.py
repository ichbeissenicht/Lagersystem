from win32com.client import Dispatch

labelCom = Dispatch('Dymo.DymoAddIn')
labelText = Dispatch('Dymo.DymoLabels')

selectPrinter = 'DYMO LabelWriter 450 DUO Label'
print(labelCom.SelectPrinter(selectPrinter))

labelText.SetField('TEXT1', "test123")
labelText.SetField('TEXT2', "test456")

labelCom.StartPrintJob()
labelCom.Print(1, False)
labelCom.EndPrintJob()