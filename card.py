import random

class Card:
    def __init__(self, title, image_directory, tier, actions):
        self.title = title
        self.image_directory = image_directory
        self.tier = tier
        self.actions = actions

    def __str__(self):
        return f"Card(title={self.title}, tier={self.tier}, actions={self.actions})"

class CardDeck:
    def __init__(self, cards):
        self.cards = cards

    def generate_card(self):
        return random.choice(self.cards)

# Example usage
if __name__ == "__main__":
    # Define some sample cards
    card1 = Card("Card A", "images/card_a.png", 1, ["Action 1", "Action 2"])
    card2 = Card("Card B", "images/card_b.png", 2, ["Action 3", "Action 4"])
    card3 = Card("Card C", "images/card_c.png", 1, ["Action 5", "Action 6"])

    # Create a tuple of cards
    card_tuple = (card1, card2, card3)

    # Create a CardDeck with the tuple of cards
    card_deck = CardDeck(card_tuple)

    # Generate a random card
    random_card = card_deck.generate_card()

    # Print the randomly generated card
    print(random_card)
