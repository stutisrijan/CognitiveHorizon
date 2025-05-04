import tkinter as tk
import random
from PIL import Image, ImageTk

class ColorTrailsLevel1:
    def __init__(self, root, return_to_main_callback):
        self.root = root
        self.return_to_main_callback = return_to_main_callback
        self.sequence = []
        self.player_sequence = []
        self.colors = ["red", "blue", "green", "yellow"]
        self.buttons = {}
        self.timer_seconds = 10
        self.timer_running = False

        self.setup_ui()
        self.new_level()

    def setup_ui(self):
        self.root.geometry("800x600")
        self.root.title("Color Trails Level 1")

        # Load background
        bg_image = Image.open("images/background.png")
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Timer Icon
        timer_img = Image.open("images/timer.png").resize((30, 30))
        self.timer_icon = ImageTk.PhotoImage(timer_img)
        self.timer_icon_label = tk.Label(self.root, image=self.timer_icon, bg="white")
        self.timer_icon_label.place(x=20, y=10)

        # Timer Text
        self.timer_label = tk.Label(self.root, text="10s", font=("Arial", 14, "bold"), bg="white")
        self.timer_label.place(x=60, y=10)

        # Exit Button
        self.exit_button = tk.Button(self.root, text="Exit", command=self.return_to_main, bg="red", fg="white")
        self.exit_button.place(x=730, y=10)

        # Status Label
        self.status_label = tk.Label(self.root, text="Watch the sequence!", font=("Arial", 16, "bold"), bg="white")
        self.status_label.place(relx=0.5, rely=0.15, anchor="center")

        # Color Buttons
        for i, color in enumerate(self.colors):
            btn = tk.Button(self.root, bg=color, width=10, height=4, command=lambda c=color: self.player_select(c))
            btn.place(x=150 + i * 120, y=250)
            self.buttons[color] = btn

        # Back to Main Menu
        self.main_menu_button = tk.Button(self.root, text="Main Menu", command=self.return_to_main, bg="blue", fg="white")
        self.main_menu_button.place(relx=0.5, y=500, anchor="center")

    def flash_color(self, color):
        btn = self.buttons[color]
        original_color = btn["bg"]
        btn.config(bg="white")
        self.root.after(400, lambda: btn.config(bg=original_color))

    def show_sequence(self):
        self.status_label.config(text="Watch the sequence!")
        self.timer_running = False
        for i, color in enumerate(self.sequence):
            self.root.after(1000 * i, lambda c=color: self.flash_color(c))
        self.root.after(1000 * len(self.sequence), self.start_timer)

    def new_level(self):
        self.sequence.append(random.choice(self.colors))
        self.player_sequence = []
        self.show_sequence()

    def player_select(self, color):
        if not self.timer_running or len(self.player_sequence) >= len(self.sequence):
            return
        self.player_sequence.append(color)
        self.flash_color(color)

        if self.player_sequence == self.sequence[:len(self.player_sequence)]:
            if len(self.player_sequence) == len(self.sequence):
                self.status_label.config(text="Correct! Starting next level...")
                self.timer_running = False
                self.root.after(1000, self.new_level)
        else:
            self.status_label.config(text="Wrong! Try again.")
            self.timer_running = False
            self.root.after(1000, self.reset_level)

    def start_timer(self):
        self.status_label.config(text="Your turn!")
        self.timer_seconds = 10
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if not self.timer_running:
            return
        self.timer_label.config(text=f"{self.timer_seconds}s")
        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.timer_running = False
            self.status_label.config(text="Time's up! Try again.")
            self.root.after(1000, self.reset_level)

    def reset_level(self):
        self.player_sequence = []
        self.show_sequence()

    def return_to_main(self):
        self.timer_running = False
        self.return_to_main_callback()
