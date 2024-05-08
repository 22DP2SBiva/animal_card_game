import animations
import utilities
# Determine battle outcome
def determine_outcome(card1, card2):
    # Check which cards tier is higher
    if card1[1] > card2[1]:
        winner = card1
    elif card1[1] == card2[1]:
        winner = None
    else:
        winner = card2
    return winner
def battle(self, card):
    cardd = card
    print("Battling")
    selected_card_pos = [self.selected_card[5].x, self.selected_card[5].y]
    cardd_pos = [cardd[5].x, cardd[5].y]
    min_distance = 40 # minimum distance till "hit" target position
    # Check if it's the PCs' turn, in whick case the PC would be attacking (third parameter is which card is attacking)
    if self.turn == "PC":
        # Calculate distance between pc card and player card
        distance_to_target = utilities.distance(cardd[5].x, cardd[5].y, self.selected_card[5].x, self.selected_card[5].y)
        if distance_to_target <= min_distance:
            print("Delay in battling")
            self.py.time.delay(1000) 
            
            # Disable event
            cardd[12] = 0
            self.battled_pc_card = cardd
            self.selected_card[12] = 1
            # Calculate winner of this battle
            winner = determine_outcome(self.selected_card, cardd)    
            # PC Wins
            if winner == cardd:
                points = utilities.calculate_score(self.selected_card)
                print("Remove 1")
                if [self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], True] in self.objects_to_display:
                    self.objects_to_display.remove([self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], True])
                    self.player_cards.remove(self.selected_card)
                    
                else:
                    self.objects_to_display.remove([self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], False])
                    self.player_cards.remove(self.selected_card)
                    
                basecard = utilities.blind_find(self, self.objects_to_display, selected_card_pos)
                self.objects_to_display.remove(basecard)
                if self.current_score >= points:
                    self.current_score -= points
                else:
                    self.current_score = 0
                
            elif winner is None:
                
                print("Remove both 2") 
                if [self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], True] in self.objects_to_display:
                    if len(self.pc_attacked) > 0:
                        # Remove also card from pc attacked list
                        # Card is in the list 
                        if cardd in self.pc_attacked:
                            self.pc_attacked.remove(cardd)
                        # Card isnt in list
                        else:
                            temp_card = cardd
                            temp_card[11] = None
                            # Alternative card is in list
                            if temp_card in self.pc_attacked:
                                self.pc_attacked.remove(temp_card)
                            # Otherwise card hasnt attacked and isnt in list
                    self.objects_to_display.remove([self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], True])
                    self.player_cards.remove(self.selected_card)
                    
                else:
                        # Remove also card from pc attacked list
                    # Card is in the list 
                    if cardd in self.pc_attacked:
                        self.pc_attacked.remove(cardd)
                    # Card isnt in list
                    else:
                        temp_card = cardd
                        temp_card[11] = None
                        # Alternative card is in list
                        if temp_card in self.pc_attacked:
                            self.pc_attacked.remove(temp_card)
                        # Otherwise card hasnt attacked and isnt in list
                    self.objects_to_display.remove([self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], False])
                    self.player_cards.remove(self.selected_card)
                    
                basecard = utilities.blind_find(self, self.objects_to_display, selected_card_pos)
                self.objects_to_display.remove(basecard)
                if [cardd[3], [cardd[5].x, cardd[5].y], False] in self.objects_to_display:
                    
                    if len(self.pc_attacked) > 0:
                        # Remove also card from pc attacked list
                        # Card is in the list 
                        if cardd in self.pc_attacked:
                            self.pc_attacked.remove(cardd)
                        # Card isnt in list
                        else:
                            temp_card = cardd
                            temp_card[11] = None
                            # Alternative card is in list
                            if temp_card in self.pc_attacked:
                                self.pc_attacked.remove(temp_card)
                            # Otherwise card hasnt attacked and isnt in list
                    self.objects_to_display.remove([cardd[3], [cardd[5].x, cardd[5].y], False])
                    self.pc_cards.remove(cardd)
                else:
                    # Remove also card from pc attacked list
                    # Card is in the list 
                    if cardd in self.pc_attacked:
                        self.pc_attacked.remove(cardd)
                    # Card isnt in list
                    else:
                        temp_card = cardd
                        temp_card[11] = None
                        # Alternative card is in list
                        if temp_card in self.pc_attacked:
                            self.pc_attacked.remove(temp_card)
                        # Otherwise card hasnt attacked and isnt in list
                    self.objects_to_display.remove([cardd[3], [cardd[5].x, cardd[5].y], True])
                    self.pc_cards.remove(cardd)
                basecard = utilities.blind_find(self, self.objects_to_display, cardd_pos)
                self.objects_to_display.remove(basecard)
            # Player wins
            else:
                print(self.pc_attacked)
                print(cardd)
                print("Remove 3") 
                if [cardd[3], [cardd[5].x, cardd[5].y], False] in self.objects_to_display:
                    if len(self.pc_attacked) > 0:
                        # Remove also card from pc attacked list
                        # Card is in the list 
                        if cardd in self.pc_attacked:
                            self.pc_attacked.remove(cardd)
                        # Card isnt in list
                        else:
                            temp_card = cardd
                            temp_card[11] = None
                            # Alternative card is in list
                            if temp_card in self.pc_attacked:
                                self.pc_attacked.remove(temp_card)
                            # Otherwise card hasnt attacked and isnt in list
                    self.objects_to_display.remove([cardd[3], [cardd[5].x, cardd[5].y], False])
                    self.pc_cards.remove(cardd)
                else:
                    if len(self.pc_attacked) > 0:
                        # Remove also card from pc attacked list
                        # Card is in the list 
                        if cardd in self.pc_attacked:
                            self.pc_attacked.remove(cardd)
                        # Card isnt in list
                        else:
                            temp_card = cardd
                            temp_card[11] = None
                            # Alternative card is in list
                            if temp_card in self.pc_attacked:
                                self.pc_attacked.remove(temp_card)
                            # Otherwise card hasnt attacked and isnt in list
                    self.objects_to_display.remove([cardd[3], [cardd[5].x, cardd[5].y], True])
                    self.pc_cards.remove(cardd)
                basecard = utilities.blind_find(self, self.objects_to_display, cardd_pos)
                self.objects_to_display.remove(basecard)
                points = utilities.calculate_score(cardd)
                self.current_score += points
            self.py.time.delay(500)
            self.card_destroy_sound.play()
            # Sort cards
            print("Sorts cards")
            
            utilities.sort_cards(self)
        else:
            cardd[12] = 1
            self.selected_card[12] = 1
            animations.Animations.card_battle(self, cardd, self.selected_card, cardd)
        
    # Check if it's the PLAYERS' turn, in whick case the PLAYER would be attacking (third parameter is which card is attacking)
    elif self.turn == "PLAYER":
        print("Player battling")
        distance_to_target = utilities.distance(self.selected_card[5].x, self.selected_card[5].y, cardd[5].x, cardd[5].y)
        if distance_to_target <= min_distance:
            # Disable event
            cardd[12] = 0
            self.selected_card[12] = 0
            cardd[11] = None
            self.selected_card[11] = None
            # Calculate winner of this battle
            winner = determine_outcome(cardd, self.selected_card)
            # Check which card has won, remove the other card
            if winner == cardd:
                points = utilities.calculate_score(self.selected_card)
                # Pc Wins
                print("Remove 1") 
                
                if [self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], True] in self.objects_to_display:
                    self.objects_to_display.remove([self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], True])
                    self.player_cards.remove(self.selected_card)
                    
                else:
                    self.objects_to_display.remove([self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], False])
                    self.player_cards.remove(self.selected_card)
                    
                basecard = utilities.blind_find(self, self.objects_to_display, selected_card_pos)
                self.objects_to_display.remove(basecard)
                if self.current_score >= points:
                    self.current_score -= points
                else:
                    self.current_score = 0
                
            elif winner is None:
                
                print("Remove both 2") 
                if [self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], True] in self.objects_to_display:
                    if len(self.pc_attacked) > 0:
                    # Remove also card from pc attacked list
                        # Card is in the list 
                        if cardd in self.pc_attacked:
                            self.pc_attacked.remove(cardd)
                        # Card isnt in list
                        else:
                            temp_card = cardd
                            temp_card[11] = None
                            # Alternative card is in list
                            if temp_card in self.pc_attacked:
                                self.pc_attacked.remove(temp_card)
                            # Otherwise card hasnt attacked and isnt in list
                    self.objects_to_display.remove([self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], True])
                    self.player_cards.remove(self.selected_card)
                    
                else:
                    if len(self.pc_attacked) > 0:
                    # Remove also card from pc attacked list
                        # Card is in the list 
                        if cardd in self.pc_attacked:
                            self.pc_attacked.remove(cardd)
                        # Card isnt in list
                        else:
                            temp_card = cardd
                            temp_card[11] = None
                            # Alternative card is in list
                            if temp_card in self.pc_attacked:
                                self.pc_attacked.remove(temp_card)
                            # Otherwise card hasnt attacked and isnt in list
                    self.objects_to_display.remove([self.selected_card[3], [self.selected_card[5].x, self.selected_card[5].y], False])
                    self.player_cards.remove(self.selected_card)
                    
                    
                basecard = utilities.blind_find(self, self.objects_to_display, selected_card_pos)
                self.objects_to_display.remove(basecard)
                if [cardd[3], [cardd[5].x, cardd[5].y], False] in self.objects_to_display:
                    if len(self.pc_attacked) > 0:
                    # Remove also card from pc attacked list
                        # Card is in the list 
                        if cardd in self.pc_attacked:
                            self.pc_attacked.remove(cardd)
                        # Card isnt in list
                        else:
                            temp_card = cardd
                            temp_card[11] = None
                            # Alternative card is in list
                            if temp_card in self.pc_attacked:
                                self.pc_attacked.remove(temp_card)
                            # Otherwise card hasnt attacked and isnt in list
                    self.objects_to_display.remove([cardd[3], [cardd[5].x, cardd[5].y], False])
                    self.pc_cards.remove(cardd)
                else:
                    if len(self.pc_attacked) > 0:
                    # Remove also card from pc attacked list
                        # Card is in the list 
                        if cardd in self.pc_attacked:
                            self.pc_attacked.remove(cardd)
                        # Card isnt in list
                        else:
                            temp_card = cardd
                            temp_card[11] = None
                            # Alternative card is in list
                            if temp_card in self.pc_attacked:
                                self.pc_attacked.remove(temp_card)
                            # Otherwise card hasnt attacked and isnt in list
                    self.objects_to_display.remove([cardd[3], [cardd[5].x, cardd[5].y], True])
                    self.pc_cards.remove(cardd)
                basecard = utilities.blind_find(self, self.objects_to_display, cardd_pos)
                self.objects_to_display.remove(basecard)
            else:
                # Player wins
                print("Remove 3") 
                print(self.pc_attacked)
                if [cardd[3], [cardd[5].x, cardd[5].y], False] in self.objects_to_display:
                    if len(self.pc_attacked) > 0:
                        # Remove also card from pc attacked list
                        # Card is in the list 
                        if cardd in self.pc_attacked:
                            self.pc_attacked.remove(cardd)
                        # Card isnt in list
                        else:
                            temp_card = cardd
                            temp_card[11] = None
                            # Alternative card is in list
                            if temp_card in self.pc_attacked:
                                self.pc_attacked.remove(temp_card)
                            # Otherwise card hasnt attacked and isnt in list
                    self.objects_to_display.remove([cardd[3], [cardd[5].x, cardd[5].y], False])
                    self.pc_cards.remove(cardd)
                else:
                    if len(self.pc_attacked) > 0:
                        # Remove also card from pc attacked list
                        # Card is in the list 
                        if cardd in self.pc_attacked:
                            self.pc_attacked.remove(cardd)
                        # Card isnt in list
                        else:
                            temp_card = cardd
                            temp_card[11] = None
                            # Alternative card is in list
                            if temp_card in self.pc_attacked:
                                self.pc_attacked.remove(temp_card)
                            # Otherwise card hasnt attacked and isnt in list
                    self.objects_to_display.remove([cardd[3], [cardd[5].x, cardd[5].y], True])
                    self.pc_cards.remove(cardd)
                basecard = utilities.blind_find(self, self.objects_to_display, cardd_pos)
                self.objects_to_display.remove(basecard)
                points = utilities.calculate_score(cardd)
                self.current_score += points
            self.py.time.delay(500)
            self.card_destroy_sound.play()
            # Sort cards
            print("Sorts cards")
            
            utilities.sort_cards(self)
        else:
            cardd[12] = 1
            self.selected_card[12] = 1
            animations.Animations.card_battle(self, cardd, self.selected_card, self.selected_card)
    