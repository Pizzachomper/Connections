import csv
import random
from tkinter import *
from functools import partial  # To prevent unwanted windows

# Functions go here
def get_items():
    
    # Retrieve words from csv file and put them in a list
    file = open("03_Connections/Csv/connections_quiz.csv", "r")
    all_items = list(csv.reader(file, delimiter=","))
    file.close()

    # remove the first row of headings
    all_items.pop(0)

    return all_items

def get_results():

    all_items_list = get_items()

    # Create lists to append items into
    all_results = []
    all_words = []
    before_after = []
    answer = []
    clue = []

    # loop until we have 3 different groups of items which arent duplicates
    while len(all_results) < 3:
        potential_items = random.choice(all_items_list)

        # Get the score and check its not a duplicate
        if potential_items[5] not in answer:
            all_results.append(potential_items)
            before_after.append(potential_items[0])
            all_words.append(potential_items[1])
            all_words.append(potential_items[2])
            all_words.append(potential_items[3])
            all_words.append(potential_items[4])
            answer.append(potential_items[5])
            clue.append(potential_items[6])

    return all_results, before_after, all_words, answer, clue

# Classes start here
class StartGame:
    """
    Initial Game Interface
    """
    def __init__(self):
        """
        Conections GUI
        """

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Strings for Labels
        intro_string = "Each round you will be asked to choose 4 words which can group together.\n"\
                       "The more groups you get correct the more points you earn.\n"\

        # Choose string = oops - please enter a whole number more than 0
        choose_string = "How many rounds do you want to play?"

        # list of labels to be made (text | font | fg)
        start_labels_list = [
            ["Conections", ("Arial", "16", "bold"), None],
            [intro_string, ("Arial", "12"), None],
            [choose_string, ("Arial", "12", "bold"), "#009900"]
        ]

        # Create labels and them to the refrence list
        start_label_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1],
                                fg=item[2],
                                wraplength=350, justify="left", pady=10, padx=20)
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        # Extract choice label so that it can be changed to an error message if necessary
        self.choose_label = start_label_ref[2]

        # Frame so that entry box and button can be in the same row
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", "20", "bold"),
                                        width=10)
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)
        
        # Create play button
        self.play_button = Button(self.entry_area_frame, font=("Arial", "16", "bold"),
                                    fg="#FFFFFF", bg="#0057D8", text="Play", width=10,
                                    command=self.check_rounds)
        self.play_button.grid(row=0, column=1, padx=20, pady=20)

    def check_rounds(self):
        """
        Checks user have entered 1 or more rounds
        """

        # Retrieve number of rounds the user wants to play
        rounds_wanted = self.num_rounds_entry.get()

        # Reset label and entry box (for when users come to home screen)
        self.choose_label.config(fg="#009900", font=("Arial", "12", "bold"))
        self.num_rounds_entry.config(bg="#FFFFFF")

        error = "Oops - please choose a whole number more than 0"
        has_errors = "no"

        # checks that amount to be converted is a number above absolute zero
        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                # Invoke Play Class (and take across number of rounds)
                Play(rounds_wanted)
                # Hide root window (ie: hide rounds choice window)
                root.withdraw()

            else:
                has_errors = "yes"
        
        except ValueError:
            has_errors = "yes"
        
        # display the error if necessary
        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000",
                                     font=("Arial", "10", "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)


class Play:
    """
    Interface for playing the Conections Game
    """

    def __init__(self, how_many):
        
        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # If users press the 'x' on the game window, end the entire game
        self.play_box.protocol('WM_DELETE_WINDOW', root.destroy)

        self.game_heading_label = Label(self.game_frame, text= f"Round 1 of {how_many}",
                                        font=("Arial", "16", "bold"), padx=5, pady=5)
        self.game_heading_label.grid(row=0)

        self.hints_button = Button(self.game_frame, font=("Arial", "14", "bold"),
                                   text="Hints", width=15, fg="#FFFFFF",
                                   bg="#FF8000", padx=10, pady=10, command=self.to_hints)
        self.hints_button.grid(row=1)

        self.end_game_button = Button(self.game_frame, text="End Game",
                                      font=("Arial", "16", "bold"), padx=20, pady=10,
                                      fg="#FFFFFF", bg="#990000", width="10",
                                      command=self.close_play)
        self.end_game_button.grid(row=2)

    def new_round(self):
        """
        Chooses four colours, works out median for score to beat. 
        configures buttons with choosen colours
        """

        # reteieve number of rounds played, add one to it and configure heading
        # rounds_played = self.rounds_played.get()
        # self.rounds_played.set(rounds_played)

        # Update heading and score to beat labels. Hide results label
        # self.heading_label.config(text=f"Round {rounds_played + 1} of {rounds_wanted}")
        # self.results_label.config(text=f"{'=' * 7}", bg="#F0F0F0")
            
        # self.next_button.config(state=DISABLED)

    def close_play(self):
        # reshow root (ie: choose rounds) and end current game / allow new game to start
        root.deiconify()
        self.play_box.destroy()

    def to_hints(self):
        """
        Displays hints for playing game
        :return:
        """
        DisplayHints(self)

# Hint and stat classes
class DisplayHints:
    """
    Displays hints for Connections game
    """

    def __init__(self, partner):
        
        # setup dialouge box and background colour
        self.hint_box = Toplevel()

        # disable hint button
        partner.hints_button.config(state=DISABLED)

        # If users press cross at top, closes hint box and releases hint button
        self.hint_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_hint, partner)) 

        self.hint_frame = Frame(self.hint_box, width=350)
        self.hint_frame.grid()

        self.hint_heading_label = Label(self.hint_frame,
                                        text= "Hint / Info",
                                        font=("Arial", "14", "bold"))
        self.hint_heading_label.grid(row=0)

        hint_text = "To use the program, enter the number of rounds you wish to play.\n"\
                    "Then you will be asked to choose 4 words which can group together.\n"\
                    "The more groups you get correct the more points you earn.\n"\
                    "Click the stats button to see more info about your points" 

        self.hint_text_label = Label(self.hint_frame,
                                     text=hint_text, wraplength=350,
                                     justify="left")
        self.hint_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.hint_frame,
                                     font=("Arial", "14", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF", 
                                     command=partial(self.close_hint, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # Closes help dialogue (used by button and x at the top of dialogue)

    def close_hint(self, partner):
        partner.hints_button.config(state=NORMAL)
        self.hint_box.destroy()



# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Connections")
    StartGame()
    root.mainloop()