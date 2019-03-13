# This file handles the board for non computationally heavy purposes


class Board(object):
    # Initializes the matrix that stores the letter locations
    positions = []
    for x in range(7):
        positions.append([" " for y in range(6)])

    # Prints the game board
    def show(self):
        for y in range(6):
            print("|", end='')
            for x in range(7):
                print("[" + self.positions[x][5-y] + "]", end='')
            print("|")
        print("|-1--2--3--4--5--6--7-|")

    # Inserts the letter into the lowest open slot possible. Insert ranges from 0 to 6 inclusive.
    def drop(self, insert, letter):
        for i in range(6):
            if self.positions[insert][i] == " ":
                self.positions[insert][i] = letter
                return

    # Returns 1 if this slot can be chosen, or 0 if it cannot. Slot ranges from 0 to 6 inclusive
    def check_open(self, slot):
        if not 0 <= slot <= 6:
            return 0
        if self.positions[slot][5] == " ":
            return 1
        else:
            return 0

    # Detects if there is a winner in the current state and returns the letter than won if there is
    def detect_win(self):
        # Vertical
        for x in range(7):
            for y in range(3):
                if self.positions[x][y] != " " and self.positions[x][y] == self.positions[x][y+1]\
                        == self.positions[x][y+2] == self.positions[x][y+3]:
                    return self.positions[x][y]
        # Horizontal
        for x in range(4):
            for y in range(6):
                if self.positions[x][y] != " " and self.positions[x][y] == self.positions[x+1][y]\
                        == self.positions[x+2][y] == self.positions[x+3][y]:
                    return self.positions[x][y]
        # Forward Slash
        for x in range(4):
            for y in range(3):
                if self.positions[x][y] != " " and self.positions[x][y] == self.positions[x+1][y+1]\
                        == self.positions[x+2][y+2] == self.positions[x+3][y+3]:
                    return self.positions[x][y]
        # Back Slash
        for x in range(3, 7):
            for y in range(3):
                if self.positions[x][y] != " " and self.positions[x][y] == self.positions[x-1][y+1]\
                        == self.positions[x-2][y+2] == self.positions[x-3][y+3]:
                    return self.positions[x][y]
        return " "
