class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw(self, deck, amount=1):
        for _ in range(amount):
            card = deck.draw_card()
            if card:
                self.hand.append(card)

    def play_card(self, index):
        return self.hand.pop(index)

    def has_won(self):
        return len(self.hand) == 0

    def show_hand(self):
        print(f"\n{self.name}'s hand:")
        for i, card in enumerate(self.hand):
            print(f"{i}: {card}")
