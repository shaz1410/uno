import tkinter as tk
from tkinter import messagebox
import random


# ------------------ CARD ------------------ #
class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __str__(self):
        return f"{self.color} {self.value}"


# ------------------ DECK ------------------ #
class Deck:
    def __init__(self):
        self.cards = []
        colors = ["Red", "Blue", "Green", "Yellow"]
        values = list(range(10)) + ["Skip", "Reverse", "+2"]

        for color in colors:
            for value in values:
                self.cards.append(Card(color, value))
                if value != 0:
                    self.cards.append(Card(color, value))

        for _ in range(4):
            self.cards.append(Card("Wild", "Wild"))
            self.cards.append(Card("Wild", "+4"))

        random.shuffle(self.cards)

    def draw(self):
        if not self.cards:
            return None
        return self.cards.pop()


# ------------------ PLAYER ------------------ #
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw_card(self, deck, count=1):
        for _ in range(count):
            card = deck.draw()
            if card:
                self.hand.append(card)


# ------------------ GAME GUI ------------------ #
class UnoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Uno - Player vs Computer")
        self.root.configure(bg="#FFC0CB")

        self.deck = Deck()

        self.human = Player("Sharon")
        self.computer = Player("Computer")

        for _ in range(7):
            self.human.draw_card(self.deck)
            self.computer.draw_card(self.deck)

        self.discard_pile = [self.deck.draw()]
        self.current_player = self.human

        self.setup_ui()
        self.refresh()

    # ---------- UI SETUP ---------- #
    def setup_ui(self):
        self.turn_label = tk.Label(self.root, font=("Arial", 16), bg="#FFC0CB")
        self.turn_label.pack(pady=10)

        self.discard_label = tk.Label(self.root, font=("Arial", 16), bg="#FFC0CB")
        self.discard_label.pack(pady=10)

        self.hand_frame = tk.Frame(self.root, bg="#FFC0CB")
        self.hand_frame.pack(pady=10)

        self.draw_button = tk.Button(
            self.root, text="Draw Card", bg="#FF69B4",
            fg="white", command=self.draw_card
        )
        self.draw_button.pack(pady=10)

    # ---------- REFRESH SCREEN ---------- #
    def refresh(self):
        self.turn_label.config(text=f"{self.current_player.name}'s Turn")
        self.discard_label.config(text=f"Top Card: {self.discard_pile[-1]}")

        for widget in self.hand_frame.winfo_children():
            widget.destroy()

        if self.current_player == self.human:
            for card in self.human.hand:
                btn = tk.Button(
                    self.hand_frame,
                    text=str(card),
                    width=12,
                    height=2,
                    bg=self.get_color(card.color),
                    fg="white",
                    command=lambda c=card: self.play_card(c)
                )
                btn.pack(side=tk.LEFT, padx=5)
        else:
            self.root.after(1000, self.computer_turn)

    # ---------- COLOR MAPPING ---------- #
    def get_color(self, color):
        return {
            "Red": "#FF0000",
            "Blue": "#0000FF",
            "Green": "#00AA00",
            "Yellow": "#CCCC00",
            "Wild": "#800080"
        }.get(color, "#FFFFFF")

    # ---------- VALID MOVE ---------- #
    def valid_move(self, card):
        top = self.discard_pile[-1]
        return (
                card.color == top.color
                or card.value == top.value
                or card.color == "Wild"
        )

    # ---------- PLAY CARD ---------- #
    def play_card(self, card):
        if not self.valid_move(card):
            messagebox.showinfo("Invalid Move", "You cannot play that card.")
            return

        self.human.hand.remove(card)
        self.discard_pile.append(card)

        self.apply_special(card, self.computer)

        if self.check_winner(self.human):
            return

        self.current_player = self.computer
        self.refresh()

    # ---------- COMPUTER TURN ---------- #
    def computer_turn(self):
        playable = [c for c in self.computer.hand if self.valid_move(c)]

        if playable:
            card = random.choice(playable)
            self.computer.hand.remove(card)
            self.discard_pile.append(card)
            self.apply_special(card, self.human)
        else:
            self.computer.draw_card(self.deck)

        if self.check_winner(self.computer):
            return

        self.current_player = self.human
        self.refresh()

    # ---------- DRAW CARD ---------- #
    def draw_card(self):
        if self.current_player != self.human:
            return

        self.human.draw_card(self.deck)
        self.current_player = self.computer
        self.refresh()

    # ---------- SPECIAL CARDS ---------- #
    def apply_special(self, card, opponent):
        if card.value == "+2":
            opponent.draw_card(self.deck, 2)
        elif card.value == "+4":
            opponent.draw_card(self.deck, 4)
        elif card.value == "Skip":
            pass  # skip works naturally in 2-player
        elif card.value == "Reverse":
            pass  # acts like skip in 2-player

        if card.color == "Wild":
            card.color = random.choice(["Red", "Blue", "Green", "Yellow"])

    # ---------- WIN CHECK ---------- #
    def check_winner(self, player):
        if len(player.hand) == 0:
            messagebox.showinfo("Game Over", f"{player.name} wins!")
            self.root.destroy()
            return True
        return False


# ------------------ RUN ------------------ #
if __name__ == "__main__":
    root = tk.Tk()
    game = UnoGUI(root)
    root.mainloop()