import constants
import tksimple as tk
import lagerLib as lib


import suchfunktion
from afktimer import afk_reset, afk_clear, afk_logout, enter_login, state_Switch
from constants import sg,sgnew, Constants, LOAD_STYLE
from lagerLib import storageData, libraryData
#from lagerTest import dataDict
from widgets import CustomCheckbutton, Counterwidget, Ask_for_wafer_name_and_amount, CheckButtonGroup, PickWaferToOutSource, PickAmountToOutSource

lib.productStorageConfigPath = "storage.json"
lib.productLibraryConfigPath = "library.json"
lib.readConfigStorage()
lib.readConfigLibrary()



del lib.libraryData["sJG7cyU2FiKiXZdnKgamDaOHo90eoF3M"]
lib.writeConfigLibary()