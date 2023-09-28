import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image


class SplashScreen(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.attributes('-fullscreen', True)
        self.configure(bg = "black")

        frame = Frame(self, width = 1280, height = 815, bg = "black")
        frame.place(anchor = 'center', relx = 0.5, rely = 0.5)

        self.img = ImageTk.PhotoImage(Image.open("photon.jpg"))
        label = tk.Label(frame, image = self.img, borderwidth = 0)
        label.pack(fill = BOTH, expand = YES)
        #label.pack()
        self.after(3000, lambda:self.destroy())

class PlayerEntryScreen(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.configure(bg="black")
        
        self.player_exists = False

        def check_id():
            player_id = id_entry.get()
            ########################################
            ########################################
            ## check if id exists in database     ##
            ## fill name_from_db with result      ##
            ## if exists                          ##
            ########################################
            ########################################
            name_from_db = "TEMP"
            if name_from_db: # change to if player id was found in DB
                self.player_exists = True
                name_entry.delete(0, END)
                name_entry.insert(0, name_from_db)

        def add_player():
            player_id = int(id_entry.get())
            player_name = name_entry.get()
            equipment_code = int(equipment_entry.get())
            team = team_chosen.get()

            if team == "Red":
                team_red.player_added()
                current_row = team_red.num_players
                team_red.set(current_row, 0, player_id)
                team_red.set(current_row, 1, player_name)
                #########################
                #########################
                ## set up UDP here     ##
                ## to transmit         ##
                ## equipment code      ##
                #########################
                #########################
                team_red_players[player_id] = {"name": player_name, "equipment": equipment_code}

            elif team == "Blue":
                team_blue.player_added()
                current_row = team_blue.num_players
                team_blue.set(current_row, 0, player_id)
                team_blue.set(current_row, 1, player_name)
                #########################
                #########################
                ## set up UDP here     ##
                ## to transmit         ##
                ## equipment code      ##
                #########################
                #########################
                team_blue_players[player_id] = {"name": player_name, "equipment": equipment_code}

            if not self.player_exists:
                pass
                #########################
                #########################
                ## add player to DB    ##
                #########################
                #########################
            else:
                self.player_exists = False

            id_entry.delete(0, END)
            name_entry.delete(0, END)
            equipment_entry.delete(0, END)


        Title = tk.Label(self, text="Player Entry", 
                        fg="white", bg="black", font=("Lexend Bold", 40))
        Title.grid(row=0, column=0, columnspan=2, pady=15)
        
        team_chosen = tk.StringVar()
        team_chosen.set("Red")
        team_red_players = {}
        team_blue_players = {}

        team_red = TeamTable(self, 16, 2)
        team_blue = TeamTable(self, 16, 2)
        team_red.grid(row=1, column=0, padx=15, pady=15)
        team_blue.grid(row=1, column=1, padx=15, pady=15)

        team_red.set(0,0,"Player ID", font = ("Lexend Bold", 25), color = "red")
        team_red.set(0,1,"Name", font = ("Lexend Bold", 25), color = "red")
        team_blue.set(0,0,"Player ID", font = ("Lexend Bold", 25), color = "deep sky blue")
        team_blue.set(0,1,"Name", font = ("Lexend Bold", 25), color = "deep sky blue")

        id_label = tk.Label(self, text="Enter Player ID:", 
                            bg="black", fg="white", 
                            font=("Lexend Bold", 25))
        id_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        id_entry_frame = tk.Frame(self, bg ="black")
        id_entry_frame.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        id_entry = tk.Entry(id_entry_frame, bg="gray", fg="white",
                            font=("Lexend Thin", 22), borderwidth=1)
        id_entry.grid(row=0, column=0, sticky="w")
        check_id_button = tk.Button(id_entry_frame, text="Check ID",
                                    bg="gray", fg="white",
                                    command=check_id)
        check_id_button.grid(row=0, column=1, sticky="e", padx=5)

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

        add_player_button = tk.Button(self, text="Add Player",
                                bg="gray", fg="white",
                                command = add_player)
        add_player_button.grid(row=6, column=0, columnspan=2, pady=10)



class TeamTable(tk.Frame):
    def __init__(self, parent, rows, columns):
        tk.Frame.__init__(self, parent, background="white")
        self._widgets = []
        self.num_players = 0
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

    def player_added(self):
        self.num_players += 1


if __name__ == "__main__":
    splash = SplashScreen()
    splash.mainloop()
    app = PlayerEntryScreen()
    app.mainloop()