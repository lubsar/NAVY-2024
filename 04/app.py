import tkinter as tk
from tkinter import filedialog, messagebox

import qlearning as ql
import numpy as np
import time 

class QLearningApp:
    def __init__(self, master, grid_size):
        self.master = master
        self.grid_size = grid_size
        self.cell_size = 32
        self.grid = [['floor' for _ in range(grid_size)] for _ in range(grid_size)]
        self.sprites = {
            'floor': tk.PhotoImage(file="floor.png"),
            'mouse': tk.PhotoImage(file="mouse.png"),
            'cat': tk.PhotoImage(file="cat.png"),
            'wall': tk.PhotoImage(file="wall.png"),
            'cheese' : tk.PhotoImage(file="cheese.png")
        }

        self.scores = {'floor' : 0, 'wall' : -1, 'cat' : -100, 'cheese' : 100, 'mouse' : 0}

        self.current_sprite = 'floor'
        self.sprite_ids = [[None for _ in range(grid_size)] for _ in range(grid_size)]
        self.create_widgets()
        self.mouse_coords = None
        self.network = None

        # self.load_map("map.txt")
        # self.train()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=self.grid_size*self.cell_size, height=self.grid_size*self.cell_size, bg='white')
        self.canvas.pack(side=tk.LEFT)

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.canvas.create_image(j*self.cell_size, i*self.cell_size, anchor=tk.NW, image=self.sprites['floor'])

        self.canvas.bind("<Button-1>", self.set_cell)

        edit_frame = tk.Frame(self.master, bd=2, relief=tk.RAISED)
        edit_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        edit_label = tk.Label(edit_frame, text="Edit")
        edit_label.pack()

        for sprite_name in self.sprites:
            sprite_button = tk.Button(edit_frame, text=sprite_name.capitalize(), command=lambda s=sprite_name: self.select_sprite(s))
            sprite_button.pack(pady=5)

        left_button_frame = tk.Frame(self.master)
        left_button_frame.pack(side=tk.LEFT)

        chase_button = tk.Button(left_button_frame, text="Chase the cheese", command=self.chase)
        chase_button.pack(pady=5, padx=5)

        train_button = tk.Button(left_button_frame, text="Train", command=self.train)
        train_button.pack(pady=5, padx=5)

        save_button = tk.Button(left_button_frame, text="Save Map", command=self.save_map)
        save_button.pack(pady=5)

        load_button = tk.Button(left_button_frame, text="Load Map", command=self.load_map)
        load_button.pack(pady=5)
        
        clear_button = tk.Button(left_button_frame, text="Clear map", command=self.clear_level)
        clear_button.pack(pady=5)

        show_bttn = tk.Button(left_button_frame, text="Show matrix", command=self.showMatrix)
        show_bttn.pack(pady=5)

    def select_sprite(self, sprite_name):
        self.current_sprite = sprite_name

    def set_cell(self, event):
        i = event.y // self.cell_size
        j = event.x // self.cell_size

        if self.sprite_ids[i][j] is not None:
            self.canvas.delete(self.sprite_ids[i][j])

        if self.current_sprite == 'mouse' and self.mouse_coords != None:
            self.canvas.delete(self.sprite_ids[self.mouse_coords[0]][self.mouse_coords[1]])
            self.mouse_coords = (i, j)

        self.grid[i][j] = self.current_sprite
        self.sprite_ids[i][j] = self.canvas.create_image(j * self.cell_size, i * self.cell_size, anchor=tk.NW, image=self.sprites[self.current_sprite])

    def train(self):
        environ = ql.EnvironmentMatrix(self.grid, self.scores)
        self.network = ql.QLearning(environ)

        self.network.train(self.mouse_coords, 1000, 0.6, False)

    def showMatrix(self):
        if not self.network:
            return

        for row in range(self.grid_size):
            for column in range(self.grid_size):
                q_matrix = self.network.q_matrix

                cell_index = row * self.grid_size + column
                
                if (row - 1) >= 0:
                    top = (row - 1) * self.grid_size + column

                    text = "{:.1f}".format(q_matrix[cell_index][top])
                    self.canvas.create_text(column * self.cell_size, row * self.cell_size, fill="blue", anchor=tk.NW, text=text)
                    
                if (row + 1) < self.grid_size:
                    bottom = (row + 1) * self.grid_size + column

                    text = "{:.1f}".format(q_matrix[cell_index][bottom])
                    self.canvas.create_text(column * self.cell_size + (self.cell_size // 2), row * self.cell_size + (self.cell_size // 2), fill="red", anchor=tk.NW, text=text)

                if (column - 1) >= 0:
                    left = cell_index - 1

                    text = "{:.1f}".format(q_matrix[cell_index][left])
                    self.canvas.create_text(column * self.cell_size, row * self.cell_size + (self.cell_size // 2), fill="green", anchor=tk.NW, text=text)

                if (column + 1) < self.grid_size:
                    right = cell_index + 1

                    text = "{:.1f}".format(q_matrix[cell_index][right])
                    self.canvas.create_text(column * self.cell_size  + (self.cell_size // 2), row * self.cell_size, fill="yellow", anchor=tk.NW, text=text)

    def chase(self):
        if self.network != None:
            self.steps = self.network.get_steps(self.mouse_coords)

            self.animation_id = self.canvas.after(300, self.next_step)
    
    def next_step(self):
        if len(self.steps) == 0:
            return

        step = self.steps[0]

        self.canvas.delete(self.sprite_ids[self.mouse_coords[0]][self.mouse_coords[1]])
        self.mouse_coords = step

        self.grid[step[0]][step[1]] = "mouse"
        self.sprite_ids[step[0]][step[1]] = self.canvas.create_image(step[1] * self.cell_size, step[0] * self.cell_size, anchor=tk.NW, image=self.sprites["mouse"])
        
        self.steps = self.steps[1:]
        self.animation_id = self.canvas.after(300, self.next_step)

    def save_map(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, 'w') as f:
                for row in self.grid:
                    f.write(' '.join(row) + '\n')
            messagebox.showinfo("Map Saved", "Map has been saved successfully!")

    def load_map(self, filename = None):
        if not filename:
            filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

        if filename:
            with open(filename, 'r') as f:
                lines = f.readlines()
                self.grid_size = len(lines)
                self.grid = [None] * self.grid_size

                for row, line in enumerate(lines):
                    line = line.strip().split()
                    for column, sprite in enumerate(line):
                        if sprite == 'mouse':
                            self.mouse_coords = (row, column)

                    self.grid[row] = line
                    self.sprite_ids = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
                    self.canvas.config(width=self.grid_size * self.cell_size, height = self.grid_size * self.cell_size)

            self.redraw_canvas()

    def redraw_canvas(self):
        self.canvas.delete("all")
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                sprite_name = self.grid[i][j]
                self.sprite_ids[i][j] = self.canvas.create_image( j *self.cell_size, i * self.cell_size, anchor=tk.NW, image=self.sprites[sprite_name])

    def clear_level(self):
        self.canvas.delete("all")
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.sprite_ids[i][j] = self.canvas.create_image(j*self.cell_size, i*self.cell_size, anchor=tk.NW, image=self.sprites["floor"])

        self.mouse_coords = None
        self.network = None

def main():
    root = tk.Tk()
    root.title("QLearning")
    app = QLearningApp(root, 5)
    root.mainloop()

if __name__ == "__main__":
    main()