import csv
import random

# Retrieve words from csv file and put them in a list
file = open("03_Connections/Csv/connections_quiz.csv", "r")
all_items = list(csv.reader(file, delimiter=","))
file.close()

# remove the first row of headings
all_items.pop(0)

# Create lists to append items into
all_results = []
all_words = []
before_after = []
answer = []
clue = []

# loop until we have four colours with different scores
while len(all_results) < 3:
    potential_items = random.choice(all_items)

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

# Print Results
print("Connections with csv file")
print()
print("All Results:", all_results)
print()
print("Before or after:", before_after)
print("All words:", all_words)
print("Answer:", answer)
print("Clue:", clue)