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
        Connections GUI
        """

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Strings for Labels
        intro_string = "In each round you will be invited to choose 4 words to create a group.\n"\
                        "Your goal is to create 3 groups and win the round\n"\
                        "To begin, please choose how many rounds you'd like to play" 

        # Choose string = oops - please enter a whole number more than 0
        choose_string = "How many rounds do you want to play?"

        # list of labels to be made (text | font | fg)
        start_labels_list = [
            ["Connections", ("Arial", "16", "bold"), None],
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
                # Clear entry box and reset instruction label so that when users play a new game,
                # they don't see an error message
                self.num_rounds_entry.delete(0, END)
                self.choose_label.config(text="How many rounds do you want to play?")
                
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
        
        # Rounds played - start with 0
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # body font for most labels
        body_font = ("Arial", "12")

        # List for label details (text | font | background | row)
        play_labels_list = [
            ["Score to beat: #", body_font, "#FFF2CC", 1],
            ["Groups will appear after you click 4 words. Good luck", body_font, "#D5E8D4", 2],
            ["Choose a word below.", body_font, "#D5E8D4", 3],
            ["You chose, result", body_font, "#D5E8D4", 5]
        ]

        play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.game_frame, text=item[0], font=item[1],
                                    bg=item[2], wraplength=300, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10)
            play_labels_ref.append(item)

        # Retrieve Labels so they can be configured later
        self.heading_label = play_labels_ref[0]
        self.target_label = play_labels_ref[1]
        self.group_label = play_labels_ref[2]
        self.word_label = play_labels_ref[3]
        self.results_label = play_labels_ref[4]

        # Set up group buttons
        self.group_frame = Frame(self.game_frame)
        self.group_frame.grid(row=3)

        # Create 3 group buttons
        for item in range(0, 3):
            self.group_button = Button(self.group_frame, font=body_font,
                                       text="Group Name", width=21)
            self.group_button.grid(row= item // 3, column=item % 3, padx=5, pady=5)

        # set up word buttons
        self.word_frame = Frame(self.game_frame)
        self.word_frame.grid(row=4)

        # # Create 12 buttons in a 4 by 3 grid
        for item in range(0, 12):
            self.word_button = Button(self.word_frame, font=body_font,
                                      text="Word Name", width=15)
            
            self.word_button.grid(row=item // 4, column=item % 4, padx=5, pady=5)

        # Frame to hold hints and stats buttons
        self.hints_stats_frame = Frame(self.game_frame)
        self.hints_stats_frame.grid(row=6)

        # List for buttons
        control_button_list = [
            [self.game_frame, "Next Round", "#0057D8", "", 21, 5, None],
            [self.hints_stats_frame, "Hints", "#FF8000", "", 10, 0, 0],
            [self.hints_stats_frame, "Stats", "#333333", "", 10, 0, 1],
            [self.game_frame, "End", "#990000", self.close_play, 30, 7, None]
        ]

        # Create control buttons to add to list
        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2],
                                         command=item[3], font=("Arial", "16", "bold"),
                                         fg="#FFFFFF", width=item[4])
            make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)

            control_ref_list.append(make_control_button)

        # Retrieve next, stats and end button so that they can be configured
        self.next_button = control_ref_list[0]
        self.stats_button = control_ref_list[2]
        self.end_game_button = control_ref_list[3]

        # Once interface has been created, invoke new round function for the first round
        self.new_round()

    def new_round(self):
        """ 
        Configures buttons, and creates a new round
        """

        # reteieve number of rounds played, add one to it and configure heading
        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        rounds_wanted = self.rounds_wanted.get()

        # Update heading and score to beat labels. Hide results label
        self.heading_label.config(text=f"Round {rounds_played} of {rounds_wanted}")
        self.results_label.config(text=f"{'=' * 7}", bg="#F0F0F0")
            
        self.next_button.config(state=DISABLED)

    def round_results(self):
        """
        Retrieves which button was pushed (index 0 - 3), retrieves score
        and then compares it with the target, updates results and add results to stat list.
        """

        # Enable stats and next buttons, disables word and group buttons
        self.next_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)

        # Check to see if game is over
        rounds_played = self.rounds_played.get()
        rounds_wanted = self.rounds_wanted.get()

        if rounds_played == rounds_wanted:
            self.next_button.config(state=DISABLED, text="Game Over")
            self.end_game_button.config(text="Play Again", bg="#006600")

        for item in self.word_button_ref:
            item.config(state=DISABLED)


    def close_play(self):
        # reshow root (ie: choose rounds) and end current game / allow new game to start
        root.deiconify()
        self.play_box.destroy()

# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Connections")
    StartGame()
    root.mainloop()