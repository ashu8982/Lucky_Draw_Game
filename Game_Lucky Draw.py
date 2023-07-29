#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk
import math
import random

class LuckyDrawSpinner:
    def __init__(self, root):
        self.root = root
        self.root.title("Lucky Draw Spinner")
        self.root.geometry("400x400")

        self.canvas = tk.Canvas(root, width=300, height=300)
        self.canvas.pack()

        self.start_button = tk.Button(root, text="Start", command=self.start_spinning)
        self.start_button.pack()

        self.prizes = ["Prize 1", "Prize 2", "Prize 3", "Prize 4", "Prize 5", "Prize 6", "Prize 7", "Prize 8", "Prize 9", "Prize 10"]
        self.angle = 0
        self.is_spinning = False
        self.spin_duration = 5  # in seconds
        self.max_speed = 40
        self.current_speed = 0
        self.pointer = None
        self.pointer_length = 50

        self.spinner_sections = []
        self.create_spinner()
        self.create_pointer()

        self.root.mainloop()

    def create_spinner(self):
        angle_range = 360 / len(self.prizes)
        for i, prize in enumerate(self.prizes):
            start_angle = i * angle_range
            end_angle = (i + 1) * angle_range
            color = self.random_color()
            self.spinner_sections.append(self.canvas.create_arc(50, 50, 250, 250, start=start_angle, extent=angle_range, fill=color, outline='black'))
            self.display_prize_on_section(start_angle, end_angle, prize)

    def display_prize_on_section(self, start_angle, end_angle, prize):
        center_angle = (start_angle + end_angle) / 2
        angle_rad = math.radians(center_angle)
        x = 150 + 120 * math.cos(angle_rad)
        y = 150 - 120 * math.sin(angle_rad)
        self.canvas.create_text(x, y, text=prize, font=("Arial", 8), fill="black")

    def random_color(self):
        return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def create_pointer(self):
        self.pointer = self.canvas.create_line(150, 150, 150, 150 - self.pointer_length, width=3, fill="red")

    def spin(self):
        if self.is_spinning:
            self.angle += self.current_speed
            self.angle %= 360
            self.rotate_pointer()
            self.canvas.delete("all")
            self.create_spinner()
            self.canvas.after(50, self.spin)  # Call the spin() method again after 50 milliseconds

    def rotate_pointer(self):
        angle_rad = math.radians(self.angle)
        x1 = 150
        y1 = 150
        x2 = 150 + self.pointer_length * math.cos(angle_rad)
        y2 = 150 - self.pointer_length * math.sin(angle_rad)
        self.canvas.coords(self.pointer, x1, y1, x2, y2)

    def start_spinning(self):
        if not self.is_spinning:
            self.is_spinning = True
            self.current_speed = 1
            self.spin_accelerate()

            # Call spin() initially after clicking the Start button
            self.spin()

    def spin_accelerate(self):
        if self.current_speed < self.max_speed:
            self.current_speed += 2
            self.canvas.after(100, self.spin_accelerate)
        else:
            self.spin_slowdown()

    def spin_slowdown(self):
        if self.current_speed > 1:
            self.current_speed -= 2
            self.canvas.after(100, self.spin_slowdown)
        else:
            self.stop_spinning()

    def stop_spinning(self):
        self.is_spinning = False
        self.get_result()

    def get_result(self):
        angle_range = 360 / len(self.prizes)
        prize_index = int((self.angle + angle_range / 2) % 360 // angle_range)
        result = self.prizes[prize_index]
        self.show_celebration_popup(result)

    def show_celebration_popup(self, prize):
        celebration_message = f"Congratulations! You won {prize} 🎉🎊🥳"
        popup_window = tk.Toplevel(self.root)
        popup_window.title("Celebration!")
        popup_window.geometry("200x100")
        
        celebration_label = tk.Label(popup_window, text=celebration_message, font=("Arial", 15))
        celebration_label.pack(pady=10)

        # Display ASCII art of crackers
        crackers_art = """
               ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
             ~     ~             ~     ~
           ~         ~         ~         ~
          ~           ~       ~           ~
          ~             ~   ~             ~
          ~              ~              ~
           ~                           ~
             ~                       ~
               ~                   ~
                 ~               ~
                   ~           ~
                     ~       ~
                       ~   ~
                         ~
        """
        crackers_label = tk.Label(popup_window, text=crackers_art, font=("Arial", 15))
        crackers_label.pack()

        popup_window.after(5000, popup_window.destroy)  # Close the popup after 5 seconds

if __name__ == "__main__":
    root = tk.Tk()
    app = LuckyDrawSpinner(root)

