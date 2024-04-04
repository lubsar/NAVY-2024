import tkinter as tk
from tkinter import filedialog, messagebox

import numpy as np
import math
import json
from copy import copy

class LsystemApp:
    def __init__(self, master):
        self.master = master

        self.create_widgets()


    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=800, height=600, bg='white')
        self.canvas.pack(side=tk.LEFT)

        left_button_frame = tk.Frame(self.master)
        left_button_frame.pack(side=tk.LEFT, padx=10)

        save_button = tk.Button(left_button_frame, text="Save preset", command=self.save_preset)
        save_button.pack(pady=5)

        load_button = tk.Button(left_button_frame, text="Load preset", command=self.load_preset)
        load_button.pack(pady=5)

        tk.Label(left_button_frame, text="Start X:").pack(pady=5)
        self.start_x_entry = tk.Entry(left_button_frame)
        self.start_x_entry.pack(pady=5)

        tk.Label(left_button_frame, text="Start Y:").pack(pady=5)
        self.start_y_entry = tk.Entry(left_button_frame)
        self.start_y_entry.pack(pady=5)

        tk.Label(left_button_frame, text="Start Angle °:").pack(pady=5)
        self.start_angle_entry = tk.Entry(left_button_frame)
        self.start_angle_entry.pack(pady=5)

        tk.Label(left_button_frame, text="Segment Length:").pack(pady=5)
        self.length_entry = tk.Entry(left_button_frame)
        self.length_entry.pack(pady=5)

        tk.Label(left_button_frame, text="Axiom:").pack(pady=5)
        self.axiom_entry = tk.Entry(left_button_frame)
        self.axiom_entry.pack(pady=5)

        tk.Label(left_button_frame, text="Rule:").pack(pady=5)
        self.rule_entry = tk.Entry(left_button_frame)
        self.rule_entry.pack(pady=5)

        tk.Label(left_button_frame, text="Depth:").pack(pady=5)
        self.depth_entry = tk.Entry(left_button_frame)
        self.depth_entry.pack(pady=5)

        tk.Label(left_button_frame, text="Angle °:").pack(pady=5)
        self.angle_entry = tk.Entry(left_button_frame)
        self.angle_entry.pack(pady=5)

        draw_bttn = tk.Button(left_button_frame, text="Draw", command=self.draw)
        draw_bttn.pack(pady=10)

        clear_bttn = tk.Button(left_button_frame, text="Clear", command=self.clear_canvas)
        clear_bttn.pack(pady=10)

    def draw(self) -> None:
        depth = int(self.depth_entry.get())

        axiom = self.axiom_entry.get().lower().strip()
        rule = self.rule_entry.get().lower().strip()
        length = float(self.length_entry.get())

        x = int(self.start_x_entry.get())
        y = int(self.start_y_entry.get())
        angle = float(self.angle_entry.get())
        init_angle = float(self.start_angle_entry.get())

        sequence = axiom

        self.clear_canvas()

        for _ in range(depth):
            sequence = sequence.replace("f", rule)

        self.drawSystem(sequence, length, angle, x, y, init_angle)

    def drawSystem(self, sequence : str, length : int, angle : int, x : int, y : int, init_angle : int) -> None:
        current_x = x
        current_y = y
        current_angle = init_angle

        stack = []

        for character in sequence:
            if character == "[":
                stack.append((current_x, current_y, current_angle))
            elif character == "]":
                current_x, current_y, current_angle = stack.pop()
            elif character == "+":
                current_angle += angle
            elif character == "-":
                current_angle -= angle
            else:
                angle_radians = math.radians(current_angle)

                end_x = current_x + length * math.cos(angle_radians)
                end_y = current_y + length * math.sin(angle_radians)

                if character == "f":
                    self.canvas.create_line(current_x, current_y, end_x, end_y)

                current_x = end_x
                current_y = end_y

    def clear_canvas(self):
        self.canvas.delete("all")
      
    def save_preset(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            settings = {
                "start_x": self.start_x_entry.get(),
                "start_y": self.start_y_entry.get(),
                "start_angle" : self.start_angle_entry.get(),
                "angle": self.angle_entry.get(),
                "length": self.length_entry.get(),
                "axiom" : self.axiom_entry.get(),
                "rule" : self.rule_entry.get(),
                "depth" : self.depth_entry.get()
            }

            with open(filename, 'w') as f:
                json.dump(settings, f)

            messagebox.showinfo("Preset Saved", "Preset has been saved successfully!")

    def load_preset(self):
        def setHelper(entry, value):
            entry.delete(0, tk.END)
            entry.insert(0, str(value))

        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])

        if filename:
            with open(filename, "r") as f:
                settings = json.load(f)

                setHelper(self.start_x_entry, settings["start_x"])
                setHelper(self.start_y_entry, settings["start_y"])
                setHelper(self.start_angle_entry, settings["start_angle"])
                setHelper(self.angle_entry, settings["angle"])
                setHelper(self.length_entry, settings["length"])
                setHelper(self.axiom_entry, settings["axiom"])
                setHelper(self.rule_entry, settings["rule"])
                setHelper(self.depth_entry, settings["depth"])


def main():
    root = tk.Tk()
    root.title("L system")
    app = LsystemApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()