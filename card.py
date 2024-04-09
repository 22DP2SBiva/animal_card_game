import random
cards = [
            # Title, Starting tier number, image directory, Action name
            ["Grasshopper", 1, "Assets/grasshopper.png", "None"],
            ["Frog", 2, "Assets/frog.png", "None"],
            ["Snake", 3, "Assets/snake.png", "None"],
            ["Eagle", 4, "Assets/eagle.png", "None"]
        ]
class Card:
    """Generates card image directory string to use from array (with card generation probabilities).

        Parameters:
            image(string): A string(card image directory)
            rect(rect): A rect that's linked to the card
        Returns:
            card(string): A string(card image directory)
    """
    def generate_card(self):
        # Define the cards chances
        card_chances = [
            (cards[0], 0.4),  # Grasshopper - 40%
            (cards[1], 0.3),  # Frog - 30%
            (cards[2], 0.2),  # Snake - 20%
            (cards[3], 0.1)   # Eagle - 10%
        ]
        # Choose a card based on the defined probabilities
        # zip takes card_chances as input and returns an iterator of tuples (groups all the elements at the same index together)
        # * symbol before zip and card_chances unpacks the variable. example: [1,2,3] becomes 1,2,3
        card = random.choices(*zip(*card_chances))[0]
        return card
    def generate_higher_tier_card(self, card_tier):
        for card in cards:
            if card[1] > card_tier:
                return card
    