from card import Card


def test_card_string():
    c = Card("Red", "5")
    assert str(c) == "Red 5"


def test_card_playable_same_color():
    top = Card("Blue", "7")
    card = Card("Blue", "2")
    assert card.is_playable_on(top, "Blue") is True


def test_card_playable_same_value():
    top = Card("Green", "Skip")
    card = Card("Red", "Skip")
    assert card.is_playable_on(top, "Green") is True


def test_card_playable_wild():
    top = Card("Red", "9")
    card = Card("Wild", "Wild")
    assert card.is_playable_on(top, "Red") is True


def test_card_not_playable():
    top = Card("Red", "9")
    card = Card("Blue", "5")
    assert card.is_playable_on(top, "Red") is False
