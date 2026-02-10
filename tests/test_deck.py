from deck import Deck


def test_deck_has_cards():
    deck = Deck()
    assert len(deck.cards) > 0


def test_deck_draw_card_reduces_size():
    deck = Deck()
    start_size = len(deck.cards)

    card = deck.draw_card()
    assert card is not None
    assert len(deck.cards) == start_size - 1


def test_deck_draw_empty_returns_none():
    deck = Deck()
    deck.cards = []

    assert deck.draw_card() is None
