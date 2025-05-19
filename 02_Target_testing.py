import csv
import random
from tkinter import *
from functools import partial  # To prevent unwanted windows

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

    # loop until we have 3 different answers of items which arent duplicates
    while len(all_results) < 3:
        potential_items = random.choice(all_items_list)

        # Get the connections and check its not a duplicate question in a previous round
        if potential_items[5] not in round_answer:
            all_results.append(potential_items)
            round_before_after.append(potential_items[0])
            round_words.append(potential_items[1])
            round_words.append(potential_items[2])
            round_words.append(potential_items[3])
            round_words.append(potential_items[4])
            round_answer.append(potential_items[5])
            round_clue.append(potential_items[6])

    return all_results, round_before_after, round_words, round_answer, round_clue


# Classes go here
class StartGame:
    def target_test_loop(self, user_choice):

        # Word and answer lists for the round
        self.all_results_list = []
        self.round_before_after_list = []
        self.round_word_list = []
        self.round_answer_list = []
        self.round_clues_list = []

        self.all_scores_list = []

        # Get round items from lists
        self.all_results_list, self.round_before_after_list, self.round_word_list, self.round_answer_list, self.round_clues_list = get_round_results()
        
        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # If users press the 'x' on the game window, end the entire game
        self.play_box.protocol('WM_DELETE_WINDOW', root.destroy)

        # body font for most labels
        body_font = ("Arial", "12")

        self.results_label = Label(self.game_frame, text="You chose, result", font=body_font,
                                    wraplength=300, justify="left")
        self.results_label.grid(row=3, pady=10, padx=10)

        # Set up answer boxes
        self.answer_frame = Frame(self.game_frame)
        self.answer_frame.grid(row=1)

        self.answer_box_ref = []

        # Create 3 answer boxes in a 3 by 1 grid and append them to be updated in the new round function
        for item in range(0, 3):
            self.answer_box = Label(self.answer_frame, font=body_font,
                                    text="Answer Box", width=21)
            self.answer_box.grid(row= item // 3, column=item % 3, padx=5, pady=5)

            self.answer_box_ref.append(self.answer_box)

        # set up word buttons
        self.word_frame = Frame(self.game_frame)
        self.word_frame.grid(row=2)

        self.word_button_ref = []

        # # Create 12 word buttons in a 4 by 3 grid
        for item in range(0, 12):
            self.word_button = Button(self.word_frame, font=body_font,
                                        text="Word button", width=15)
            
            self.word_button.grid(row=item // 4, column=item % 4, padx=5, pady=5)

            self.word_button_ref.append(self.word_button)

        # Whatever words the user clicks
        # alternate way to get button name. Good for if buttons have been scrambled
        word_group_loop = 0
        self.word_group = []

        while len(word_group_loop) < 4:
            self.word_group.append(self.word_button_ref[user_choice].cget('text'))
            word_group_loop + 1
            

        # Find if the answer is equal to target
        self.targets = (self.target1, self.target2, self.target3)
        
        # The target is equal to the 3 answers from answer list, and each answer is equal to the 4 words
        self.target1 == self.round_answer_list[0] == (self.word1, self.word2, self.word3, self.word4)
        self.target2 == self.round_answer_list[1] == (self.word5, self.word6, self.word7, self.word8) 
        self.target3 == self.round_answer_list[2] == (self.word9, self.word10, self.word11, self.word12) 

        for target in self.targets:

            # See if the user found the correct answer that matches with a target
            if self.word_group == target:
                result_text = f"Success! {user_choice} earned you (Placeholder: 10) points"
                result_bg = "#82B366"
                self.all_scores_list.append(10)

            else:
                result_text = f"Oops: {user_choice} is not the same connections as the ones you made"
                result_bg = "#F8CECC"
                self.all_scores_list.append(0)
                print(f"Total score: {self.all_scores_list} points")

        self.results_label.config(text=result_text, bg=result_bg)

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

