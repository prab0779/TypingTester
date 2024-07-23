import tkinter as tk
import time
import random

class TypingTester:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Tester")

        self.texts = {
            "easy": [
                "The quick brown fox jumps over the lazy dog.",
                "All that glitters is not gold.",
                "The early bird catches the worm."
            ],
            "medium": [
                "A journey of a thousand miles begins with a single step.",
                "To be or not to be, that is the question.",
                "In the midst of chaos, there is also opportunity."
            ],
            "hard": [
                "If you want to go fast, go alone. If you want to go far, go together.",
                "Life is 10% what happens to us and 90% how we react to it.",
                "Do not dwell in the past, do not dream of the future, concentrate the mind on the present moment."
            ]
        }
        
        self.start_time = None
        self.selected_text = ""
        self.correct_characters = 0
        self.total_characters = 0
        self.wpm = 0
        self.accuracy = 0

        self.create_widgets()
        self.setup_profile()

    def create_widgets(self):
        self.intro_label = tk.Label(self.root, text="Select difficulty and start typing:", font=("Arial", 14))
        self.intro_label.pack(pady=10)

        self.difficulty_var = tk.StringVar(value="easy")
        self.easy_button = tk.Radiobutton(self.root, text="Easy", variable=self.difficulty_var, value="easy", font=("Arial", 12))
        self.medium_button = tk.Radiobutton(self.root, text="Medium", variable=self.difficulty_var, value="medium", font=("Arial", 12))
        self.hard_button = tk.Radiobutton(self.root, text="Hard", variable=self.difficulty_var, value="hard", font=("Arial", 12))
        self.easy_button.pack()
        self.medium_button.pack()
        self.hard_button.pack()

        self.start_button = tk.Button(self.root, text="Start", command=self.start_test, font=("Arial", 12))
        self.start_button.pack(pady=10)

        self.text_display = tk.Label(self.root, text="", font=("Arial", 12), wraplength=400)
        self.text_display.pack(pady=10)

        self.entry = tk.Entry(self.root, width=60, font=("Arial", 12))
        self.entry.pack(pady=10)
        self.entry.bind("<KeyRelease>", self.update_feedback)
        self.entry.config(state='disabled')

        self.result_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.calculate_results, font=("Arial", 12))
        self.submit_button.pack(pady=10)
        self.submit_button.config(state='disabled')

        self.history_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.history_label.pack(pady=10)

    def setup_profile(self):
        self.profile = {"easy": [], "medium": [], "hard": []}

    def start_test(self):
        self.selected_text = random.choice(self.texts[self.difficulty_var.get()])
        self.text_display.config(text=self.selected_text)
        self.entry.delete(0, tk.END)
        self.entry.config(state='normal')
        self.submit_button.config(state='normal')
        self.start_time = None
        self.correct_characters = 0
        self.total_characters = len(self.selected_text)
        self.wpm = 0
        self.accuracy = 0

    def start_timer(self):
        if self.start_time is None:
            self.start_time = time.time()

    def calculate_accuracy(self, typed_text):
        correct_characters = sum(1 for tc, oc in zip(typed_text, self.selected_text) if tc == oc)
        accuracy = (correct_characters / self.total_characters) * 100
        return accuracy

    def calculate_typing_speed(self, time_taken, typed_text):
        words_typed = len(typed_text.split())
        wpm = (words_typed / time_taken) * 60
        return wpm

    def update_feedback(self, event):
        self.start_timer()
        typed_text = self.entry.get()
        self.correct_characters = sum(1 for tc, oc in zip(typed_text, self.selected_text) if tc == oc)

        elapsed_time = time.time() - self.start_time
        self.accuracy = self.calculate_accuracy(typed_text)
        self.wpm = self.calculate_typing_speed(elapsed_time, typed_text)

        self.result_label.config(text=f"Accuracy: {self.accuracy:.2f}% | Speed: {self.wpm:.2f} WPM")

    def calculate_results(self):
        if self.start_time is None:
            return

        end_time = time.time()
        time_taken = end_time - self.start_time
        typed_text = self.entry.get()
        self.accuracy = self.calculate_accuracy(typed_text)
        self.wpm = self.calculate_typing_speed(time_taken, typed_text)

        self.result_label.config(text=f"Time taken: {time_taken:.2f} seconds\nAccuracy: {self.accuracy:.2f}%\nSpeed: {self.wpm:.2f} WPM")

        # Save the result to the profile
        self.profile[self.difficulty_var.get()].append({
            "time": time_taken,
            "accuracy": self.accuracy,
            "wpm": self.wpm
        })

        self.entry.config(state='disabled')
        self.submit_button.config(state='disabled')
        self.show_history()

    def show_history(self):
        difficulty = self.difficulty_var.get()
        history = self.profile[difficulty]

        if history:
            history_text = f"History for {difficulty.capitalize()}:\n"
            for i, record in enumerate(history, 1):
                history_text += f"{i}. Time: {record['time']:.2f}s, Accuracy: {record['accuracy']:.2f}%, WPM: {record['wpm']:.2f}\n"
        else:
            history_text = f"No history for {difficulty.capitalize()}."

        self.history_label.config(text=history_text)

def main():
    root = tk.Tk()
    app = TypingTester(root)
    root.mainloop()

if __name__ == "__main__":
    main()
