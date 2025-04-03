from tkinter import *
from functools import partial  # To prevent unwanted windows

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
    Interface for playing the Colour Quest Game
    """

    def __init__(self, how_many):
        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # body font for most labels
        body_font = ("Arial", "12")

        # List for label details (text | font | background | row)
        play_labels_list = [
            ["Round # of #", ("Arial", "16", "bold"), None, 0],
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

        # Create 3 group button
        for item in range(0, 2):
            self.group_button = Button(self.group_frame, font=body_font,
                                       text="Group Name", width=18)
            self.group_frame.grid(row= item // 3, column=item % 3, padx=5, pady=5)

        # set up word buttons
        self.word_frame = Frame(self.game_frame)
        self.word_frame.grid(row=4)

        # Create 12 buttons in a 4 by 3 grid
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