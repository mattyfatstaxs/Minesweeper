import tkinter as tk
import numpy as np
import random

class Minesweeper:
    def __init__(self, width, height, num_mines):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.board = np.zeros((height, width), dtype=int)
        self.mask = np.full((height, width), False, dtype=bool)
        self.generate_mines()
        self.game_over = False

    def generate_mines(self):
        mines_placed = 0
        while mines_placed < self.num_mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.board[y][x] != -1:
                self.board[y][x] = -1
                mines_placed += 1

        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == -1:
                    continue
                count = 0
                for dx, dy in [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        count += self.board[ny][nx] == -1
                self.board[y][x] = count

    def reveal(self, x, y):
        if self.mask[y][x]:
            return
        if self.board[y][x] == -1:
            self.game_over = True
            self.mask = np.full((self.height, self.width), True, dtype=bool)
            return

        self.mask[y][x] = True

        if self.board[y][x] == 0:
            for dx, dy in [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    self.reveal(nx, ny)

    def toggle_mine_label(self, x, y):
        if not self.mask[y][x]:
            if self.board[y][x] == -1:
                self.board[y][x] = 0
            elif self.board[y][x] == 0:
                self.board[y][x] = -1

    def display(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.mask[y][x]:
                    if self.board[y][x] == -1:
                        print('*', end=' ')
                    else:
                        print(self.board[y][x], end=' ')
                else:
                    print('.', end=' ')
            print()

class MinesweeperGUI:
    def __init__(self, master):
        self.master = master
        self.master.title('Minesweeper')
        self.game = Minesweeper(10, 10, num_mines=10)
        self.buttons = [[None for _ in range(self.game.width)] for _ in range(self.game.height)]
        self.create_widgets()

    def create_widgets(self):
        for y in range(self.game.height):
            for x in range(self.game.width):
                button = tk.Button(self.master, text=' ', width=2, height=1, command=lambda x=x, y=y: self.click(x, y))
                button.grid(row=y, column=x)
                button.id = (x, y)  # add id attribute to button
                button.bind('<Button-1>', lambda event, x=x, y=y: self.left_click(event, x, y))
                button.bind('<Key-m>', lambda event, x=x, y=y: self.label_mine(event, x, y))
                self.buttons[y][x] = button


    def left_click(self, event, x, y):
        self.game.reveal(x, y)
        self.update()

    def label_mine(self, event, x, y):
        if not self.game.mask[y][x]:
            self.buttons[y][x].config(text='M')

    def update(self):
        for y in range(self.game.height):
            for x in range(self.game.width):
                if self.game.mask[y][x]:
                    if self.game.board[y][x] == -1:
                        # set text of button to 'M' if mine
                        self.buttons[y][x].config(text='M', state='disabled')
                    else:
                        self.buttons[y][x].config(text=self.game.board[y][x], state='disabled')
                else:
                    self.buttons[y][x].config(text=' ', state='normal')

        if self.game.game_over:
            for y in range(self.game.height):
                for x in range(self.game.width):
                    if self.game.board[y][x] == -1:
                        self.buttons[y][x].config(text='*', state='disabled')
                    else:
                        self.buttons[y][x].config(state='disabled')

        tk.messagebox.showinfo('Game Over', 'You lose!')


        
root = tk.Tk()
game_gui = MinesweeperGUI(root)
root.mainloop()
                                  
