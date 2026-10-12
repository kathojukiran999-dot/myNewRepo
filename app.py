import tkinter as tk
from tkinter import messagebox
import random

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.geometry("450x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")

        # Game variables
        self.secret_number = 0
        self.attempts = 0
        self.max_attempts = 7
        self.game_over = False

        # Build the UI
        self.create_widgets()
        self.start_new_game()

    def create_widgets(self):
        # Title
        title = tk.Label(
            self.root,
            text="🎯 Number Guessing Game",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        title.pack(pady=15)

        # Instruction
        self.instruction = tk.Label(
            self.root,
            text="Guess a number between 1 and 100",
            font=("Arial", 12),
            bg="#2c3e50",
            fg="#bdc3c7"
        )
        self.instruction.pack()

        # Attempts counter
        self.attempts_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 12, "bold"),
            bg="#2c3e50",
            fg="#f39c12"
        )
        self.attempts_label.pack(pady=10)

        # Feedback message
        self.feedback_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 14, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1",
            wraplength=400,
            height=2
        )
        self.feedback_label.pack(pady=10)

        # Entry field
        self.guess_entry = tk.Entry(
            self.root,
            font=("Arial", 16),
            justify="center",
            width=10,
            bd=3,
            relief="solid"
        )
        self.guess_entry.pack(pady=10)
        self.guess_entry.bind("<Return>", lambda event: self.check_guess())

        # Guess button
        self.guess_button = tk.Button(
            self.root,
            text="Guess",
            font=("Arial", 13, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            width=15,
            bd=0,
            cursor="hand2",
            command=self.check_guess
        )
        self.guess_button.pack(pady=10)

        # Hint button
        self.hint_button = tk.Button(
            self.root,
            text="💡 Hint",
            font=("Arial", 11),
            bg="#9b59b6",
            fg="white",
            activebackground="#8e44ad",
            activeforeground="white",
            width=15,
            bd=0,
            cursor="hand2",
            command=self.show_hint
        )
        self.hint_button.pack(pady=5)

        # New game button
        self.new_game_button = tk.Button(
            self.root,
            text="🔄 New Game",
            font=("Arial", 11),
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            activeforeground="white",
            width=15,
            bd=0,
            cursor="hand2",
            command=self.start_new_game
        )
        self.new_game_button.pack(pady=5)

        # History display
        self.history_label = tk.Label(
            self.root,
            text="History: ",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#95a5a6",
            wraplength=420,
            justify="center"
        )
        self.history_label.pack(pady=10)

    def start_new_game(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.game_over = False
        self.guesses_history = []

        self.feedback_label.config(text="New game started! Make your guess.", fg="#ecf0f1")
        self.update_attempts_label()
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.config(state="normal")
        self.guess_button.config(state="normal")
        self.hint_button.config(state="normal")
        self.history_label.config(text="History: ")
        self.guess_entry.focus_set()

    def update_attempts_label(self):
        remaining = self.max_attempts - self.attempts
        self.attempts_label.config(
            text=f"Attempts: {self.attempts} / {self.max_attempts}   |   Remaining: {remaining}"
        )

    def check_guess(self):
        if self.game_over:
            return

        # Get and validate input
        guess_text = self.guess_entry.get().strip()

        if not guess_text:
            self.feedback_label.config(text="⚠️ Please enter a number!", fg="#e74c3c")
            return

        try:
            guess = int(guess_text)
        except ValueError:
            self.feedback_label.config(text="⚠️ Invalid input! Enter a whole number.", fg="#e74c3c")
            self.guess_entry.delete(0, tk.END)
            return

        if guess < 1 or guess > 100:
            self.feedback_label.config(text="⚠️ Number must be between 1 and 100.", fg="#e74c3c")
            self.guess_entry.delete(0, tk.END)
            return

        # Valid guess
        self.attempts += 1
        self.guesses_history.append(guess)
        self.update_attempts_label()

        # Update history display
        self.history_label.config(text="History: " + ", ".join(str(g) for g in self.guesses_history))

        # Check the guess
        if guess == self.secret_number:
            self.feedback_label.config(
                text=f"🎉 Correct! You got it in {self.attempts} attempts!",
                fg="#2ecc71"
            )
            self.end_game(won=True)
        elif guess < self.secret_number:
            self.feedback_label.config(text="📈 Too low! Try a higher number.", fg="#f39c12")
        else:
            self.feedback_label.config(text="📉 Too high! Try a lower number.", fg="#f39c12")

        # Check if out of attempts
        if self.attempts >= self.max_attempts and guess != self.secret_number:
            self.feedback_label.config(
                text=f"😢 Game Over! The number was {self.secret_number}.",
                fg="#e74c3c"
            )
            self.end_game(won=False)

        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus_set()

    def show_hint(self):
        if self.game_over:
            return

        if self.attempts == 0:
            messagebox.showinfo("Hint", "Make at least one guess first to get a hint!")
            return

        # Give hint based on last guess
        last_guess = self.guesses_history[-1]
        diff = abs(self.secret_number - last_guess)

        if diff <= 5:
            hint = "🔥 You're VERY close! (within 5)"
        elif diff <= 10:
            hint = "♨️ You're getting warm! (within 10)"
        elif diff <= 20:
            hint = "🌡️ Getting warmer... (within 20)"
        else:
            hint = "❄️ Still cold... (more than 20 away)"

        messagebox.showinfo("💡 Hint", hint)

    def end_game(self, won):
        self.game_over = True
        self.guess_entry.config(state="disabled")
        self.guess_button.config(state="disabled")
        self.hint_button.config(state="disabled")

        if won:
            messagebox.showinfo("🎉 You Won!", f"Congratulations!\nYou guessed it in {self.attempts} attempts!")
        else:
            messagebox.showinfo("😢 Game Over", f"Better luck next time!\nThe number was {self.secret_number}.")


# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGuessingGame(root)
    root.mainloop()
