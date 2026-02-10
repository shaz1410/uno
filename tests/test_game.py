from game import Game
from card import Card


def test_reverse_direction():
    game = Game()
    original = game.direction
    game.reverse_direction()
    assert game.direction == original * -1


def test_apply_skip_card():
    game = Game()
    card = Card("Red", "Skip")
    game.apply_card_effect(card)
    assert game.skip_next is True


def test_apply_plus2_card():
    game = Game()
    card = Card("Blue", "+2")
    game.apply_card_effect(card)
    assert game.draw_amount == 2


def test_apply_reverse_card():
    game = Game()
    card = Card("Green", "Reverse")
    game.apply_card_effect(card)
    assert game.direction == -1


def test_next_player_changes_index():
    game = Game()
    game.players = [object(), object(), object()]
    game.current_player_index = 0
    game.next_player()
    assert game.current_player_index == 1
