import math
import animations
# Various useful functions
def sort_by_highest(accounts):
    # Sort players by highest score
    sorted_accounts = []
    for user in accounts:
        if not sorted_accounts: # If list empty, add first score
            sorted_accounts.append([user[2], user[0]]) # Append score and name of user
        else:
            inserted = False
            for i, sorted_user in enumerate(sorted_accounts):
                if int(user[2]) > int(sorted_user[0]):
                    sorted_accounts.insert(i, [user[2], user[0]])
                    inserted = True
                    break
            if not inserted:
                sorted_accounts.append([user[2], user[0]])
    return sorted_accounts
def sort_by_lowest(accounts):
    # Sort players by lowert score
    sorted_accounts = []
    for user in accounts:
        if not sorted_accounts: # If list empty, add first score
            sorted_accounts.append([user[2], user[0]]) # Append score and name of user
        else:
            inserted = False
            for i, sorted_user in enumerate(sorted_accounts):
                if int(user[2]) < int(sorted_user[0]):
                    sorted_accounts.insert(i, [user[2], user[0]])
                    inserted = True
                    break
            if not inserted:
                sorted_accounts.append([user[2], user[0]])
    return sorted_accounts
def calculate_score(card_obj):
    # Calculate each attack score based on card tier
    if card_obj[1] == 4:
        return 75
    elif card_obj[1] == 3:
        return 50
    elif card_obj[1] == 2:
        return 25
    elif card_obj[1] == 1:
        return 10
def distance(x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
def blind_find(self, specified_list, value):
    # Checks list for value and returns the sublist the value is a part of
    # Iterate through the specified list
    for sublist in specified_list:
        # Check if the known value is in the sublist
        if value in sublist:
            # If found, return value
            return sublist
def sort_cards(self):
    self.sorting_cards = True # Started sorting cards
    # Sort all cards in list position-wise
    self.new_positions = animations.Animations.sort_card_positions(self, self.objects_to_display, self.player_cards, self.pc_cards)
    # Set all cards' current event to moving to new position event
    for cardd in self.player_cards:
        cardd[11] = self.move_to_new_pos_event
    for cardd in self.pc_cards:
        cardd[11] = self.move_to_new_pos_event
    self.done_base_sort = True # Done sorting card position in list
def set_options_values(self, options):
    # Guest user
    if self.user_name_text == "" and self.user_password_text == "":
        self.max_card_count_text = options[1][2]
        self.new_card_count_text = options[1][3]
        self.bg_choice = options[1][4]
        self.music_volume_text = options[1][5]
        self.sfx_volume_text = options[1][6]
    # Registered user
    elif self.user_name_text != "" and self.user_password_text != "" and self.options_changed is True:
        self.max_card_count_text = options[2]
        self.new_card_count_text = options[3]
        self.bg_choice = options[4]
        self.music_volume_text = options[5]
        self.sfx_volume_text = options[6]

    