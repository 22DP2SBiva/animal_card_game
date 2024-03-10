class Collisions:
    """Checks for collision between each card in deck and cursor.

        Parameters:
            rects(rect tuple): A rect tuple
            collision_checks(bool tuple): A boolean tuple
            mouse_pos(tuple): A tuple containing integers
            images(string tuple) A string(card image directory) tuple
        Returns:
            True(bool): A boolean
            rects[check]: A rect(which is currently colliding with cursor)

    """
    def deck_collide_check(self, rects, collision_checks, mouse_pos):
        i = 0
        cards_checked = [] # A boolean list to store all cards that have been checked
        while i < len(collision_checks):
            collision_checks[i] = rects[i].collidepoint(mouse_pos)
            if collision_checks[i]: # If cursor colliding with player card
                # return (collision on?, which card this is)
                cards_checked.append(True) # Add True (card colliding with cursor) to list of cards
            else: # Cursors isnt colliding with anything
                cards_checked.append(False) # Add False (card not colliding with cursor) to list of cards
            i += 1
        return cards_checked