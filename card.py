class Card:
    def __init__(self, color, value):
        self.color = color      # Red, Yellow, Green, Blue, Wild
        self.value = value      # 0-9, Skip, Reverse, +2, Wild, Wild+4

    def is_playable_on(self, top_card, current_color):
        # If wild is active, match current color
        if self.color == "Wild":
            return True

        # Match by color
        if self.color == current_color:
            return True

        # Match by value
        if self.value == top_card.value:
            return True

        return False

    def __str__(self):
        return f"{self.color} {self.value}"
