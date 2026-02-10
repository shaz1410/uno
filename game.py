from deck import Deck
from player import Player


class Game:
    def __init__(self):
        self.deck = Deck()
        self.players = []
        self.current_player_index = 0
        self.direction = 1
        self.top_card = None
        self.current_color = None
        self.skip_next = False
        self.draw_amount = 0

    def setup(self):
        print("=== UNO GAME ===")

        num_players = int(input("How many players? (2-4): "))
        while num_players < 2 or num_players > 4:
            num_players = int(input("Enter a number between 2 and 4: "))

        for i in range(num_players):
            name = input(f"Enter name for Player {i + 1}: ")
            self.players.append(Player(name))

        # Deal 7 cards each
        for player in self.players:
            player.draw(self.deck, 7)

        # Set starting top card (must not be Wild+4)
        self.top_card = self.deck.draw_card()
        while self.top_card.color == "Wild" and self.top_card.value == "Wild+4":
            self.deck.cards.insert(0, self.top_card)
            self.top_card = self.deck.draw_card()

        self.current_color = self.top_card.color

    def next_player(self):
        self.current_player_index = (self.current_player_index + self.direction) % len(self.players)

    def reverse_direction(self):
        self.direction *= -1

    def choose_color(self):
        colors = ["Red", "Yellow", "Green", "Blue"]
        print("\nChoose a color:")
        for i, c in enumerate(colors):
            print(f"{i}: {c}")

        choice = input("Enter choice (0-3): ")
        while choice not in ["0", "1", "2", "3"]:
            choice = input("Enter choice (0-3): ")

        return colors[int(choice)]

    def apply_card_effect(self, card):
        if card.value == "Skip":
            self.skip_next = True

        elif card.value == "Reverse":
            self.reverse_direction()

        elif card.value == "+2":
            self.draw_amount += 2

        elif card.value == "Wild":
            self.current_color = self.choose_color()

        elif card.value == "Wild+4":
            self.draw_amount += 4
            self.current_color = self.choose_color()

    def handle_draw_effect(self):
        if self.draw_amount > 0:
            player = self.players[self.current_player_index]
            print(f"\n{player.name} must draw {self.draw_amount} cards!")
            player.draw(self.deck, self.draw_amount)
            self.draw_amount = 0

    def play_turn(self):
        player = self.players[self.current_player_index]

        print("\n=================================================================")
        print(f"Top Card: {self.top_card} | Current Color: {self.current_color}")
        print("===================================================================")

        if self.skip_next:
            print(f"{player.name} was skipped!")
            self.skip_next = False
            self.next_player()
            return

        self.handle_draw_effect()

        player.show_hand()

        playable_indexes = [
            i for i, card in enumerate(player.hand)
            if card.is_playable_on(self.top_card, self.current_color)
        ]

        if not playable_indexes:
            print("\nNo playable card. Drawing one...")
            player.draw(self.deck, 1)
            self.next_player()
            return

        print("\nPlayable cards:", playable_indexes)

        choice = input("Choose card index to play or type 'draw': ")

        if choice.lower() == "draw":
            player.draw(self.deck, 1)
            self.next_player()
            return

        if not choice.isdigit():
            print("Invalid input. Turn skipped.")
            self.next_player()
            return

        index = int(choice)

        if index < 0 or index >= len(player.hand):
            print("Invalid card index.")
            return

        chosen_card = player.hand[index]

        if not chosen_card.is_playable_on(self.top_card, self.current_color):
            print("You cannot play that card!")
            return

        played = player.play_card(index)
        self.top_card = played

        # Update current color
        if played.color != "Wild":
            self.current_color = played.color

        print(f"\n{player.name} played: {played}")

        self.apply_card_effect(played)

        if player.has_won():
            print(f"\n🎉 {player.name} WINS THE GAME! 🎉")
            exit()

        self.next_player()

    def start(self):
        self.setup()

        while True:
            self.play_turn()
