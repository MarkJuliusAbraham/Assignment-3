# CMPUT 455 Assignment 3 starter code
# Implement the specified commands to complete the assignment

import sys
import random
import os


class CommandInterface:

    def __init__(self):
        # Define the string to function command mapping
        self.command_dict = {
            "help": self.help,
            "game": self.game,
            "show": self.show,
            "play": self.play,
            "legal": self.legal,
            "genmove": self.genmove,
            "winner": self.winner,
            "loadpatterns": self.loadpatterns,
            "policy_moves": self.policy_moves
        }
        self.board = [[None]]
        self.player = 1
        self.patterns = {}

    # ===============================================================================================
    # VVVVVVVVVV START of PREDEFINED FUNCTIONS. DO NOT MODIFY. VVVVVVVVVV
    # ===============================================================================================

    def process_command(self, str):
        str = str.lower().strip()
        command = str.split(" ")[0]
        args = [x for x in str.split(" ")[1:] if len(x) > 0]
        if command not in self.command_dict:
            print("? Unknown command.\nType 'help' to list known commands.", file=sys.stderr)
            print("= -1\n")
            return False
        try:
            return self.command_dict[command](args)
        except Exception as e:
            print("Command '" + str + "' failed with exception:", file=sys.stderr)
            print(e, file=sys.stderr)
            print("= -1\n")
            return False

    def main_loop(self):
        while True:
            str = input()
            if str.split(" ")[0] == "exit":
                print("= 1\n")
                return True
            if self.process_command(str):
                print("= 1\n")

    def arg_check(self, args, template):
        converted_args = []
        if len(args) < len(template.split(" ")):
            print("Not enough arguments.\nExpected arguments:", template, file=sys.stderr)
            print("Received arguments: ", end="", file=sys.stderr)
            for a in args:
                print(a, end=" ", file=sys.stderr)
            print(file=sys.stderr)
            return False
        for i, arg in enumerate(args):
            try:
                converted_args.append(int(arg))
            except ValueError:
                print("Argument '" + arg + "' cannot be interpreted as a number.\nExpected arguments:", template,
                      file=sys.stderr)
                return False
        args = converted_args
        return True

    def help(self, args):
        for command in self.command_dict:
            if command != "help":
                print(command)
        print("exit")
        return True

    # ===============================================================================================
    # ɅɅɅɅɅɅɅɅɅɅ END OF PREDEFINED FUNCTIONS. ɅɅɅɅɅɅɅɅɅɅ
    # ===============================================================================================

    # ===============================================================================================
    # VVVVVVVVVV START OF ASSIGNMENT 3 FUNCTIONS. ADD/REMOVE/MODIFY AS NEEDED. VVVVVVVV
    # ===============================================================================================

    def game(self, args):
        if not self.arg_check(args, "n m"):
            return False
        n, m = [int(x) for x in args]
        if n < 0 or m < 0:
            print("Invalid board size:", n, m, file=sys.stderr)
            return False

        self.board = []
        for i in range(m):
            self.board.append([None] * n)
        self.player = 1
        return True

    def show(self, args):
        for row in self.board:
            for x in row:
                if x is None:
                    print(".", end="")
                else:
                    print(x, end="")
            print()
        return True

    def is_legal_reason(self, x, y, num):
        if self.board[y][x] is not None:
            return False, "occupied"

        consecutive = 0
        count = 0
        self.board[y][x] = num
        for row in range(len(self.board)):
            if self.board[row][x] == num:
                count += 1
                consecutive += 1
                if consecutive >= 3:
                    self.board[y][x] = None
                    return False, "three in a row"
            else:
                consecutive = 0
        too_many = count > len(self.board) // 2 + len(self.board) % 2

        consecutive = 0
        count = 0
        for col in range(len(self.board[0])):
            if self.board[y][col] == num:
                count += 1
                consecutive += 1
                if consecutive >= 3:
                    self.board[y][x] = None
                    return False, "three in a row"
            else:
                consecutive = 0
        if too_many or count > len(self.board[0]) // 2 + len(self.board[0]) % 2:
            self.board[y][x] = None
            return False, "too many " + str(num)

        self.board[y][x] = None
        return True, ""

    def is_legal(self, x, y, num):
        if self.board[y][x] is not None:
            return False

        consecutive = 0
        count = 0
        self.board[y][x] = num
        for row in range(len(self.board)):
            if self.board[row][x] == num:
                count += 1
                consecutive += 1
                if consecutive >= 3:
                    self.board[y][x] = None
                    return False
            else:
                consecutive = 0
        if count > len(self.board) // 2 + len(self.board) % 2:
            self.board[y][x] = None
            return False

        consecutive = 0
        count = 0
        for col in range(len(self.board[0])):
            if self.board[y][col] == num:
                count += 1
                consecutive += 1
                if consecutive >= 3:
                    self.board[y][x] = None
                    return False
            else:
                consecutive = 0
        if count > len(self.board[0]) // 2 + len(self.board[0]) % 2:
            self.board[y][x] = None
            return False

        self.board[y][x] = None
        return True

    def valid_move(self, x, y, num):
        return x >= 0 and x < len(self.board[0]) and \
            y >= 0 and y < len(self.board) and \
            (num == 0 or num == 1) and \
            self.is_legal(x, y, num)

    def play(self, args):
        if len(args) != 3:
            print("= illegal move: " + " ".join(args) + " wrong number of arguments\n")
            return False
        try:
            x = int(args[0])
            y = int(args[1])
        except ValueError:
            print("= illegal move: " + " ".join(args) + " wrong coordinate\n")
            return False
        if x < 0 or x >= len(self.board[0]) or y < 0 or y >= len(self.board):
            print("= illegal move: " + " ".join(args) + " wrong coordinate\n")
            return False
        if args[2] != '0' and args[2] != '1':
            print("= illegal move: " + " ".join(args) + " wrong number\n")
            return False
        num = int(args[2])
        legal, reason = self.is_legal_reason(x, y, num)
        if not legal:
            print("= illegal move: " + " ".join(args) + " " + reason + "\n")
            return False
        self.board[y][x] = num
        self.player = 2 if self.player == 1 else 1
        return True

    def legal(self, args):
        if not self.arg_check(args, "x y number"):
            return False
        x, y, num = [int(x) for x in args]
        if self.valid_move(x, y, num):
            print("yes")
        else:
            print("no")
        return True

    def get_legal_moves(self):
        moves = []
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                for num in range(2):
                    if self.is_legal(x, y, num):
                        moves.append([str(x), str(y), str(num)])
        return moves

    def genmove(self, args):
        moves = self.get_legal_moves()
        if len(moves) == 0:
            print("resign")
        else:
            rand_move = moves[random.randint(0, len(moves) - 1)]
            self.play(rand_move)
            print(" ".join(rand_move))
        return True

    def winner(self, args):
        if len(self.get_legal_moves()) == 0:
            print(2 if self.player == 1 else 1)
        else:
            print("unfinished")
        return True

    # New function for loading patterns
    def loadpatterns(self, args):
        self.patterns.clear()
        try:
            with open(args[0], 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue  # Skip empty lines and comments
                    pattern, move, weight = line.split()
                    move, weight = int(move), int(weight)
                    if pattern not in self.patterns:
                        self.patterns[pattern] = {}
                    self.patterns[pattern][move] = weight
        except FileNotFoundError:
            print("Pattern file not found", file=sys.stderr)
            return False
        return True

    # Function to calculate policy moves with probabilities
    def policy_moves(self, args):
        legal_moves = self.get_legal_moves()
        move_weights = []
        total_weight = 0

        for move in legal_moves:
            x, y, num = int(move[0]), int(move[1]), int(move[2])

            # Generate row and column patterns
            row_pattern = self.make_pattern(x, y, axis=0)  # Row pattern
            col_pattern = self.make_pattern(x, y, axis=1)  # Column pattern

            # Get weights for row and column patterns, or default weight of 10
            row_weight = self.patterns.get(row_pattern, {}).get(num, 10)
            col_weight = self.patterns.get(col_pattern, {}).get(num, 10)

            # Calculate the total weight for the move
            move_weight = row_weight + col_weight
            move_weights.append((move, move_weight))
            total_weight += move_weight

        # Generate output with probabilities
        result = "= "
        for move, weight in sorted(move_weights):
            probability = round(weight / total_weight, 3)
            result += f"{' '.join(move)} {probability} "
        print(result.strip())
        return True

    def make_pattern(self, x, y, axis=0):
        pattern = ""
        for i in range(-2, 3):
            nx, ny = (x + i, y) if axis == 0 else (x, y + i)
            if nx < 0 or ny < 0 or nx >= len(self.board[0]) or ny >= len(self.board):
                pattern += "X"  # Off the board
            else:
                cell = self.board[ny][nx]
                pattern += str(cell) if cell is not None else "."
        return pattern


# ===============================================================================================
# ɅɅɅɅɅɅɅɅɅɅ END OF ASSIGNMENT 3 FUNCTIONS. ɅɅɅɅɅɅɅɅɅɅ
# ===============================================================================================

if __name__ == "__main__":
    interface = CommandInterface()
    interface.main_loop()
