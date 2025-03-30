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

        # Create play button
        self.play_button = Button(self.start_frame, font=("Arial", "16", "bold"),
                                    fg="#FFFFFF", bg="#0057D8", text="Play", width=10,
                                    command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        """
        Checks users have entered 1 or more rounds
        """

        Play(5)
        # Hide root window (ie: hide round choice window)
        root.withdraw()


class Play:
    """
    Interface for playing the Conections Game
    """

    def __init__(self, how_many):

        # Integers / String Variables
        self.target_score = IntVar()

        # Rounds played - start with 0
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        # Item lists and more
        self.all_results_list = []
        self.before_after_list = []
        self.all_words_list = []
        self.answer_list = []
        self.clue_list = []

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # body font for most labels
        body_font = ("Arial", "12")

        # List for label details (text | font | background | row)
        play_labels_list = [
            ["Round # of #", ("Arial", "16", "bold"), None, 0],
            ["Score to beat: #", body_font, "#FFF2CC", 1],
            ["Choose words below. Good luck", body_font, "#D5E8D4", 2],
            ["You chose, result", body_font, "#D5E8D4", 4]
        ]

        play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.game_frame, text=item[0], font=item[1],
                                    bg=item[2], wraplength=300, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10)
            play_labels_ref.append(self.make_label)

        # Retrieve Labels so they can be configured later
        self.heading_label = play_labels_ref[0]
        self.target_label = play_labels_ref[1]
        self.results_label = play_labels_ref[3]

        # set up word buttons
        self.word_frame = Frame(self.game_frame)
        self.word_frame.grid(row=3)

        self.word_button_ref = []
        self.button_words_list = []

        # Create 4 buttons in a 2 by 2 grid
        for item in range(0, 4):
            self.word_button = Button(self.word_frame, font=body_font,
                                        text="Word Name", width=15,
                                        command=partial(self.round_results, item))
            self.word_button.grid(row=item // 2,
                                    column=item % 2,
                                    padx=5, pady=5)
            
            self.word_button_ref.append(self.word_button)
            
        # Frame to hold hints and stats buttons
        self.hints_stats_frame = Frame(self.game_frame)
        self.hints_stats_frame.grid(row=6)

        # List for buttons
        control_button_list = [
            [self.game_frame, "Next Round", "#0057D8", self.new_round, 21, 5, None],
            [self.hints_stats_frame, "Hints", "#FF8000", "", 10, 0, 0],
            [self.hints_stats_frame, "Stats", "#333333", "", 10, 0, 1],
            [self.game_frame, "End", "#990000", self.close_play, 21, 7, None]
        ]

        # Create buttons to add to list
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
        Chooses 12 words, with 3 groups of 4 words for the user to guess. 
        configures buttons with choosen words
        """

        # reteieve number of rounds played, add one to it and configure heading
        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        rounds_wanted = self.rounds_wanted.get()

        # get round colours and median score
        self.round_colour_list, median = get_items()

        self.target_score.set(median)

        # Update heading and score to beat labels. Hide results label
        self.heading_label.config(text=f"Round {rounds_played} of {rounds_wanted}")
        self.target_label.config(text=f"Target score: {median}", font=("Arial", "14", "bold"))
        self.results_label.config(text=f"{'=' * 7}", bg="#F0F0F0")

        # Configure buttons using foreground and background colours from list
        # Enable colour buttons
        for count, item in enumerate(self.colour_button_ref):
            item.config(fg=self.round_colour_list[count][2], 
                        bg=self.round_colour_list[count][0],
                        text=self.round_colour_list[count][0], state=NORMAL)
            
        self.next_button.config(state=DISABLED)

    def round_results(self, user_choice):
        """
        Retrieves which button was pushed (index 0 - 3), retrieves score
        and then compares it with median, updates results and add results to stat list.
        """
        # Get user score and colour based on button press
        score = int(self.round_colour_list[user_choice][1])

        # alternate way to get button name. Good for if buttons have been scrambled
        colour_name = self.colour_button_ref[user_choice].cget('text')

        # Retrieve target score and compare with user score to find round result
        target = self.target_score.get()
        self.all_medians_list.append(target)

        if score >= target:
            result_text = f"Success! {colour_name} earned you {score} points"
            result_bg = "#82B366"
            self.all_scores_list.append(score)

        else:
            result_text = f"Oops {colour_name} ({score}) is less than the target"
            result_bg = "#F8CECC"
            self.all_scores_list.append(0)

        self.results_label.config(text=result_text, bg=result_bg)

        # Enable stats and next buttons, disable colour buttons
        self.next_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)

        # Check to see if game is over
        rounds_played = self.rounds_played.get()
        rounds_wanted = self.rounds_wanted.get()

        if rounds_played == rounds_wanted:
            self.next_button.config(state=DISABLED, text="Game Over")
            self.end_game_button.config(text="Play Again", bg="#006600")

        for item in self.colour_button_ref:
            item.config(state=DISABLED)


    def close_play(self):
        # reshow root (ie: choose rounds) and end current game / allow new game to start
        root.deiconify()
        self.play_box.destroy()

# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Conections")
    StartGame()
    root.mainloop()