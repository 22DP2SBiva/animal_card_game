import pygame
class Display:
    # pylint: disable=no-member
    # Display objects to screen
    def display_objects(self):
        # DISPLAYING OBJECTS
        # Display each object to screen
        for obj in self.objects_to_display:
            # Clarification:  image      position
            self.screen.blit(obj[0], obj[1])
    # Modify specified object that you still want to be dislayed to the screen
    def modify_objects_to_display(self, old_value, new_value):
        # Check all items in specified list
        i = 0
        while(i < len(self.objects_to_display)):
            # if the item is the same as the old value were looking for, then replace it as the new value]
            if self.objects_to_display[i][1] == old_value:
                self.objects_to_display[i][1] = new_value
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