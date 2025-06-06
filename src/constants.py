from tkinter import ttk
import tksimple as tk




class Resolution:
    FourK = 1.5
    WQHD = 1
    FullHD = 0.75
class Constants:

    adminLoginUpdateHook = []                                                                                           #Alle Methoden die in der Liste enthalten sind werden beim Login/Logout einmal ausgefuehrt
    admin = False
    master = None
    checkbox_wafer = False
    afk_timer = 300
    afk_window_timer = 30
    resolution = Resolution.FullHD
    whitemode = False


class Color:
    COLOR_BLUE = tk.Color.rgb(0,120,215)
    COLOR_WHITE = tk.Color.rgb(228, 227, 223)
    COLOR_DARK = tk.Color.rgb(50, 50, 50)
    COLOR_GRAY = tk.Color.rgb(190, 190, 190)
    COLOR_DARKGRAY = tk.Color.rgb(60,60,60)
    primarycolor = None
    secondarycolor = None
    contrastcolor = None
    STYLE = None



def LOAD_STYLE():
    if Constants.whitemode:
        Color.primarycolor = Color.COLOR_WHITE
        Color.secondarycolor = Color.COLOR_DARK
        Color.contrastcolor = Color.COLOR_GRAY
    else:
        Color.primarycolor = Color.COLOR_DARK
        Color.secondarycolor = Color.COLOR_WHITE
        Color.contrastcolor = Color.COLOR_DARKGRAY
    if Color.STYLE is None:
        Color.STYLE = ttk.Style()
        Color.STYLE.theme_create("custom_theme", parent="alt", settings = {})

    Color.STYLE.theme_settings("custom_theme", settings ={
        "TNotebook": {
            "configure": {
                "tabmargins": [2, 5, 2, 0],
                "background": Color.primarycolor,
            }
        },
        "TNotebook.Tab": {
            "configure": {
                "padding": [5, 1],
                "background": Color.primarycolor,
                "foreground": Color.secondarycolor,
            }
        },
        "Treeview": {
            "configure": {
                "font": ("Arial", 30),
                "rowheight": 50,
                "background": Color.primarycolor,
                "foreground": Color.secondarycolor,
                "fieldbackground": Color.primarycolor
            },
            "map": {
                "background": [('selected', Color.COLOR_GRAY)]
            }
        },
        "Treeview.Heading": {
            "configure": {
                "font": ("Arial",30),
                "background": Color.primarycolor,
                "foreground": Color.secondarycolor
            }
        },
        "Treeview.Item": {
            "configure": {
                "indicatorsize": 30

            }
        },
        "TProgressbar": {
            "configure": {
                "background": "green",
                "troughcolor": Color.primarycolor,
            }
        },
        "TCombobox": {
            "configure": {
                "background": Color.primarycolor,
                "foreground": Color.secondarycolor,
                "fieldbackground": Color.primarycolor,
                "selectbackground": Color.COLOR_BLUE,
                "selectcolor": Color.primarycolor,
            }
        },
        "TCheckbutton": {
            "configure": {
                "font": 30,

            }
        },
        "Vertical.TScrollbar": {
            "configure": {
                "background": Color.primarycolor,
                "foreground": Color.secondarycolor,
                "fieldbackground": Color.primarycolor,
                "selectbackground": Color.primarycolor,
                "selectcolor": Color.primarycolor,
                "arrowsize": 17
            }
        }
    }
                       )
    Color.STYLE.theme_use("custom_theme")


    sg.clearCommands()
    sg.addCommand("setBg", Color.primarycolor, ignoreErrors=True) #w
    sg.addCommand("setFg", Color.secondarycolor, ignoreErrors=True)
    sg.addCommand("setActiveBg", Color.contrastcolor, ignoreErrors=True)
    sg.addCommand("setSlotBgDefault", Color.primarycolor, ignoreErrors=True) #w
    sg.addCommand("setSelectBackGroundColor", tk.Color.rgb(0, 102,204), ignoreErrors=True)
    sg.addCommand("setSelectColor", Color.contrastcolor, ignoreErrors=True)
    sg.addCommand("setSlotBgAll", Color.contrastcolor, ignoreErrors=True)
    sg.executeCommands()
    contrastcolorsg.clearCommands()
    contrastcolorsg.addCommand("setBg", Color.contrastcolor, ignoreErrors=True)
    contrastcolorsg.addCommand("setFg", Color.secondarycolor, ignoreErrors=True)
    contrastcolorsg.addCommand("setActiveBg", Color.contrastcolor, ignoreErrors=True)
    contrastcolorsg.addCommand("setSlotBgDefault", Color.contrastcolor, ignoreErrors=True)  # w
    contrastcolorsg.addCommand("setSelectBackGroundColor", Color.contrastcolor, ignoreErrors=True)
    contrastcolorsg.addCommand("setSelectColor", Color.contrastcolor, ignoreErrors=True)
    contrastcolorsg.addCommand("setSlotBgAll", Color.contrastcolor, ignoreErrors=True)
    contrastcolorsg.executeCommands()
    sgnew.clearCommands()
    sgnew.addCommand("setBg", Color.primarycolor, ignoreErrors=True)
    sgnew.executeCommands()
sg = tk.WidgetGroup()



sgnew = tk.WidgetGroup()



contrastcolorsg = tk.WidgetGroup()



