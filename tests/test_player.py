from player import Player
from deck import Deck


def test_player_draws_cards():
    deck = Deck()
    player = Player("Sharon")

    player.draw(deck, 3)
    assert len(player.hand) == 3


def test_player_play_card_removes_card():
    deck = Deck()
    player = Player("Sharon")

    player.draw(deck, 1)
    assert len(player.hand) == 1

    played = player.play_card(0)
    assert played is not None
    assert len(player.hand) == 0


def test_player_has_won():
    player = Player("Sharon")
    player.hand = []
    assert player.has_won() is True
