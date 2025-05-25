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

        # Strings for Labels
        intro_string = "Each round you will choose an answer which makes a connection with the 4 words given.\n"\
                        "You will also get a clue if the words can be placed before or after the answer.\n"\
                        "The more groups you get correct one after the other, the larger the combo and the more points you earn."

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
        """
        Checks users have entered 1 or more rounds
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

        self.rounds_won = IntVar()

        # Gameplay lists
        self.round_before_after_list = []
        self.round_word_list = []
        self.round_answer_list = []
        self.round_clue_list = []

        # Score lists
        self.all_scores_list = []
        self.all_high_score_list = []

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # If users press the 'x' on the game window, end the entire game
        self.play_box.protocol('WM_DELETE_WINDOW', root.destroy)

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
            [self.hints_stats_frame, "Hints", "#FF8000", self.to_hints, 10, 0, 0],
            [self.hints_stats_frame, "Stats", "#333333", self.to_stats, 10, 0, 1],
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
        self.hints_button = control_ref_list[1]
        self.stats_button = control_ref_list[2]
        self.end_game_button = control_ref_list[3]

        self.stats_button.config(state=DISABLED)

        # End game button
        self.end_game_button.config(text="End Game")

        # Once interface has been created, invoke new round function for the first round
        self.new_round()

    def new_round(self):
        """
        Chooses four answers, with one being the correct answer. 
        configures buttons with choosen answers
        """

        # reteieve number of rounds played, add one to it and configure heading
        rounds_played = self.rounds_played.get()
        self.rounds_played.set(rounds_played)

        rounds_wanted = self.rounds_wanted.get()

        # get round lists 
        self.round_before_after_list, self.round_words_list, self.round_answer_list, self.round_clue_list = get_round_results()

        # Randomly choose a number and match that number to the correct Answer, Connections, and Clues.
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
        # Enable stats button after at least one round has been played
        self.stats_button.config(state=NORMAL)

        # Add one to the number of rounds played and retrieve the number of rounds won
        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        # alternate way to get button name. Good for if buttons have been scrambled
        answer_name = self.answer_button_ref[user_choice].cget('text')

        if answer_name == self.correct_answer:
            result_text = f"Success! {answer_name} is correct, and earned you (placeholder: 10) points"
            result_bg = "#82B366"
            self.all_scores_list.append(10)

            rounds_won = self.rounds_won.get()
            rounds_won += 1
            self.rounds_won.set(rounds_won)
            self.combo += 1
            

        else:
            result_text = f"Oops! {answer_name} is incorrect, and earned you no points. The correct answer was {self.correct_answer}"
            result_bg = "#F8CECC"
            self.all_scores_list.append(0)
            self.combo = 0


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

    def to_hints(self):
        """
        Displays hints for playing game
        :return:
        """
        # check we have played at least one round so that stats button is not enabled in error
        rounds_played = self.rounds_played.get()
        DisplayHints(self, rounds_played)


    def to_stats(self):
        """
        Retrieves everything we need to display the game / round statistics
        """

        # IMPORTANT: retrieve number of rounds
        # won as a number (rather than the 'self' container)
        rounds_won = self.rounds_won.get()
        highest_combo = self.highest_combo.get()
        stats_bundle = [rounds_won, highest_combo, self.all_scores_list, self.all_high_score_list]

        Stats(self, stats_bundle)
        


# Hint and stat classes
class DisplayHints:
    """
    Displays hints for Connections game
    """

    def __init__(self, partner , rounds_played):
        self.rounds_played = rounds_played

        # setup dialouge box and background colour
        self.hint_box = Toplevel()

        # disable hint button
        partner.hints_button.config(state=DISABLED)
        partner.end_game_button.config(state=DISABLED)
        partner.stats_button.config(state=DISABLED)

        # If users press cross at top, closes hint box and releases hint button
        self.hint_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_hint, partner)) 

        self.hint_frame = Frame(self.hint_box, width=350)
        self.hint_frame.grid()

        self.hint_heading_label = Label(self.hint_frame,
                                        text= "Hint / Info",
                                        font=("Arial", "14", "bold"))
        self.hint_heading_label.grid(row=0)

        hint_text = "Each round you will choose an answer which makes a connection with the 4 words given.\n"\
                    "You will also get a clue if the words can be placed before or after the answer.\n"\
                    "The more groups you get correct, the more points you earn.\n"\
                    "Click the stats button to high scores and other info" 

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
        partner.end_game_button.config(state=NORMAL)
        
        # Only enable stats button if we have played at least one round
        if self.rounds_played >= 1:
            partner.stats_button.config(state=NORMAL)
        
        self.hint_box.destroy()


class Stats:
    """
    Displays stats for Connections game
    """

    def __init__(self, partner, all_stats_info):

        # Disable buttons to prevent program crashing
        partner.hints_button.config(state=DISABLED)
        partner.end_game_button.config(state=DISABLED)
        partner.stats_button.config(state=DISABLED)
        
        # Extract information from master list
        rounds_won = all_stats_info[0]
        highest_combo = all_stats_info[1]
        user_scores = all_stats_info[2]
        high_scores = all_stats_info[3]

        # Sort user scores to find high score
        user_scores.sort()

        # setup stats box
        self.stats_box = Toplevel()

        # disable stats button
        partner.stats_button.config(state=DISABLED)

        # If users press cross at top, closes stat box and releases stat button
        self.stats_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_stats, partner)) 

        self.stats_frame = Frame(self.stats_box, width=350)
        self.stats_frame.grid()

        # Math to populate Stats dialogue
        rounds_played = len(user_scores)

        success_rate = rounds_won / rounds_played * 100
        total_score = sum(user_scores)
        max_possible = sum(high_scores)

        best_score = user_scores[-1]
        average_score = total_score / rounds_played

        # Strings for Stats labels

        success_string = (f"Success Rate: {rounds_won} / {rounds_played}"
                          f" ({success_rate:.0f}%)")
        total_score_string = f"Total Score: {total_score}"
        max_possible_string = f"Maximum possible score: {max_possible}"
        best_score_string = f"Best score: {best_score}"

        # Custom comment text and formatting for score
        if total_score == max_possible:
            comment_string = ("Amazing! You got the highest possible score and combo!")
            comment_colour = "#D5E8D4"

        elif total_score == 0:
            comment_string = ("Oops - you've lost every round! You might want to look at the hints!")
            comment_colour = "#F8CECC"
            best_score_string = f"Best Score: n/a"

        else:
            comment_string = ""
            comment_colour = "#F0F0F0"

        average_score_string = f"Average score: {average_score:.0f}"
        highest_combo_string = f"Highest combo: {highest_combo}\n"


        heading_font = ("Arial", "16", "bold")
        normal_font = ("Arial", "14")
        comment_font = ("Arial", "13")

        # label list (text | font | 'Sticky')
        all_stats_strings = [
            ["Statistics", heading_font, ""],
            [success_string, normal_font, "W"],
            [total_score_string, normal_font, "W"],
            [max_possible_string, normal_font, "W"],
            [comment_string, comment_font, "W"],
            ["\nRound Stats", heading_font, ""],
            [best_score_string, normal_font, "W"],
            [average_score_string, normal_font, "W"],
            [highest_combo_string, normal_font, "W"]
        ]

        stats_label_ref_list = []
        for count, item in enumerate(all_stats_strings):
            self.stats_label = Label(self.stats_frame, text=item[0], font=item[1],
                                     anchor="w", justify="left",
                                     padx=30, pady=5)
            self.stats_label.grid(row=count, sticky=item[2], padx=10)
            stats_label_ref_list.append(self.stats_label)

        # Configure comment label background (for all won / all lost)
        stats_comment_label = stats_label_ref_list[4]
        stats_comment_label.config(bg=comment_colour)

        self.dismiss_button = Button(self.stats_frame,
                                     font=("Arial", "16", "bold"),
                                     text="Dismiss", bg="#333333",
                                     fg="#FFFFFF", width=20,
                                     command=partial(self.close_stats, partner))
        self.dismiss_button.grid(row=9, padx=10, pady=10)

        # Closes stat dialogue (used by button and x at the top of dialogue)

    def close_stats(self, partner):
        # Put help button back to normal
        partner.hints_button.config(state=NORMAL)
        partner.end_game_button.config(state=NORMAL)
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()



# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Connections")
    StartGame()
    root.mainloop()