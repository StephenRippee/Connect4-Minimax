# This file sets up the game and runs the game loop
from Board import Board
import AI_2


def human_choice(board):
    # Gets a valid slot input from the human player and returns the slot
    while True:
        try:
            slot = int(input("Choose a slot\n")) - 1
        except:
            print("Lets try that again")
            slot = -1
        if slot < 0 or slot > 6:
            print("Please choose from 1 to 7")
        elif board.check_open(slot) == 0:
            print("That slot is full. Please choose a different slot.")
        else:
            print(board.check_open(slot))
            return slot


def choice(human, board, comp_diff, letter):
    # Calls human_choice() if it is a human's turn (0) or
    # ai_choice() if it is a computers turn (!0)
    if human == 1:
        return human_choice(board)
    else:
        board_array = board.get_array()
        output = AI_2.ai_choice(board_array, comp_diff, letter)
        print("%s chooses slot %d" % (letter, output+1))
        return output


"""
Game starts here
"""

# Find mode and first player and start game
game_board = Board()  # Generates the game board
mode_one = 0  # stores if Player one is a human (1) or CPU (2)
mode_two = 0  # stores if Player two is a human (1) or CPU (2)
comp_diff_one = 0  # stores the CPU 1 difficulty
comp_diff_two = 0  # stores the CPU 2 difficulty

while mode_one != 1 and mode_one != 2:  # Determines if Player 1 is a human or CPU
    try:
        mode_one = int(input("Player 1 (X) is a:\n1: Human\n2: Computer\n"))
    except:
        print("Invalid input")
        mode_one = 0
    if mode_one != 1 and mode_one != 2:
        print("Please choose either 1 or 2")

if mode_one == 2:  # If Player 1 is a computer, this determines its difficulty
    while comp_diff_one < 1 or comp_diff_one > 7:
        try:
            comp_diff_one = int(input("Choose CPU 1 difficulty (1 - 7): "))
        except:
            print("Invalid input")
            comp_diff_one = 0
        if comp_diff_one < 1 or comp_diff_one > 7:
            print("Please choose a number from 1 to 7")

while mode_two != 1 and mode_two != 2:  # Determines if Player 2 is a human or CPU
    try:
        mode_two = int(input("Player 2 (O) is a:\n1: Human\n2: Computer\n"))
    except:
        print("Invalid input")
        mode_two = 0
    if mode_two != 1 and mode_two != 2:
        print("Please choose either 1 or 2")

if mode_two == 2:  # If Player 2 is a computer, this determines its difficulty
    while comp_diff_two < 1 or comp_diff_two > 7:
        try:
            comp_diff_two = int(input("Choose CPU 2 difficulty (1 - 7): "))
        except:
            print("Invalid input")
            comp_diff_two = 0
        if comp_diff_two < 1 or comp_diff_two > 7:
            print("Please choose a number from 1 to 7")

# Start game loop
turns = 0
while turns < 42:
    game_board.show()
    print("X's turn")
    game_board.drop(choice(mode_one, game_board, comp_diff_one, "X"), "X")
    if game_board.detect_win() != " ":
        break
    turns += 1
    game_board.show()
    print("O's turn")
    game_board.drop(choice(mode_two, game_board, comp_diff_two, "O"), "O")
    if game_board.detect_win() != " ":
        break
    turns += 1

# Game has ended
game_board.show()
if turns == 42:
    print("Its a tie!\n")
else:
    print("Player " + game_board.detect_win() + " Wins!")
