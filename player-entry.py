import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from supabase import create_client
import json
import socket
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2) # if your windows version >= 8.1
except:
    ctypes.windll.user32.SetProcessDPIAware() # win 8.0 or less 
DEFAULT_FONT = ("Lexend Thin", 22)
BOLD_FONT = ("Lexend Bold", 25)
TITLE_FONT = ("Lexend Bold", 40)
API_URL = "https://yosaltaismwvhvbpvpzq.supabase.co"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlvc2FsdGFpc213dmh2YnB2cHpxIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTU3NTU3MTQsImV4cCI6MjAxMTMzMTcxNH0.AXuDtr3a1F3bEGhkfwPF0jtJE1MgtCEN-LCYczyHv7w"
# establish database connection
supabase = create_client(API_URL, API_KEY)

class UDP:
    # initialize socket
    def __init__(self):
        # server's IP address and port number
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.HOST_PORT = 7501

        # all clients IP addresses and port numbers
        self.CLIENTS = socket.gethostbyname(socket.gethostname())
        self.CLIENT_PORTS = 7500

        # specifies socket type (internet and UDP)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # binds socket to the server's IP address and port number
        self.server.bind((self.HOST, self.HOST_PORT))

    # server receives 1024 bytes of information from client
    def receive_data(self):
        received_information, address = self.server.recvfrom(1024)
        print("Information recieved from client: " + received_information.decode('utf-8'))
        return received_information.decode('utf-8')
        
    # server sends variable amount of bytes to all clients
    def broadcast_data(self, message):
        self.server.sendto(message.encode('utf-8'), (self.CLIENTS, self.CLIENT_PORTS))
        print("Sending code to client: " + message)
# open UDP socket
server_socket = UDP()



class SplashScreen(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # set fullscreen with black background
        self.attributes('-fullscreen', True)
        self.configure(bg = "black")

        # create frame to hold image
        frame = Frame(self, bg = "black")
        frame.place(anchor = 'center', relx = 0.5, rely = 0.5)

        # prepare image
        origImg = Image.open("photon.jpg")
        resizeImg = origImg.resize((self.winfo_screenwidth(), self.winfo_screenheight()))
        self.img = ImageTk.PhotoImage(resizeImg)

        # place image in label contained by frame
        label = tk.Label(frame, image = self.img, borderwidth = 0)
        label.pack(fill = BOTH, expand = YES)
        
        # destroy splash screen after 3 seconds
        self.after(3000, lambda:self.destroy())



class PlayerEntryScreen(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.state('zoomed')
        self.configure(bg="black")
        # reset fonts based on screen size
        global DEFAULT_FONT, BOLD_FONT, TITLE_FONT
        font_base = self.winfo_screenheight()/95
        #self.winfo_screenwidth()/150
        DEFAULT_FONT = ("Lexend Thin", int(font_base))
        BOLD_FONT = ("Lexend Bold", int(font_base+2))
        TITLE_FONT = ("Lexend Bold", int(font_base*1.5))
        
        # establish boolean to track whether current player exists in database
        self.player_exists = False
        # initiate dictionaries to hold players for each team
        self.team_red_players = {}
        self.team_blue_players = {}

        ###########################################################
        ### checks if current player_id exists in the database  ### 
        ### and auto fills entry boxes for names if id is found ###
        ###########################################################
        def check_id():
            # use entered player_id to query database for existing entry
            player_id = id_entry.get()
            data = []
            try:
                f_name=supabase.table('player').select('first_name').eq('id', player_id).execute().data[0] # fetching documents
                l_name=supabase.table('player').select('last_name').eq('id', player_id).execute().data[0] # fetching documents
                c_name=supabase.table('player').select('codename').eq('id', player_id).execute().data[0] # fetching documents
                data = [f_name['first_name'], l_name['last_name'], c_name['codename']]
            except:
                data = ["", "", ""]
            
            # clear existing values in name entry fields
            name_entry.delete(0, END)
            first_name_entry.delete(0, END)
            last_name_entry.delete(0, END)

            # show remaining fields
            name_label.grid()
            name_entry.grid()
            first_name_frame.grid()
            last_name_frame.grid()
            team_label.grid()
            dropdown.grid()
            equipment_label.grid()
            equipment_entry.grid()
            add_player_button.grid()

            # determine whether each piece of data was returned
            data_returned = []
            for name in data:
                if len(name) > 0:
                    data_returned.append(True)
                if len(name) <= 0:
                    data_returned.append(False)

            # if all elements of the data were returned, insert into entry boxes
            if all(data_returned) and len(data_returned) == 3:
                # mark the current player as existing in the database
                self.player_exists = True

                name_entry.insert(0, data[2])
                first_name_entry.insert(0, data[0])
                last_name_entry.insert(0, data[1])

        ###########################################################
        ### adds player to team table, team dictionary, and     ###
        ### if id does not already exist database               ###
        ###########################################################
        def add_player():
            player_id = int(id_entry.get())
            player_name = name_entry.get()
            equipment_code = equipment_entry.get()
            team = team_chosen.get()
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()

            if team == "Red":
                # add player to red team table
                team_red.player_added()
                current_row = team_red.num_players
                team_red.set(current_row, 0, player_id)
                team_red.set(current_row, 1, player_name)
                
                # broadcast equipment code
                server_socket.broadcast_data(equipment_code)

                # store player details in dictionary
                self.team_red_players[player_id] = {"name": player_name, "equipment": equipment_code}

            elif team == "Blue":
                # add player to blue team table
                team_blue.player_added()
                current_row = team_blue.num_players
                team_blue.set(current_row, 0, player_id)
                team_blue.set(current_row, 1, player_name)
                
                # broadcast equipment code
                server_socket.broadcast_data(equipment_code)

                # store player details in dictionary
                self.team_blue_players[player_id] = {"name": player_name, "equipment": equipment_code}

            # insert into the database if the player was not found in check_id()
            if not self.player_exists:
                data = {
                    'id': player_id,
                    'first_name': first_name,
                    'last_name': last_name,
                    'codename': player_name
                }
                supabase.table('player').insert(data).execute() # inserting one record
            
            else:
                self.player_exists = False
            
            # clear entry box values and hide fields
            id_entry.delete(0, END)
            name_entry.delete(0, END)
            first_name_entry.delete(0, END)
            last_name_entry.delete(0, END)
            equipment_entry.delete(0, END)
            name_label.grid_remove()
            name_entry.grid_remove()
            first_name_frame.grid_remove()
            last_name_frame.grid_remove()
            team_label.grid_remove()
            dropdown.grid_remove()
            equipment_label.grid_remove()
            equipment_entry.grid_remove()
            add_player_button.grid_remove()

        ###########################################################
        ### clears all players from both teams                  ### 
        ###########################################################
        def clear_teams():
            team_red.clear_team()
            self.team_red_players = {}
            team_blue.clear_team()
            self.team_blue_players = {}

        ###########################################################
        ### starts the game and moves to play action screen     ###
        ### after start button is clicked                       ###
        ###########################################################
        def start_game():
            pass

        # create title for player entry screen contained in frame
        title_bar_frame = tk.Frame(self, bg="black")
        title_bar_frame.place(anchor = 'center', relx = 0.5, rely = 0.5)
        title_bar_frame.grid(row=0, column=0, columnspan=2, pady=15)
        title = tk.Label(title_bar_frame, text="Player Entry", 
                        fg="white", bg="black", font=TITLE_FONT)
        title.grid(row=0, column=1, padx=250)

        # add button to clear teams
        clear_teams_button = tk.Button(title_bar_frame, text="Empty Teams",
                                    bg="gray", fg="white",
                                    command=clear_teams, font=DEFAULT_FONT,
                                    activebackground="white", activeforeground="black")
        clear_teams_button.grid(row=0, column=0, sticky="w", padx=100)

        # add button to start game
        start_game_button = tk.Button(title_bar_frame, text="Start Game",
                                    bg="gray", fg="white",
                                    command=start_game, font=DEFAULT_FONT,
                                    activebackground="white", activeforeground="black")
        start_game_button.grid(row=0, column=2, sticky="e", padx=100)

        # initialize tables for each team
        team_red = TeamTable(self, 16, 2)
        team_blue = TeamTable(self, 16, 2)
        team_red.grid(row=1, column=0, padx=15, pady=15)
        team_blue.grid(row=1, column=1, padx=15, pady=15)
        team_red.set(0,0,"Player ID", font=BOLD_FONT, color = "red")
        team_red.set(0,1,"Name", font=BOLD_FONT, color = "red")
        team_blue.set(0,0,"Player ID", font=BOLD_FONT, color = "deep sky blue")
        team_blue.set(0,1,"Name", font=BOLD_FONT, color = "deep sky blue")

        # initialize id label and entry box
        id_label = tk.Label(self, text="Enter Player ID:", 
                            bg="black", fg="white", 
                            font=BOLD_FONT)
        id_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        id_entry_frame = tk.Frame(self, bg ="black")
        id_entry_frame.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        id_entry = tk.Entry(id_entry_frame, bg="gray", fg="white",
                            font=DEFAULT_FONT, borderwidth=1)
        id_entry.grid(row=0, column=0, sticky="w")

        # create button to check if id exists in the database
        check_id_button = tk.Button(id_entry_frame, text="Check ID",
                                    bg="gray", fg="white",
                                    command=check_id, font=DEFAULT_FONT,
                                    activebackground="white", activeforeground="black")
        check_id_button.grid(row=0, column=1, sticky="e", padx=5)

        # initialize codename label and entry box
        name_label = tk.Label(self, text="Enter Code Name:", 
                            bg="black", fg="white", 
                            font=BOLD_FONT)
        name_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        name_label.grid_remove()
        name_entry = tk.Entry(self, bg="gray", fg="white",
                            font=DEFAULT_FONT, borderwidth=1)
        name_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        name_entry.grid_remove()

        # intialize first name label and entry box
        first_name_frame = tk.Frame(self, bg="black")
        first_name_frame.grid(row=4, column=0, sticky="e", padx=15)
        first_name_label = tk.Label(first_name_frame, text="Enter First Name: ", 
                            bg="black", fg="white", 
                            font=BOLD_FONT)
        first_name_label.grid(row=0, column=0, sticky="e")
        first_name_entry = tk.Entry(first_name_frame, bg="gray", fg="white",
                            font=DEFAULT_FONT, borderwidth=1)
        first_name_entry.grid(row=0, column=1, sticky="w")
        first_name_frame.grid_remove()

        # initialize last name label and entry box
        last_name_frame = tk.Frame(self, bg="black")
        last_name_frame.grid(row=4, column=1, sticky="w", padx=15)
        last_name_label = tk.Label(last_name_frame, text="Enter Last Name: ", 
                            bg="black", fg="white", 
                            font=BOLD_FONT)
        last_name_label.grid(row=0, column=0, sticky="e")
        last_name_entry = tk.Entry(last_name_frame, bg="gray", fg="white",
                            font=DEFAULT_FONT, borderwidth=1)
        last_name_entry.grid(row=0, column=1, sticky="w")     
        last_name_frame.grid_remove()   
        
        # initialize team selection dropdown
        team_chosen = tk.StringVar()
        team_chosen.set("Red")
        team_label = tk.Label(self, text="Choose Team:", 
                            bg="black", fg="white", 
                            font=BOLD_FONT)
        team_label.grid(row=5, column=0, sticky="e", padx=5, pady=5)
        team_label.grid_remove()
        dropdown = tk.OptionMenu(self, team_chosen, *['Red','Blue'])
        dropdown.grid(row=5, column=1, sticky="w", padx=5, pady=5)
        dropdown.configure(font=DEFAULT_FONT, bg="black", fg="white")
        team_dropdown = self.nametowidget(dropdown.menuname)
        team_dropdown.configure(font=DEFAULT_FONT, bg="black", fg="white")
        dropdown.grid_remove()

        # initialize equipment label and entry box
        equipment_label = tk.Label(self, text="Enter Equipment ID:", 
                            bg="black", fg="white", 
                            font=BOLD_FONT)
        equipment_label.grid(row=6, column=0, sticky="e", padx=5, pady=5)
        equipment_label.grid_remove()
        equipment_entry = tk.Entry(self, bg="gray", fg="white",
                            font=DEFAULT_FONT, borderwidth=1)
        equipment_entry.grid(row=6, column=1, sticky="w", padx=5, pady=5)
        equipment_entry.grid_remove()

        # create button to add player to table & database
        add_player_button = tk.Button(self, text="Add Player",
                                bg="gray", fg="white",
                                command = add_player, font=DEFAULT_FONT,
                                activebackground="white", activeforeground="black")
        add_player_button.grid(row=7, column=0, columnspan=2, pady=10)
        add_player_button.grid_remove()



class TeamTable(tk.Frame):
    def __init__(self, parent, rows, columns):
        tk.Frame.__init__(self, parent, background="white")
        # list to store all cells of the table
        self._widgets = []
        self.num_players = 0
        self.nrow = rows
        self.ncol = columns
        
        # initialize labels for each column within each row, then append to widgets list
        for row in range(self.nrow):
            current_row = []
            for column in range(self.ncol):
                label = tk.Label(self, text=" ", 
                                 borderwidth=0, width=20,
                                 background="black", foreground="red",
                                 font=DEFAULT_FONT)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

        # align columns
        for column in range(self.ncol):
            self.grid_columnconfigure(column, weight=1)

    # allows table cell's value to be set
    def set(self, row, column, value, font=DEFAULT_FONT, color="white"):
        if(font != DEFAULT_FONT and font != BOLD_FONT and font != TITLE_FONT):
            font = DEFAULT_FONT
        widget = self._widgets[row][column]
        widget.configure(text=value, font=font, fg=color)

    # keep track of num players in each team
    def player_added(self):
        self.num_players += 1

    def clear_team(self):
        for row in range(1, self.nrow):
            for col in range(self.ncol):
                self.set(row, col, "")
        self.num_players = 0



if __name__ == "__main__":
    splash = SplashScreen()
    splash.mainloop()
    app = PlayerEntryScreen()
    app.mainloop()