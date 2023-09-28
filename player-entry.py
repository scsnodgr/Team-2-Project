import tkinter as tk
from tkinter import *

class PlayerEntryScreen(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        #self.attributes("-fullscreen", True)
        #self.geometry("1800x1000")
        self.configure(bg="black")

        Title = tk.Label(self, text="Player Entry", 
                        fg="white", bg="black", font=("Lexend Bold", 40))
        Title.grid(row=0, column=0, columnspan=2)
        
        team_red_curr_row = 1
        team_blue_curr_row = 1
        team_chosen = tk.StringVar(self)
        team_chosen.set("Red")
        team_red_players = {}

        team_red = TeamTable(self, 16, 2)
        team_blue = TeamTable(self, 16, 2)
        team_red.grid(row=1, column=0, padx=15, pady=15)
        team_blue.grid(row=1, column=1, padx=15, pady=15)

        team_red.set(0,0,"Player ID", font = ("Lexend Bold", 25), color = "red")
        team_red.set(0,1,"Name", font = ("Lexend Bold", 25), color = "red")
        team_blue.set(0,0,"Player ID", font = ("Lexend Bold", 25), color = "blue")
        team_blue.set(0,1,"Name", font = ("Lexend Bold", 25), color = "blue")

        id_label = tk.Label(self, text="Enter Player ID:", 
                            bg="black", fg="white", 
                            font=("Lexend Bold", 25))
        id_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        id_entry = tk.Entry(self, bg="gray", fg="white",
                            font=("Lexend Thin", 22), borderwidth=1)
        id_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        name_label = tk.Label(self, text="Enter Player Name:", 
                            bg="black", fg="white", 
                            font=("Lexend Bold", 25))
        name_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        name_entry = tk.Entry(self, bg="gray", fg="white",
                            font=("Lexend Thin", 22), borderwidth=1)
        name_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        team_label = tk.Label(self, text="Choose Team:", 
                            bg="black", fg="white", 
                            font=("Lexend Bold", 25))
        team_label.grid(row=4, column=0, sticky="e", padx=5, pady=5)
        dropdown = tk.OptionMenu(self, team_chosen, *['Red','Blue'])
        dropdown.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        dropdown.configure(font=("Lexend Thin", 22), bg="black", fg="white")
        team_dropdown = self.nametowidget(dropdown.menuname)
        team_dropdown.configure(font=("Lexend Thin", 30))

        equipment_label = tk.Label(self, text="Enter Equipment ID:", 
                            bg="black", fg="white", 
                            font=("Lexend Bold", 25))
        equipment_label.grid(row=5, column=0, sticky="e", padx=5, pady=5)
        equipment_entry = tk.Entry(self, bg="gray", fg="white",
                            font=("Lexend Thin", 22), borderwidth=1)
        equipment_entry.grid(row=5, column=1, sticky="w", padx=5, pady=5)




class TeamTable(tk.Frame):
    def __init__(self, parent, rows, columns):
        tk.Frame.__init__(self, parent, background="white")
        self._widgets = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                label = tk.Label(self, text=" ", 
                                 borderwidth=0, width=20,
                                 background="black", foreground="red",
                                 font = ("Lexend Thin", 22))
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)


    def set(self, row, column, value, font=("Lexend Thin", 22), color="white"):
        widget = self._widgets[row][column]
        widget.configure(text=value, font=font, fg=color)


if __name__ == "__main__":
    app = PlayerEntryScreen()
    app.mainloop()