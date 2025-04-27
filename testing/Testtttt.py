import tksimple as tk

master =tk.Tk()

frame = tk.Frame(master)

frame.place(0,0,100,200)
#frame.setBg(tk.Color.RED)
frame.setStyle(tk.Style.SUNKEN)
frame.setBorderWidth(10)
master.mainloop()