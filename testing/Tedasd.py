from win32com.client import Dispatch

labelCom = Dispatch('Dymo.IDymoAddin6')
labelText = Dispatch('Dymo.IDymoLabels3')

labelCom.SelectPrinter('DYMO LabelWriter 450')

labelText.SetField('TEXT1', "test123")
labelText.SetField('TEXT2', "test456")

labelCom.StartPrintJob()
labelCom.Print(1, False)
labelCom.EndPrintJob()


