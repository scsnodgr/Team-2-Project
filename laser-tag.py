import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from supabase import create_client
from playsound import playsound
import random
import json
import socket
DEFAULT_FONT = ("Lexend Thin", 15)
BOLD_FONT = ("Lexend Bold", 18)
API_URL = "https://yosaltaismwvhvbpvpzq.supabase.co"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlvc2FsdGFpc213dmh2YnB2cHpxIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTU3NTU3MTQsImV4cCI6MjAxMTMzMTcxNH0.AXuDtr3a1F3bEGhkfwPF0jtJE1MgtCEN-LCYczyHv7w"
# establish database connection
supabase = create_client(API_URL, API_KEY)

class UDP:
    # initialize socket
    def __init__(self):
        # server's IP address
        self.HOST = socket.gethostbyname(socket.gethostname())

        # client's IP address and port number, temporarily set to 1 1 
        self.client_address = ("1", "1")

        # player who scored 10 points from hitting another player, temporarily set to 1111
        self.player_who_scored = 1111

        # server's broadcast and receive ports
        self.BROADCAST_PORT = 7500
        self.RECEIVE_PORT = 7501

        # specifies socket type (internet and UDP) for broadcast and receive sockets
        self.server_broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # binds sockets to the server's IP address and associated port number
        # self.server_broadcast.bind((self.HOST, self.BROADCAST_PORT))
        self.server_broadcast.bind((self.HOST, self.BROADCAST_PORT))
        self.server_receive.bind((self.HOST, self.RECEIVE_PORT))

    # turns a message of the form "equipment id of player transmitting:equipment id of player hit"
    # into a message of the form "equipment id of player hit"
    def parse_data(self, message):
        parts = message.split(":")
        self.player_who_scored = parts[0]
        player_hit_ID = parts[1]
        return player_hit_ID
    
    # server sends variable amount of bytes to all clients
    def broadcast_data(self, message):
        self.server_broadcast.sendto(message.encode('utf-8'), self.client_address)
        print("Sending " + message + " to traffic generator")

    # server receives 1024 bytes of information from client
    def receive_data(self):
        received_information, address = self.server_receive.recvfrom(1024)
        self.client_address = address
        print("\nInformation recieved from traffic generator: " + received_information.decode('utf-8'))
        player_hit_ID = self.parse_data(received_information.decode('utf-8'))
        self.broadcast_data(player_hit_ID)
        return received_information.decode('utf-8')
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
        origImg = Image.open("photon.jpg") #location of photon.jpg
        resizeImg = origImg.resize((self.winfo_screenwidth(), self.winfo_screenheight()))
        self.img = ImageTk.PhotoImage(resizeImg)

        # place image in label contained by frame
        label = tk.Label(frame, image = self.img, borderwidth = 0)
        label.pack(fill = BOTH, expand = YES)
        
        # destroy splash screen after 3 seconds
        self.after(3000, self.destroy)



class PlayerEntryScreen(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.configure(bg="black")
        
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
            red_team = self.team_red_players
            blue_team = self.team_blue_players
            play_action = PlayActionScreen(red_team, blue_team)
            self.after(500, self.destroy)
            play_action.mainloop()
            

        ttk.Style().configure('gray/black.TButton', foreground='black', background='gray', font=DEFAULT_FONT)

        # create title for player entry screen contained in frame
        title_bar_frame = tk.Frame(self, bg="black")
        title_bar_frame.grid(row=0, column=0, columnspan=2, pady=15)
        title = tk.Label(title_bar_frame, text="Player Entry", 
                        fg="white", bg="black", font=("Lexend Bold", 40))
        title.grid(row=0, column=1, padx=250)

        # add button to clear teams
        clear_teams_button = ttk.Button(title_bar_frame, text="Empty Teams",
                                    style='gray/black.TButton',
                                    command=clear_teams)
        clear_teams_button.grid(row=0, column=0, sticky="w", padx=100)

        # add button to start game
        start_game_button = ttk.Button(title_bar_frame, text="Start Game",
                                    style='gray/black.TButton',
                                    command=start_game)
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
        check_id_button = ttk.Button(id_entry_frame, text="Check ID",
                                    style='gray/black.TButton',
                                    command=check_id)
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
        add_player_button = ttk.Button(self, text="Add Player",
                                    style='gray/black.TButton',
                                    command=add_player)
        add_player_button.grid(row=7, column=0, columnspan=2, pady=10)
        add_player_button.grid_remove()


class PlayActionScreen(tk.Tk):
    def __init__(self, red_team_players, blue_team_players):
        tk.Tk.__init__(self)
        self.configure(bg="black")
        self.red_num_players = len(red_team_players)
        self.blue_num_players = len(blue_team_players)
        self.red_team_scores = {}
        self.blue_team_scores = {}
        self.red_team_activity = []
        self.blue_team_activity = []
        self.audio_tracks =  ['.\\Audio\\Track01.mp3', '.\\Audio\\Track02.mp3', '.\\Audio\\Track03.mp3', '.\\Audio\\Track04.mp3', '.\\Audio\\Track05.mp3', '.\\Audio\\Track06.mp3', '.\\Audio\\Track07.mp3', '.\\Audio\\Track08.mp3']

        for player in red_team_players.values():
            self.red_team_scores[player["equipment"]] = {"name":  player["name"], 
                                                         "score": 0}
        for player in blue_team_players.values():
            self.blue_team_scores[player["equipment"]] = {"name":  player["name"], 
                                                         "score": 0}
        
        def update_score_tables(self):
            # sort score dictionaries
            self.red_team_scores = dict(sorted(self.red_team_scores.items(), key = lambda x: x[1]["score"], reverse=True))
            self.blue_team_scores = dict(sorted(self.blue_team_scores.items(), key = lambda x: x[1]["score"], reverse=True))

            red_team_equipment = self.red_team_scores.keys()
            blue_team_equipment = self.blue_team_scores.keys()
            red_total_score = sum([player["score"] for player in self.red_team_scores.values()])
            blue_total_score = sum([player["score"] for player in self.blue_team_scores.values()])

            # fill total rows
            team_red.set(team_red.nrow - 1, 0, "Total", color = "red")
            team_blue.set(team_blue.nrow - 1, 0, "Total", color = "deep sky blue")
            # if game_started, flash high total score
            if self.game_started:
                if self.time_left % 2 == 0:
                    team_red.set(team_red.nrow - 1, 1, red_total_score)
                    team_blue.set(team_blue.nrow - 1, 1, blue_total_score)
                elif (self.time_left % 2 == 1) and (red_total_score > blue_total_score):
                    team_red.set(team_red.nrow - 1, 1, " ")
                    team_blue.set(team_blue.nrow - 1, 1, blue_total_score)
                elif (self.time_left % 2 == 1) and (blue_total_score > red_total_score):
                    team_red.set(team_red.nrow - 1, 1, red_total_score)
                    team_blue.set(team_blue.nrow - 1, 1, " ")

            # fill red team score table
            for j, id in enumerate(red_team_equipment):
                team_red.set(j, 0, self.red_team_scores[id]["name"], color = "red")
                # flash high scores
                if self.game_started:
                    if (j == 0) and (self.time_left % 2 == 0):
                        team_red.set(j, 1, self.red_team_scores[id]["score"])
                    elif (j == 0) and (self.time_left % 2 == 1):
                        team_red.set(j, 1, " ")
                    else:
                        team_red.set(j, 1, self.red_team_scores[id]["score"])

            # fill blue team score tablef
            for j, id in enumerate(blue_team_equipment):
                team_blue.set(j, 0, self.blue_team_scores[id]["name"], color = "deep sky blue")
                # flash high scores
                if self.game_started:
                    if (j == 0) and (self.time_left % 2 == 0):
                        team_blue.set(j, 1, self.blue_team_scores[id]["score"])
                    elif (j == 0) and (self.time_left % 2 == 1):
                        team_blue.set(j, 1, " ")
                    else:
                        team_blue.set(j, 1, self.blue_team_scores[id]["score"])

        def update_activity_log(self, player_hit, player_scored):
            # inserting message into red activity log if red scored
            if player_scored in self.red_team_scores.keys():
                # check if base hit
                if player_hit == 43:
                    hit_name = "BLUE BASE"
                else:
                    hit_name = self.blue_team_scores[player_hit]["name"]
                scored_name = self.red_team_scores[player_scored]["name"]
                message = f'{scored_name} hit {hit_name}'
                self.red_team_activity.insert(0, message)
            # inserting message into blue activity log if blue scored
            else:
                # check if base hit
                if player_hit == 53:
                    hit_name = "RED BASE"
                else:
                    hit_name = self.red_team_scores[player_hit]["name"]
                scored_name = self.blue_team_scores[player_scored]["name"]
                message = f'{scored_name} hit {hit_name}'
                self.blue_team_activity.insert(0, message)

            # keep activity log length at 10
            if len(self.red_team_activity) > 10:
                self.red_team_activity = self.red_team_activity[:-1]
            if len(self.blue_team_activity) > 10:
                self.blue_team_activity = self.blue_team_activity[:-1]

            # fill activity tables
            for i, message in enumerate(self.red_team_activity):
                team_red_activity_table.set(i, 0, message)
            for i, message in enumerate(self.blue_team_activity):
                team_blue_activity_table.set(i, 0, message)

        def _seconds_to_time_string(self, seconds):
            minutes, sec = divmod(seconds, 60)
            return "{:02}:{:02}".format(minutes, sec)

        def update_timer(self):
            if self.time_left > 0:
                self.time_left -= 1
                self.timer_label.config(text=_seconds_to_time_string(self, self.time_left))
                if self.time_left == 17:
                    audio = random.choice(self.audio_tracks)
                    playsound(audio, block = False)
                if self.game_started == True:
                    player_hit = server_socket.receive_data().split(":")[1]
                    player_who_scored = server_socket.player_who_scored
                    if player_who_scored in self.red_team_scores.keys():
                        # check if base was hit
                        if player_hit == 43:
                            self.red_team_scores[player_who_scored]["score"] += 100
                        else:
                            self.red_team_scores[player_who_scored]["score"] += 10
                    else:
                        # check if base was hit
                        if player_hit == 53:
                            self.blue_team_scores[player_who_scored]["score"] += 100
                        else:
                            self.blue_team_scores[player_who_scored]["score"] += 10
                    update_score_tables(self)
                    update_activity_log(self, player_hit, player_who_scored)    
                # Schedule the function to run after 1000ms (1 second)
                self.after(1000, update_timer, self)
            else:
                if self.game_started == True:
                    # server broadcasts code 221 three times 
                    server_socket.broadcast_data("221")
                    server_socket.broadcast_data("221")
                    server_socket.broadcast_data("221")
                    return_button.grid()
                    return
                else:
                    # start game with 6 minute timer
                    self.time_left = 6 * 60
                    server_socket.broadcast_data("202")
                    self.game_started = True
                    self.after(1000, update_timer, self)
        
        def return_to_player_entry(self):
            player_entry = PlayerEntryScreen()
            self.after(250, self.destroy)
            player_entry.mainloop()

        title_bar = tk.Frame(self, bg="black")
        title_bar.grid(row=0, column=0, columnspan=2, pady=15)

        self.game_started = False
        self.time_left = 30 
        self.timer_label = tk.Label(title_bar, text=_seconds_to_time_string(self, self.time_left), 
                                    bg="black", fg="white", font=BOLD_FONT)
        self.timer_label.grid(row=0, column=1)
        update_timer(self)

        team_red_label = tk.Label(title_bar, text="Red Team", 
                            bg="black", fg="red", 
                            font=BOLD_FONT)
        team_red_label.grid(row=0, column=0, sticky="w", padx=250)

        team_blue_label = tk.Label(title_bar, text="Blue Team", 
                            bg="black", fg="deep sky blue", 
                            font=BOLD_FONT)
        team_blue_label.grid(row=0, column=2, sticky="e", padx = 250)


        team_red = TeamTable(self, self.red_num_players + 2, 2, width=30)
        team_blue = TeamTable(self, self.blue_num_players + 2, 2, width=30)
        team_red.grid(row=1, column=0, padx=15, pady=5)
        team_blue.grid(row=1, column=1, padx=15, pady=5)
        update_score_tables(self)

        activity_label_red = tk.Label(self, text="Activity",
                                      bg="black", fg="red",
                                      font=BOLD_FONT)
        activity_label_blue = tk.Label(self, text="Activity",
                                       bg = "black", fg="deep sky blue",
                                       font=BOLD_FONT)
        activity_label_red.grid(row=2, column=0, pady=5, sticky="s")
        activity_label_blue.grid(row=2, column=1, pady=5, sticky="s")

        team_red_activity_table = TeamTable(self, 10, 1, width=60)
        team_blue_activity_table = TeamTable(self, 10, 1, width=60)
        team_red_activity_table.grid(row=3, column=0, pady=5, sticky="n")
        team_blue_activity_table.grid(row=3, column=1, pady=5, sticky="n")

        return_command = lambda:return_to_player_entry(self)
        return_button = ttk.Button(self, text="Return to Player Entry",
                                    style='gray/black.TButton',
                                    command=return_command)
        return_button.grid(row=0, column=0, columnspan=2)
        return_button.grid_remove()

        



class TeamTable(tk.Frame):
    def __init__(self, parent, rows, columns, width=20):
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
                                 borderwidth=0, width=width,
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
    server_socket.receive_data()
    splash = SplashScreen()
    splash.mainloop()
    player_entry = PlayerEntryScreen()
    player_entry.mainloop()
