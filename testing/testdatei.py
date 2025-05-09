import tkinter as tk
from tkinter import messagebox


class FrageWidget:
    def __init__(self, root):
        self.root = root
        self.root.title("Fragen-Widget")

        # Liste der Fragen
        self.fragen = [
            "Was ist die Hauptstadt von Deutschland?",
            "Wie viele Kontinente gibt es?",
            "Was ist 2 + 2?"
        ]
        self.index = 0  # Der Index der aktuellen Frage

        # Label für die Frage
        self.frage_label = tk.Label(root, text=self.fragen[self.index], font=('Arial', 14))
        self.frage_label.pack(pady=20)

        # Eingabefeld für die Antwort
        self.antwort_entry = tk.Entry(root, font=('Arial', 14))
        self.antwort_entry.pack(pady=10)

        # Button zum Absenden der Antwort
        self.submit_button = tk.Button(root, text="Antworten", font=('Arial', 14), command=self.naechste_frage)
        self.submit_button.pack(pady=20)

    def naechste_frage(self):
        # Hier könnten Sie Logik hinzufügen, um die Antwort zu überprüfen
        antwort = self.antwort_entry.get()

        # Wenn es keine weiteren Fragen gibt
        if self.index < len(self.fragen) - 1:
            self.index += 1
            self.frage_label.config(text=self.fragen[self.index])
            self.antwort_entry.delete(0, tk.END)  # Eingabefeld leeren
        else:
            messagebox.showinfo("Ende", "Es gibt keine weiteren Fragen!")
            self.root.quit()  # Beende das Programm


# Tkinter-Setup
root = tk.Tk()
widget = FrageWidget(root)
root.mainloop()