import tkinter as tk
from constants import BLOCK_SIZE, FIELD_WIDTH, FIELD_HEIGHT
from tetromino import TetrisBlock
from board import TetrisField, TetrisCanvas

class TetrisGame():
    # ...

if __name__ == "__main__":
    root = tk.Tk()
    game = TetrisGame(root)
    root.mainloop()
