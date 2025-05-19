import csv
import random
from tkinter import *
from functools import partial  # To prevent unwanted windows

# helper functions go here
# Functions go here
def get_items():
    """
    Retrieves items from csv file in CSV folder in project folder
    Return: list of results where each list item has the correct name.
    """

    # Retrieve words from csv file and put them in a list
    file = open("03_Connections/Csv/connections_quiz.csv", "r")
    all_items = list(csv.reader(file, delimiter=","))
    file.close()

    # remove the first row of headings
    all_items.pop(0)

    return all_items

def get_round_results():

    all_items_list = get_items()

    # Create lists to append items into
    all_results = []
    round_words = []
    round_before_after = []
    round_answer = []
    round_clue = []

    # loop until we have 4 different answers of items which arent duplicates
    while len(all_results) < 4:
        potential_items = random.choice(all_items_list)

        # Get the connections csv variables and check its not a duplicate question in a previous round
        if potential_items[5] not in round_answer:
            all_results.append(potential_items)
            round_before_after.append(potential_items[0])
            round_words.append(potential_items[1])
            round_words.append(potential_items[2])
            round_words.append(potential_items[3])
            round_words.append(potential_items[4])
            round_answer.append(potential_items[5])
            round_clue.append(potential_items[6])

    return round_before_after, round_words, round_answer, round_clue


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

        # Rounds played - start with 0
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        # Gameplay lists
        self.round_before_after_list = []
        self.round_word_list = []
        self.round_answer_list = []
        self.round_clue_list = []

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # body font for most labels
        body_font = ("Arial", "12")
        heading_font = ("Arial", "16", "bold")

        # List for label details (text | font | background | row)
        play_labels_list = [
            ["Round # of #", heading_font, None, 0],
            ["Choose the correct answer below which matches these connections: #, #, #, #. Good luck", body_font, "#D5E8D4", 2],
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
        self.connection_label = play_labels_ref[1]
        self.results_label = play_labels_ref[2]

        # set up answer buttons
        self.answer_frame = Frame(self.game_frame)
        self.answer_frame.grid(row=3)

        self.answer_button_ref = []

        # Create 4 answer buttons in a 2 by 2 grid
        for item in range(0, 4):
            self.answer_button = Button(self.answer_frame, font=body_font,
                                        text="Answer Name", width=15,
                                        command=partial(self.round_results, item))
            self.answer_button.grid(row=item // 2,
                                    column=item % 2,
                                    padx=5, pady=5)
            
            self.answer_button_ref.append(self.answer_button)
            
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
                                         command=item[3], font=heading_font,
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
        Chooses four answers, with one being the correct answer. 
        configures buttons with choosen answers
        """

        # reteieve number of rounds played, add one to it and configure heading
        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        rounds_wanted = self.rounds_wanted.get()

        # get round lists 
        self.round_before_after_list, self.round_words_list, self.round_answer_list, self.round_clue_list = get_round_results()

        # Randomly choose a number
        number_list = [1, 2, 3, 4]
        number = random.choice(number_list)

        if number == 1:
            self.correct_answer = self.round_answer_list[0]
            word1 = self.round_words_list[0]
            word2 = self.round_words_list[1]
            word3 = self.round_words_list[2]
            word4 = self.round_words_list[3]
            round_clue = self.round_clue_list[0]
            round_before_after = self.round_before_after_list[0]

        elif number == 2:
            self.correct_answer = self.round_answer_list[1]
            word1 = self.round_words_list[4]
            word2 = self.round_words_list[5]
            word3 = self.round_words_list[6]
            word4 = self.round_words_list[7]
            round_clue = self.round_clue_list[1]
            round_before_after = self.round_before_after_list[1]

        elif number == 3:
            self.correct_answer = self.round_answer_list[2]
            word1 = self.round_words_list[8]
            word2 = self.round_words_list[9]
            word3 = self.round_words_list[10]
            word4 = self.round_words_list[11]
            round_clue = self.round_clue_list[2]
            round_before_after = self.round_before_after_list[2]

        elif number == 4:
            self.correct_answer = self.round_answer_list[3]
            word1 = self.round_words_list[12]
            word2 = self.round_words_list[13]
            word3 = self.round_words_list[14]
            word4 = self.round_words_list[15]
            round_clue = self.round_clue_list[3]
            round_before_after = self.round_before_after_list[3]

        # Update heading and score to beat labels. Hide results label
        self.heading_label.config(text=f"Round {rounds_played} of {rounds_wanted}")
        self.connection_label.config(text=f"Choose the correct answer below which is placed {round_before_after} these connections: {word1}, {word2}, {word3}, {word4}. Clue: {round_clue}")
        self.results_label.config(text=f"{'=' * 7}", bg="#F0F0F0")

        # Configure buttons using foreground and background answers from list
        # Enable answer buttons
        for count, item in enumerate(self.answer_button_ref):
            item.config(text=self.round_answer_list[count], state=NORMAL)
            
        self.next_button.config(state=DISABLED)

    def round_results(self, user_choice):
        """
        Retrieves which button was pushed (index 0 - 4), retrieves the correct answer
        and then compares it with the answer button that the user clicks, updates results.
        """

        # alternate way to get button name. Good for if buttons have been scrambled
        answer_name = self.answer_button_ref[user_choice].cget('text')

        if answer_name == self.correct_answer:
            result_text = f"Success! {answer_name} is correct, and earned you (placeholder) points"
            result_bg = "#82B366"
            # self.all_scores_list.append(score)

        else:
            result_text = f"Oops! {answer_name} is incorrect, and earned you no points. The correct answer was {self.correct_answer}"
            result_bg = "#F8CECC"
            # self.all_scores_list.append(0)

        self.results_label.config(text=result_text, bg=result_bg)

        # Enable stats and next buttons, disable  buttons
        self.next_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)

        # Check to see if game is over
        rounds_played = self.rounds_played.get()
        rounds_wanted = self.rounds_wanted.get()

        if rounds_played == rounds_wanted:
            self.next_button.config(state=DISABLED, text="Game Over")
            self.end_game_button.config(text="Play Again", bg="#006600")

        for item in self.answer_button_ref:
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