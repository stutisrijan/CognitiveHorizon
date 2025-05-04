import tkinter as tk
from tkinter import messagebox
from random import choice, shuffle
from PIL import Image, ImageTk

class Level2:
    SIMPLE_WORDS = ["account", "basket", "circle", "donate", "effort", "friend", "garden", "health"]

    def __init__(self, root, canvas, next_level_callback, update_score_callback, generate_report_callback, back_to_menu_callback):
        self.root = root
        self.canvas = canvas
        self.next_level_callback = next_level_callback
        self.update_score_callback = update_score_callback
        self.generate_report_callback = generate_report_callback
        self.back_to_menu_callback = back_to_menu_callback
        self.letters = []
        self.current_question = 0
        self.max_questions = 5
        self.timer_seconds = 30
        self.timer_id = None
        self.init_ui()

    def init_ui(self):
        self.frame = tk.Frame(self.canvas, bg="white", width=600, height=400)
        self.canvas.create_window(400, 300, window=self.frame)

        self.label = tk.Label(self.frame, text="Level 2: Form a word!", font=("Arial", 14), bg="white")
        self.label.pack(pady=5)

        self.entry = tk.Entry(self.frame, font=("Arial", 14))
        self.entry.pack(pady=5)

        self.submit_button = tk.Button(self.frame, text="Submit", command=self.check_word)
        self.submit_button.pack(pady=5)

        self.back_button = tk.Button(self.frame, text="Back to Menu", command=self.back_to_menu)
        self.back_button.pack(pady=5)

        # Timer Image and Countdown
        timer_img_raw = Image.open("images/timer.png").resize((40, 40))
        self.timer_image = ImageTk.PhotoImage(timer_img_raw)
        self.canvas.create_image(20, 20, anchor=tk.NW, image=self.timer_image)
        self.timer_label = self.canvas.create_text(70, 40, text="30", font=("Arial", 20), fill="black")

        self.new_game()

    def start_timer(self):
        self.timer_seconds = 30
        self.update_timer()

    def update_timer(self):
        self.canvas.itemconfig(self.timer_label, text=str(self.timer_seconds))
        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            messagebox.showinfo("Time's up!", "Moving to next word.")
            self.current_question += 1
            self.entry.delete(0, tk.END)
            self.new_game()

    def cancel_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def new_game(self):
        self.cancel_timer()
        if self.current_question < self.max_questions:
            self.letters = list(choice(self.SIMPLE_WORDS).upper())
            shuffle(self.letters)
            self.update_letters()
            self.start_timer()
        else:
            self.generate_report_callback()
            self.next_level_callback()

    def update_letters(self):
        for widget in self.frame.winfo_children():
            if isinstance(widget, tk.Label) and widget != self.label:
                widget.destroy()

        for letter in self.letters:
            tk.Label(self.frame, text=letter, font=("Arial", 16), width=4, bg="white").pack(side=tk.LEFT, padx=5)

    def check_word(self):
        word = self.entry.get().upper()
        if set(word).issubset(set(self.letters)) and len(word) > 3:
            self.cancel_timer()
            self.update_score_callback(len(word) * 2)
            self.current_question += 1
            self.entry.delete(0, tk.END)
            self.new_game()
        else:
            messagebox.showerror("Error", "Invalid word! Try again.")

    def back_to_menu(self):
        self.cancel_timer()
        self.destroy()
        self.back_to_menu_callback()

    def destroy(self):
        self.frame.destroy()

# ===== Test Run (Standalone) =====
if __name__ == "__main__":
    def dummy_next_level():
        print("Level complete!")

    def dummy_update_score(score):
        print(f"Score updated: +{score}")

    def dummy_generate_report():
        print("Report generated.")

    def dummy_back_to_menu():
        print("Back to menu.")

    root = tk.Tk()
    root.title("Word Builder - Level 2")
    root.geometry("800x600")

    canvas = tk.Canvas(root, width=800, height=600)
    canvas.pack()

    # Load builder.webp as background
    bg_image = Image.open("images/builder.webp").resize((800, 600))
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas.create_image(0, 0, image=bg_photo, anchor=tk.NW)

    level = Level2(root, canvas, dummy_next_level, dummy_update_score, dummy_generate_report, dummy_back_to_menu)

    root.mainloop()
