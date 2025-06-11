from tkinter import *
from functools import partial  # To prevent unwanted windows
import clue_constants as c


class StartGame:
    """
    Clues tool
    """

    def __init__(self):
        """
        Clues GUI
        """

        self.game_frame = Frame(padx=10, pady=10)
        self.game_frame.grid()

        self.heading = Label(self.game_frame,
                                  text="Connections Clues",
                                  font=("Arial", "16", "bold"))
        self.heading.grid(row=0)

        # Conversion, help and history / export buttons
        self.button_frame = Frame(self.game_frame)
        self.button_frame.grid(row=4)

        # button list (button text | bg colour | command | row | column)
        button_details_list = [
            ["Clues On", "#990099", lambda: self.clue_check(c.CLUES_ON), 0, 0],
            ["Clues Off", "#009900", lambda: self.clue_check(c.CLUES_OFF), 0, 1]
        ]

        # List to hold buttons once they have been made
        self.button_ref_list = []

        # Customises the buttons
        for item in button_details_list:
            self.make_button = Button(self.button_frame,
                                      text=item[0], bg=item[1],
                                      fg="#FFFFFF", font=("Arial", "12", "bold"),
                                      width=12, command=item[2])
            self.make_button.grid(row=item[3], column=item[4], padx=5, pady=5)

            self.button_ref_list.append(self.make_button)

    def clue_check(self, clue_input):
        """
        Checks if user wants clues enabled or disabled
        """

        if clue_input == c.CLUES_OFF:
            answer = 0
        else:
            answer = 1

        Clues(self, answer)

class Clues:
    def __init__(self, partner, all_clues_info):

        # Extract if the user wanted clues on or off
        clues_on = all_clues_info

        # Print a different message depending on if the user wanted clues on or off
        if clues_on == 1:
            print("Choose the correct answer below which is placed before / after these connections: Placeholder. Clues on")
        elif clues_on == 0:
            print("Choose the correct answer below which matches these connections: Placeholder. Clues off")
        else:
            print("Error")
            

# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Connections")
    StartGame()
    root.mainloop()
