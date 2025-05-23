from tkinter import *
from functools import partial  # To prevent unwanted windows

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
                       "The more groups you get correct, the more points you earn.\n"\

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

        # Retrieve temperature to be converted
        rounds_wanted = 6
        self.to_play(rounds_wanted)

    def to_play(self, num_rounds):
        """
        Invokes Game GUI and takes across number of rounds to be played
        """
        Play(num_rounds)
        # Hide root window (hide rounds choice window)
        root.withdraw()

class Play:
    """
    Interface for playing the Conections Game
    """

    def __init__(self, how_many):
        self.rounds_won = IntVar()
        self.highest_combo = IntVar()

        # Lists for stats component
        # Random score test data
        self.all_scores_list = [10, 12, 14, 0, 10, 0]
        self.all_high_score_list = [10, 12, 14, 16, 18, 20]
        self.rounds_won.set(4)
        self.highest_combo.set(3)
        
        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.heading_label = Label(self.game_frame, text="Conections", font=("Arial", "16", "bold"),
                                   padx=5, pady=5)
        self.heading_label.grid(row=0)

        self.stats_button = Button(self.game_frame, font=("Arial", "14", "bold"),
                                   text="Stats", width=15, fg="#FFFFFF",
                                   bg="#FF8000", padx=10, pady=10, command=self.to_stats)
        self.stats_button.grid(row=1)


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
        

class Stats:
    """
    Displays stats for Connections game
    """

    def __init__(self, partner, all_stats_info):
        
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
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Conections")
    StartGame()
    root.mainloop()