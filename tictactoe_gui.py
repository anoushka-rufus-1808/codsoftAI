import tkinter as tk             #gui library for game window
from tkinter import messagebox   #to display messages to the user
import random

# Check if a player has won
def is_winner(board, player):
    # Check rows, columns, and diagonals ... [i][j] because tictactoe board is a 2D list
    for i in range(3):
        if all(board[i][j] == player for j in range(3)): return True      #checking all three rows have same input
        if all(board[j][i] == player for j in range(3)): return True      #checking all three coloumns have same input
    #now checking diagonals
    if all(board[i][i] == player for i in range(3)): return True
    if all(board[i][2 - i] == player for i in range(3)): return True
    return False

# Check if the board is full (draw)
def is_draw(board):
    return all(cell != " " for row in board for cell in row)

# Minimax algorithm (unbeatable AI)
def minimax(board, is_maximizing):
    if is_winner(board, "O"): return 1       #ai wins
    if is_winner(board, "X"): return -1      #player wins
    if is_draw(board): return 0              #draw

    if is_maximizing:
        best_score = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    score = minimax(board, False)
                    board[i][j] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    score = minimax(board, True)
                    board[i][j] = " "
                    best_score = min(score, best_score)
        return best_score

# Get best move using Minimax
def best_move(board):
    best_score = -float("inf")
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                score = minimax(board, False)
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

# Get a random move (for easy AI)
def random_move(board):
    empty = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    return random.choice(empty) if empty else None

# Main GUI Game Class
class TicTacToe:
    def __init__(self, root):      #__init__ sets window title, gameboard, and buttons
        self.root = root
        self.root.title("Tic-Tac-Toe AI (You = X, AI = O)")

        # Game board (3x3 grid)
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        # Dropdown for AI difficulty
        self.ai_mode = tk.StringVar(value="Unbeatable")
        dropdown = tk.OptionMenu(self.root, self.ai_mode, "Unbeatable", "Random")
        dropdown.grid(row=3, column=0, columnspan=3, sticky="we")

        # Restart button
        restart_btn = tk.Button(self.root, text="Restart Game", font=("Helvetica", 14), command=self.restart_game)
        restart_btn.grid(row=4, column=0, columnspan=3, sticky="we", pady=10)

        # Create GUI board
        self.create_board()

    # Create 3x3 buttons for the board
    def create_board(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.root, text=" ", font=("Helvetica", 32), width=5, height=2,
                                   command=lambda row=i, col=j: self.human_move(row, col))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

    # Human player move (X)
    def human_move(self, row, col):
        if self.board[row][col] == " ":
            self.board[row][col] = "X"
            self.buttons[row][col].config(text="X", state="disabled")

            if is_winner(self.board, "X"):
                self.end_game("You win!")
            elif is_draw(self.board):
                self.end_game("It's a draw!")
            else:
                # Delay AI move slightly to make it feel natural
                self.root.after(500, self.ai_move)

    # AI move (O)
    def ai_move(self):
        mode = self.ai_mode.get()
        move = best_move(self.board) if mode == "Unbeatable" else random_move(self.board)

        if move:
            row, col = move
            self.board[row][col] = "O"
            self.buttons[row][col].config(text="O", state="disabled")

            if is_winner(self.board, "O"):
                self.end_game("AI wins!")
            elif is_draw(self.board):
                self.end_game("It's a draw!")

    # Show game result and disable all buttons
    def end_game(self, result):
        messagebox.showinfo("Game Over", result)
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state="disabled")

    # Reset the game board and buttons
    def restart_game(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=" ", state="normal")

# Run the game by calling all defined functions
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()