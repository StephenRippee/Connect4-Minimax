# This file contains all of the AI decision making
import random

"""
BOARD FUNCTIONS (comments are currently wrong btw)
"""
# These are apparently necessary
global ai_board_array
ai_board_array = []
for blip in range(7):
    ai_board_array.append([" " for y in range(6)])


# Prints the game board
def show():
    for y in range(6):
        print("|", end='')
        for x in range(7):
            print("[" + ai_board_array[x][5 - y] + "]", end='')
        print("|")
    print("|-1--2--3--4--5--6--7-|")


# Inserts the letter into the lowest open slot possible. Insert ranges from 0 to 6 inclusive.
def drop(insert, letter):
    for i in range(6):
        if ai_board_array[insert][i] == " ":
            ai_board_array[insert][i] = letter
            break


# Removes the top letter. The inverse of drop(). Insert ranges from 0 to 6 inclusive.
def pick_up(insert):
    for i in range(6):
        if ai_board_array[insert][5 - i] != " ":
            ai_board_array[insert][5 - i] = " "
            break


# Returns 1 if this slot can be chosen, or 0 if it cannot. Slot ranges from 0 to 6 inclusive
def check_open(slot):
    if not 0 <= slot <= 6:
        return 0
    if ai_board_array[slot][5] == " ":
        return 1
    else:
        return 0


# Detects if there is a winner in the current state and returns the letter than won if there is
def detect_win():
    # Vertical
    for x in range(7):
        for y in range(3):
            if ai_board_array[x][y] != " " and ai_board_array[x][y] == ai_board_array[x][y + 1] == \
                    ai_board_array[x][y + 2] == ai_board_array[x][y + 3]:
                return ai_board_array[x][y]
    # Horizontal
    for x in range(4):
        for y in range(6):
            if ai_board_array[x][y] != " " and ai_board_array[x][y] == ai_board_array[x + 1][y] == \
                    ai_board_array[x + 2][y] == ai_board_array[x + 3][y]:
                return ai_board_array[x][y]
    # Forward Slash
    for x in range(4):
        for y in range(3):
            if ai_board_array[x][y] != " " and ai_board_array[x][y] == ai_board_array[x + 1][y + 1] == \
                    ai_board_array[x + 2][y + 2] == ai_board_array[x + 3][y + 3]:
                return ai_board_array[x][y]
    # Back Slash
    for x in range(3, 7):
        for y in range(3):
            if ai_board_array[x][y] != " " and ai_board_array[x][y] == ai_board_array[x - 1][y + 1] == \
                    ai_board_array[x - 2][y + 2] == ai_board_array[x - 3][y + 3]:
                return ai_board_array[x][y]
    return " "


"""
END OF BOARD FUNCTIONS
"""


"""
How the Process works:
This program plays minimax with Xs and Os instead of numbers
It tests every option until a win or loss, and finds which path if played perfectly by both sides
leads to a win or delays a loss the most
It can see into the future a comp_diff amount of moves
"""


# This function sets up the board, creates an array of choices, and chooses whichever leads to victory or avoids defeat
def ai_choice(input_array, comp_diff, letter):  # (game board array, computer difficulty, X or O)
    print("Calculating up to %d possibilities" % (7 ** comp_diff))
    global ai_board_array
    ai_board_array = input_array
    choices = ["f", "f", "f", "f", "f", "f", "f"]  # f stands for full. It will be overwritten if it is not full
    if letter == "O":  # Determines opponents letter
        opponent_letter = "X"
    else:
        opponent_letter = "O"

    print("Progress: ", end='')
    for x in range(7):  # first layer of recursive loop. Creates a vector of X, O, and space
        if comp_diff > 5:
            print("%d/7 " % x, end='')
        if check_open(x) == 1:
            choices[x] = ai_loop(x, letter, opponent_letter, comp_diff)
    print("Progress: 7/7")

    best = 0  # best option
    for i in range(7):
        if choices[i] != "f" and (choices[i] == letter or (choices[best] == opponent_letter and choices[i] == " ")):
            best = i
        print("Slot %d: %s | Best slot: %d" % (i+1, choices[i], best+1))

    if choices[best] == "f":  # Prevents CPU from picking a full slot when there are no good options
        for i in range(7):
            if choices[i] == " ":
                best = i
                break

    humanizer = []  # This process randomly selects equivalent best outputs, tending towards the middle
    for i in range(7):
        if choices[i] == choices[best]:
            humanizer.append(i)
    return humanizer[int(random.triangular(0, len(humanizer)))]


"""
This loop is what recursively checks each slot.
First, it drops the into the drop parameters slot.
Then it checks for a win/loss.
If it wins, it undoes that change and returns that winning letter.
If no one wins, then it switches perspectives and repeats itself for all 7 options do determine their outcomes
The bottom layer of the program selects choices in this priority:
    Winning choices
    Neutral choices
    Losing choices
and returns its choice.
The layer above it then sees the results of the 7 members of the layer below it, and makes a similar choice.
This process continues until the top layer in ai_choice returns its choice to the main program.
Note that the perspective switches each time. If one layer chooses from the perspective of X, the next will
choose from the perspective of O, the next from X, etc.
"""


def ai_loop(drop_slot, letter, opponent_letter, comp_diff):
    drop(drop_slot, letter)  # Drop's current letter into the slot

    if detect_win() != " ":  # detects if that move won
        returnable = detect_win()
        pick_up(drop_slot)  # removes the last dropped token
        return returnable
    else:  # If it didnt win,
        if comp_diff == 1:  # and if this is the last step, return " "
            pick_up(drop_slot)
            return " "
        else:  # If this isn't the last step, then dig another layer
            h = letter  # swap letter and opponent_letter
            letter = opponent_letter
            opponent_letter = h
            choices = [" ", " ", " ", " ", " ", " ", " "]
            for x in range(7):
                if check_open(x) == 1:
                    choices[x] = ai_loop(x, letter, opponent_letter, comp_diff-1)  # loops through new choices
                else:
                    choices[x] = " "  # Returns " " if no choices lead to win/loss

            for i in range(7):
                if choices[i] == letter:  # If this letter won, return that letter
                    pick_up(drop_slot)
                    return letter

            for i in range(7):
                if choices[i] == " ":  # If this letter can avoid a loss, return " "
                    pick_up(drop_slot)
                    return " "

            pick_up(drop_slot)
            return opponent_letter  # If this letter is forced to lose, return the opponent's letter
