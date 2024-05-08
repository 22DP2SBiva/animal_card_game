import random
CARD_SPACING = 220
WHITE = (255, 255, 255)
player_last_card_pos = [0,0] # position of last card in player deck
pc_last_card_pos = [0,0] # position of last card in pc deck
cards = [
            # Title, Starting tier number, image directory, Action name
            ["Grasshopper", 1, "Assets/grasshopper.png", "None"],
            ["Frog", 2, "Assets/frog.png", "None"],
            ["Snake", 3, "Assets/snake.png", "None"],
            ["Eagle", 4, "Assets/eagle.png", "None"]
        ]
def generate_card():
    # Generates card image directory string to use from array (with card generation probabilities).
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
def generate_higher_tier_card(card_tier):
    for card in cards:
        if card[1] > card_tier:
            return card
def generate_cards(self, count_to_generate):
    i = 0 # Counter
    x = 0 # Amount by which we move each cards position more
    # Temporary sub-lists
    self.player_sub_list = []
    self.pc_sub_list = []
    
    player_pos = [350, 700] # Default pos
    pc_pos = [350, 80] # Default pos
    # Checks if current turn is not the first, if so then take last card positions from outside and redefine
    if self.turn_count > 1:
        player_last_card_pos[0] = self.player_cards[len(self.player_cards)-1][5].x
        player_last_card_pos[1] = self.player_cards[len(self.player_cards)-1][5].y
        pc_last_card_pos[0] = self.pc_cards[len(self.pc_cards)-1][5].x
        pc_last_card_pos[1] = self.pc_cards[len(self.pc_cards)-1][5].y
        player_last_card_pos[0] += 100
        pc_last_card_pos[0] += 100
        player_pos = player_last_card_pos
        pc_pos = pc_last_card_pos
        x = 100
    
    while(i < count_to_generate):
        # Generate card (Name, Tier, Image directory, Ability)
        
        # Create temporary lists that store the values, then add them to the main card deck lists and re-use these temp lists each loop
        # if there's already more than one list in sublists, empty the whole sublist: declare it as empty
        if(len(self.player_sub_list) > 0):  
            self.player_sub_list.clear()
            self.pc_sub_list.clear()
        card_sublist = generate_card()
        if len(self.player_cards) < self.max_card_amount:
            # generate a card, add it to player deck
            for item in card_sublist:
                self.player_sub_list.append(item)
        if len(self.pc_cards) < self.max_card_amount:
            # generate a card, add it to pc deck
            card_sublist = generate_card()
            for item in card_sublist:
                self.pc_sub_list.append(item)
        if len(self.player_cards) < self.max_card_amount:
            # PLAYER CARDS
            # load/transform card image
            self.player_sub_list[3] = self.py.image.load(self.player_sub_list[2]) # Loads image
            self.player_sub_list[3].convert_alpha() # Removes transparent bits from image
            self.player_sub_list[3] = self.py.transform.scale(self.player_sub_list[3], (1000,900)) # Scales image to fit

            # base cards
            self.player_sub_list.append(self.py.image.load('Assets/b_card.png').convert_alpha())
            self.player_sub_list[4] = self.py.transform.scale(self.player_sub_list[4], (1000,900))
            # create card rects (top left corner = 400+x, 200; widht = 150, height = 300)
            self.player_sub_list.append(self.py.Rect(player_pos[0] + x, player_pos[1], 170, 320)) # start button collsion rect index [5]
            # Add collision check bool
            self.player_sub_list.append(False) # always at start
            # Revealed bool (used for checking if player can currently see waht card it is)
            self.player_sub_list.append(False)
            # add position for further refrencing
            self.player_sub_list.append([player_pos[0] + x, player_pos[1]])
            # animation: is the card curretnly being animated?
            self.player_sub_list.append(False)
            # Color for debug mode
            self.player_sub_list.append(WHITE)
            # Currently activate event for this card
            self.player_sub_list.append(None)
            # Animation frames played in total
            self.player_sub_list.append(0)
            # Can the card move back?
            self.player_sub_list.append(False)
            # Stores refrence to semi-transparent grey image used to display on top of the card, to signify it can't be selected
            self.player_sub_list.append(0)
            # Has the card attacekd?
            self.player_sub_list.append(False)
            # Has the card jsut combined with another card?
            self.player_sub_list.append(False)

            # Store objects which need to be displayed to the screen
            # Base card must be displayed first since it is on the bottom most layer and the card image is on a higher layer
            self.objects_to_display.append([self.player_sub_list[4], self.player_sub_list[8], False])
            self.objects_to_display.append([self.player_sub_list[3], self.player_sub_list[8], False])
        if len(self.pc_cards) < self.max_card_amount:
            # PC CARDS
            
            # load card image
            self.pc_sub_list[3] = self.py.image.load(self.pc_sub_list[2])
            self.pc_sub_list[3].convert_alpha()
            self.pc_sub_list[3] = self.py.transform.scale(self.pc_sub_list[3], (1000,900))
            # base cards
            self.pc_sub_list.append(self.py.image.load('Assets/b_card.png').convert_alpha())
            self.pc_sub_list[4] = self.py.transform.scale(self.pc_sub_list[4], (1000,900))

            # Collision rects and checks

            # create card rects (top left corner = 400+x, 200; widht = 150, height = 300)
            self.pc_sub_list.append(self.py.Rect(pc_pos[0] + x, pc_pos[1], 170, 320)) # start button collsion rect index [5]
            # Add collision check bool
            self.pc_sub_list.append(False) # check if cursor is over rect (start button) index [6]
            # Revealed bool (used for checking if player can currently see waht card it is)
            self.pc_sub_list.append(False) # always at start
            # add position for further refrencing
            self.pc_sub_list.append([pc_pos[0] + x, pc_pos[1]])
            # animation: is the card curretnly being animated?
            self.pc_sub_list.append(False)
            # Color for debug mode
            self.pc_sub_list.append(WHITE)
            # Currently activate event for this card
            self.pc_sub_list.append(None)
            # Animation frames played in total
            self.pc_sub_list.append(0)
            # Can the card move back?
            self.pc_sub_list.append(False)
            # Stores refrence to semi-transparent grey image used to display on top of the card, to signify it can't be selected
            self.pc_sub_list.append(0)
            # Has the card attacekd?
            self.pc_sub_list.append(False)
            
            # Store objects which need to be displayed to the screen
            self.objects_to_display.append([self.pc_sub_list[4], self.pc_sub_list[8], False])
            self.objects_to_display.append([self.pc_sub_list[3], self.pc_sub_list[8], False])
        if len(self.player_cards) < self.max_card_amount:
            # append all items in player_sub_list to new empty list ath end of main player_cards list
            self.player_cards.append([])
            new_list = len(self.player_cards) - 1
            y = 0 # for getting rect position
            for item in self.player_sub_list:
                self.player_cards[new_list].append(item)
                # Saving positions of last cards to use in next turns
                if y == 5: # If were at the index the rect should be at, then set last pos to this sublsit value
                    player_last_card_pos[0] = self.player_sub_list[y][0]
                    player_last_card_pos[1] = self.player_sub_list[y][1]
                y += 1
        if len(self.pc_cards) < self.max_card_amount:
            # append all items in pc_sub_list to main pc_cards list
            self.pc_cards.append([])
            new_list = len(self.pc_cards) - 1
            y = 0 # for getting rect position
            for item in self.pc_sub_list:
                self.pc_cards[new_list].append(item)
                # Saving positions of last cards to use in next turns
                if y == 5: # If were at the index the rect should be at, then set last pos to this sublsit value
                    pc_last_card_pos[0] = self.pc_sub_list[y][0]
                    pc_last_card_pos[1] = self.pc_sub_list[y][1]
                y += 1
        i += 1
        x += CARD_SPACING
    self.generated_cards = True
    self.added_new_cards = True
def tier_up_cards(self):
    global card_obj
    new_player_card = []
    new_pc_card = []
    old_player_card = []
    old_pc_card = []
    # Replace not top tier cards in original list with next tier card (new cards)
    i = 0
    for cardd in self.player_cards:
        if cardd[1] != 4:
            new_card = generate_higher_tier_card(cardd[1])
            old_player_card.append([self.player_cards[i][3], [self.player_cards[i][5].x, self.player_cards[i][5].y], False])
            self.player_cards[i][0] = new_card[0]
            self.player_cards[i][1] = new_card[1]
            self.player_cards[i][2] = new_card[2]
            # convert/scale card image
            self.player_cards[i][3] = self.py.image.load(new_card[2])
            
            self.player_cards[i][3].convert_alpha()
            self.player_cards[i][3] = self.py.transform.scale(self.player_cards[i][3], (1000,900))
            new_player_card.append([self.player_cards[i][3], [self.player_cards[i][5].x, self.player_cards[i][5].y], False])
            
        i += 1
    i = 0
    for cardd in self.pc_cards:
        if cardd[1] != 4:
            new_card = generate_higher_tier_card(cardd[1])
            old_pc_card.append([self.pc_cards[i][3], [self.pc_cards[i][5].x, self.pc_cards[i][5].y], False])
            self.pc_cards[i][0] = new_card[0]
            self.pc_cards[i][1] = new_card[1]
            self.pc_cards[i][2] = new_card[2]
            # convert/scale card image
            self.pc_cards[i][3] = self.py.image.load(new_card[2])
            self.pc_cards[i][3].convert_alpha()
            self.pc_cards[i][3] = self.py.transform.scale(self.pc_cards[i][3], (1000,900))
            new_pc_card.append([self.pc_cards[i][3], [self.pc_cards[i][5].x, self.pc_cards[i][5].y], False])
            
        i += 1
    i = 0
    for cardd in old_player_card:
        if cardd in self.objects_to_display:
            index = self.objects_to_display.index(cardd)
            self.objects_to_display[index] = new_player_card[i]
        i += 1
    i = 0
    for cardd in old_pc_card:
        if cardd in self.objects_to_display:
            index = self.objects_to_display.index(cardd)
            self.objects_to_display[index] = new_pc_card[i]
        i += 1
    