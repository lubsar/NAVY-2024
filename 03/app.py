import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import hopfield as hf

import numpy as np

class GridApp:
    def __init__(self, master, grid_size):
        self.master = master
        self.grid_size = grid_size
        self.cell_size = 50
        self.grid = np.zeros((grid_size, grid_size), np.int32)
        self.current_pattern_index = 0
        self.network = hf.HopfieldNetwork(grid_size, 5)
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=self.grid_size*self.cell_size, height=self.grid_size*self.cell_size, bg='white')
        self.canvas.pack(side=tk.LEFT)

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1, y1 = j*self.cell_size, i*self.cell_size
                x2, y2 = x1+self.cell_size, y1+self.cell_size
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='black')
                self.canvas.tag_bind(rect, '<Button-1>', lambda event, i=i, j=j: self.toggle_cell(event, i, j))
        
        buttons_frame = tk.Frame(self.master)
        buttons_frame.pack(side=tk.RIGHT)

        self.clear_button = tk.Button(buttons_frame, text="Clear Grid", command=self.clear_grid)
        self.clear_button.pack(fill=tk.X, padx=5, pady=5)

        self.add_pattern_button = tk.Button(buttons_frame, text="Add Pattern", command=self.add_pattern)
        self.add_pattern_button.pack(fill=tk.X, padx=5, pady=5)

        self.remove_pattern_button = tk.Button(buttons_frame, text="Remove Pattern", command=self.remove_pattern)
        self.remove_pattern_button.pack(fill=tk.X, padx=5, pady=5)

        self.next_pattern_button = tk.Button(buttons_frame, text="Next Pattern", command=self.next_pattern)
        self.next_pattern_button.pack(fill=tk.X, padx=5, pady=5)

        self.recover_sync_button = tk.Button(buttons_frame, text="Recover Synchronously", command=self.recover_sync)
        self.recover_sync_button.pack(fill=tk.X, padx=5, pady=5)

        self.recover_async_button = tk.Button(buttons_frame, text="Recover Asynchronously", command=self.recover_async)
        self.recover_async_button.pack(fill=tk.X, padx=5, pady=5)

        self.save_network_button = tk.Button(buttons_frame, text="Save Network", command=self.save_network)
        self.save_network_button.pack(fill=tk.X, padx=5, pady=5)

        self.load_network_button = tk.Button(buttons_frame, text="Load Network", command=self.load_network)
        self.load_network_button.pack(fill=tk.X, padx=5, pady=5)

    def toggle_cell(self, event, i, j):
        if self.grid[i][j] == 0:
            self.grid[i][j] = 1
            self.canvas.itemconfig(self.canvas.find_closest(event.x, event.y), fill='black')
        else:
            self.grid[i][j] = 0
            self.canvas.itemconfig(self.canvas.find_closest(event.x, event.y), fill='white')

        self.current_pattern_index = -1

    def clear_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.grid[i][j] = 0
                self.canvas.itemconfig(self.canvas.find_all()[i * self.grid_size + j], fill='white')

    def add_pattern(self):
        pattern = hf.Pattern(self.grid)

        result = self.network.add_pattern(pattern)

        if result:
            messagebox.showinfo("Pattern Added", "Pattern added successfully!")
        else:
            messagebox.showinfo("Pattern already saved", "Pattern is already saved in network.")

    def remove_pattern(self):
        pattern = hf.Pattern(self.grid)

        result = self.network.remove_pattern(pattern)

        if result:
            messagebox.showinfo("Pattern Removed", "Pattern removed successfully!")
        else:
            messagebox.showinfo("Pattern not found", "Pattern was not found in network")

    def next_pattern(self):
        if len(self.network.patterns) == 0:
            return

        self.current_pattern_index = (self.current_pattern_index + 1) % len(self.network.patterns)
        self.update_grid_with_pattern(self.network.patterns[self.current_pattern_index])

    def update_grid_with_pattern(self, pattern : hf.Pattern):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if pattern.picture_matrix[i][j] == 1:
                    self.grid[i][j] = 1
                    self.canvas.itemconfig(self.canvas.find_all()[i * self.grid_size + j], fill='black')
                else:
                    self.grid[i][j] = 0
                    self.canvas.itemconfig(self.canvas.find_all()[i * self.grid_size + j], fill='white')

    def recover_sync(self):
        current_pattern = hf.Pattern(self.grid)

        result = self.network.synchronous_recovery(current_pattern)
        if result is None:
            messagebox.showinfo("Pattern not found", "Pattern was not found in network")
        else:
            self.update_grid_with_pattern(result)

    def recover_async(self):
        current_pattern = hf.Pattern(self.grid)

        result = self.network.asynchronous_recovery(current_pattern)
        if result is None:
            messagebox.showinfo("Pattern not found", "Pattern was not found in network")
        else:
            self.update_grid_with_pattern(result)

    def save_network(self):
        filename = filedialog.asksaveasfilename(defaultextension=".pickle", filetypes=[("Pickle files", "*.pickle")])
        if filename:
            self.network.save_network(filename)


    def load_network(self):
        filename = filedialog.askopenfilename(filetypes=[("Pickle files", "*.pickle")])
        if filename:
            self.network = hf.HopfieldNetwork.load_network(filename)
            self.current_pattern_index = 0
            self.clear_grid()

def main():
    root = tk.Tk()
    root.title("Hopfield network")
    app = GridApp(root, 5)
    root.mainloop()

if __name__ == "__main__":
    main()