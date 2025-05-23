from constants import Constants, sg, sgnew
import tksimple as tk
from threading import Thread
from time import sleep,time

current_afk_window_timer = 0
timerLabel = None
timer_in_seconds = Constants.afk_timer
afk_task = None
root = None
def state_Switch():
    if Constants.admin == True:
        sgnew.setFg("green")
    else:
        sgnew.setFg("red")


def afk_logout():
    afk_popup()
    state_Switch()




def afk_clear():
    global afk_task
    if afk_task is not None:
        afk_task.cancel()
        afk_task = None





def afk_reset():
    global afk_task
    if Constants.admin:
        afk_clear()
        afk_task = Constants.master.runTaskAfter(afk_logout, Constants.afk_timer)
        afk_task.start()
        changeAdminMode(True)
        state_Switch()





def updateTimerThread():
    global current_afk_window_timer
    timer = time()
    while True:
        sleep(0.1)                                                                                                  #immer einbauen
        if time()-timer >=1:
            timer=time()
            current_afk_window_timer -=1
            if current_afk_window_timer < 1:
                return

            timerLabel.setText(f"Abmeldung in: {current_afk_window_timer} Sekunden")


def angemeldet_bleiben():
    global current_afk_window_timer
    current_afk_window_timer = 0
    afk_reset()
    root.destroy()


def abmelden():
    global current_afk_window_timer
    current_afk_window_timer = 0
    changeAdminMode(False)
    state_Switch()
    root.destroy()



def afk_popup():
    global timerLabel, current_afk_window_timer, root

    def timer_abmeldung():

        logout_timer = root.runTaskAfter(abmelden, Constants.afk_window_timer)
        logout_timer.start()
        return

    root = tk.Dialog(Constants.master, group=sg)
    root.setWindowSize(600, 150)
    root.setResizeable(False)
    root.centerWindowOnScreen(True)
    root.setTitle("Automatische Abmeldung")
    label_anmelden = tk.Label(root, text="Angemeldet Bleiben", group=sg)
    label_anmelden.bind(angemeldet_bleiben, tk.EventType.LEFT_CLICK)
    label_anmelden.setFont(20)
    label_anmelden.place(20, 20, 300, 100)
    label_abmelden = tk.Label(root, text="Abmelden", group=sg)
    label_abmelden.bind(abmelden, tk.EventType.LEFT_CLICK)
    label_abmelden.setFont(20)
    label_abmelden.place(380, 20, 150, 100)

    current_afk_window_timer = Constants.afk_window_timer
    timerLabel = tk.Label(root,text=f"Abmeldung in: {Constants.afk_window_timer} Sekunden",group=sg)
    timerLabel.setFont(15)

    timerLabel.placeRelative(centerY=False,centerX=True,fixWidth=400,fixHeight=20,changeY=10)
    root.setCloseable(False)
    timer_abmeldung()
    root.show()
    Thread(target=updateTimerThread).start()

def login():
    global afk_task
    changeAdminMode(not Constants.admin)
    afk_clear()
    if Constants.admin:
        afk_task = Constants.master.runTaskAfter(afk_logout, Constants.afk_timer)
        afk_task.start()

    state_Switch()



def wrong_password():
    root1 = tk.Dialog(Constants.master, group=sg)
    root1.setWindowSize(400, 150)
    root1.setResizeable(False)
    root1.centerWindowOnScreen(True)
    root1.setTitle("Falsches passwort")
    label_anmelden = tk.Label(root1, text="Falsches Passwort!", group=sg)
    label_anmelden.setFont(20)
    label_anmelden.place(50, 20, 300, 100)
    root1.show()
def changeAdminMode(_admin):
    if Constants.admin == _admin:
        return
    Constants.admin = _admin
    for i in Constants.adminLoginUpdateHook:
        i()







def enter_login():
    if Constants.admin:
        login()
        return
    out = tk.SimpleDialog.askString(Constants.master, "Bitte Einscannen!", "Login", hideWith="*")
    if out is None:
        return
    elif out != None and out != "1379":
        wrong_password()

    elif out == "1379":  # Passwort
        login()




