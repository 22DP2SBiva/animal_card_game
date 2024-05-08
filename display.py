import pygame
# pylint: disable=no-member
# Display objects to screen
UNSELECTABLE = 180
def display_objects(self):
    # Display each object to screen
    i = 0
    display_last = False
    base_of_last_object = None
    while i < len(self.objects_to_display):
        # Check if the object should be rendered at the top most layer
        if self.objects_to_display[i][2] is True:
            display_last = True
            # Search through all objects to find base card that mathes position of this top image card (but not the same object)
            x = 0
            for obj in self.objects_to_display:
                # Checks if object position is the same as current list obj position and if image is NOT same for both objects
                if obj[1] == self.objects_to_display[i][1] and obj[0] != self.objects_to_display[i][0]:
                    base_of_last_object = obj # base card
                x += 1
            last_object = self.objects_to_display[i] # card image
        else:
            # Clarification:  image      position
            self.screen.blit(self.objects_to_display[i][0], self.objects_to_display[i][1])
        i += 1
    # Display the top most ofject last, so that it renders on top of all other objects
    if display_last:
        if base_of_last_object is None:
            self.screen.blit(last_object[0], [200,200]) # card image
        else:
            self.screen.blit(base_of_last_object[0], base_of_last_object[1]) # base card
            self.screen.blit(last_object[0], last_object[1]) # card image
# Modify specified object that you still want to be dislayed to the screen
def modify_objects_to_display(self, old_value, new_value, top_most_layer):
    # Check all items in specified list
    i = 0
    while(i < len(self.objects_to_display)):
        # if the item is the same as the old value were looking for, then replace it as the new value]
        if self.objects_to_display[i][1] == old_value:
            self.objects_to_display[i][1] = new_value
            self.objects_to_display[i][2] = top_most_layer
        i += 1
# Debug mode: draw rects to screen
def debug_draw_rects(self):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 255, 0)
    i = 0
    # Check how cards should be drawn
    card_count = len(self.player_cards)
    color = BLACK
    while i < card_count:
        # Show collision objects and when cursor over them, turn red
        
        # PLAYER CARD COLLISION
        if self.p_colliding_with_card[i]:
            color = RED
            rect_to_draw = self.player_cards[i][5]
            self.player_cards[i][10] = color #Color rect red if colliding with player card

        else:
            color = BLUE
            rect_to_draw = self.player_cards[i][5]
            self.player_cards[i][10] = color #Color rect blue if not colliding with player card

        
        # Draw the rect
        debug_rect = rect_to_draw 
        self.debug_rects.append([self.screen, color, debug_rect])
        i += 1
    i = 0
    card_count = len(self.pc_cards)
    while i < card_count:
        # Show collision objects and when cursor over them, turn red
        
        # PC CARD COLLISION
        if self.pc_colliding_with_card[i]:
            color = RED
            self.pc_cards[i][10] = color #Color rect red if colliding with player card
            rect_to_draw = self.pc_cards[i][5]
        else:
            color = BLUE
            self.pc_cards[i][10] = color #Color rect blue if not colliding with player card
            rect_to_draw = self.pc_cards[i][5]
        # Draw the rect
        debug_rect = rect_to_draw
        self.debug_rects.append([self.screen, color, debug_rect])
        i += 1
    i = 0
    # Draw debug rects to screen
    while i < len(self.debug_rects):
        pygame.draw.rect(self.debug_rects[i][0],self.debug_rects[i][1],self.debug_rects[i][2])
        i += 1
def display_unselectable_cards(self):
    if self.turn is "PLAYER":
        # Display un-selectable cards
        if self.drawing_unselectable is False:
            for cardd in self.player_cards:
                if cardd[14] is not 0:
                    if self.press:
                        self.cant_select_sound.play()
                    self.drawing_unselectable = True
                    unselectable_image = pygame.Surface(cardd[5].size) # the size of rect
                    unselectable_image.set_alpha(UNSELECTABLE) # alpha level
                    unselectable_image.fill((255,255,255)) # this fills the entire surface
                    self.screen.blit(unselectable_image, [cardd[5].x, cardd[5].y]) # (0,0) are the top-left coordinates
                    cardd[14] = 0
            for cardd in self.pc_cards:
                if cardd[14] is not 0:
                    if self.press:
                        self.cant_select_sound.play()
                    self.drawing_unselectable = True
                    unselectable_image = pygame.Surface(cardd[5].size) # the size of rect
                    unselectable_image.set_alpha(UNSELECTABLE) # alpha level
                    unselectable_image.fill((255,255,255)) # this fills the entire surface
                    self.screen.blit(unselectable_image, [cardd[5].x, cardd[5].y]) # (0,0) are the top-left coordinates
                    cardd[14] = 0