import random
from card import Card


class Deck:
    COLORS = ["Red", "Yellow", "Green", "Blue"]
    VALUES = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
              "Skip", "Reverse", "+2"]

    def __init__(self):
        self.cards = []
        self.build_deck()
        self.shuffle()

    def build_deck(self):
        self.cards = []

        for color in self.COLORS:
            # One 0 per color
            self.cards.append(Card(color, "0"))

            # Two of each other value
            for value in self.VALUES[1:]:
                self.cards.append(Card(color, value))
                self.cards.append(Card(color, value))

        # Add Wild cards
        for _ in range(4):
            self.cards.append(Card("Wild", "Wild"))
            self.cards.append(Card("Wild", "Wild+4"))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if len(self.cards) == 0:
            return None
        return self.cards.pop()
