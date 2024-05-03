# pylint: disable=no-member
# For managing user text input
NAME_MAX_CHAR_LIMIT = 15
PASSWORD_MAX_CHAR_LIMIT = 15
MAX_CARD_COUNT_MAX_CHAR_LIMIT = 1
NEW_CARD_MAX_CHAR_LIMIT = 1
MUSIC_MAX_CHAR_LIMIT = 3
SFX_MAX_CHAR_LIMIT = 3
class Text_Input:
    def write_text(self, py, event, typing_name, typing_password, typing_max_card_count, typing_new_card_count, typing_music_volume, typing_sfx_volume, user_name_text, user_password_text, max_card_count_text, new_card_count_text, music_volume_text, sfx_volume_text):
        if typing_name:
            if len(user_name_text) < NAME_MAX_CHAR_LIMIT:
                print("Typing name...")
                # Delete last character
                if event.key == py.K_BACKSPACE:
                    print("Delete letter")
                    self.user_name_text = self.user_name_text[:-1]
                # Done typing
                elif event.key == py.K_RETURN:
                    self.typing_name = False
                # Add input to string
                else:
                    print("Add letter")
                    self.user_name_text += event.unicode
                    # Trigger screen re-drawing to display text
                    print("Login open?", self.account_login_open)
            else:
                # Delete last character
                if event.key == py.K_BACKSPACE:
                    print("Delete letter")
                    self.user_name_text = self.user_name_text[:-1]
                # Done typing
                elif event.key == py.K_RETURN:
                    self.typing_name = False
        elif typing_password:
            if len(user_password_text) < PASSWORD_MAX_CHAR_LIMIT:
                print("Typing password...")
                if event.key == py.K_BACKSPACE:
                    self.user_password_text = self.user_password_text[:-1]
                # Done typing
                elif event.key == py.K_RETURN:
                    self.typing_password = False
                else:
                    self.user_password_text += event.unicode
            else:
                if event.key == py.K_BACKSPACE:
                    self.user_password_text = self.user_password_text[:-1]
                # Done typing
                elif event.key == py.K_RETURN:
                    self.typing_password = False
        elif typing_max_card_count:
            if len(max_card_count_text) < MAX_CARD_COUNT_MAX_CHAR_LIMIT:
                print("Typing MAX CARD...")
                if event.key == py.K_BACKSPACE:
                    self.max_card_count_text = max_card_count_text[:-1]
                # Done typing
                elif event.key == py.K_RETURN:
                    self.typing_max_card_count = False
                else:
                    self.max_card_count_text += event.unicode
            else:
                if event.key == py.K_BACKSPACE:
                    self.max_card_count_text = max_card_count_text[:-1]
                # Done typing
                elif event.key == py.K_RETURN:
                    self.typing_max_card_count = False
        elif typing_new_card_count:
            if len(new_card_count_text) < NEW_CARD_MAX_CHAR_LIMIT:
                print("Typing SFX...")
                if event.key == py.K_BACKSPACE:
                    self.new_card_count_text = self.new_card_count_text[:-1]
                # Done typing
                elif event.key == py.K_RETURN:
                    self.typing_new_card_count = False
                else:
                    self.new_card_count_text += event.unicode
            else:
                if event.key == py.K_BACKSPACE:
                    self.new_card_count_text = self.new_card_count_text[:-1]
                # Done typing
                elif event.key == py.K_RETURN:
                    self.typing_new_card_count = False
        elif typing_music_volume:
            if len(music_volume_text) < MUSIC_MAX_CHAR_LIMIT:
                print("Typing SFX...")
                if event.key == py.K_BACKSPACE:
                    self.music_volume_text = self.music_volume_text[:-1]
                # Done typing
                elif event.key == py.K_RETURN:
                    self.typing_music_volume = False
                else:
                    self.music_volume_text += event.unicode
            else:
                if event.key == py.K_BACKSPACE:
                    self.music_volume_text = self.music_volume_text[:-1]
                # Done typing
                elif event.key == py.K_RETURN:
                    self.typing_music_volume = False
        elif typing_sfx_volume:
            if len(sfx_volume_text) < SFX_MAX_CHAR_LIMIT:
                print("Typing SFX...")
                if event.key == py.K_BACKSPACE:
                    self.sfx_volume_text = self.sfx_volume_text[:-1]
                # Done typing
                elif event.key == py.K_RETURN:
                    self.typing_sfx_volume = False
                else:
                    self.sfx_volume_text += event.unicode
            else:
                if event.key == py.K_BACKSPACE:
                    self.sfx_volume_text = self.sfx_volume_text[:-1]
                # Done typing
                elif event.key == py.K_RETURN:
                    self.typing_sfx_volume = False
        # MAX character amount reached
        elif typing_max_card_count and len(max_card_count_text) ==  MAX_CARD_COUNT_MAX_CHAR_LIMIT:
            self.typing_max_card_count = False
        elif typing_new_card_count and len(new_card_count_text) ==  NEW_CARD_MAX_CHAR_LIMIT:
            self.typing_new_card_count = False
        elif typing_music_volume and len(music_volume_text) ==  MUSIC_MAX_CHAR_LIMIT:
            self.typing_music_volume = False
        elif typing_sfx_volume and len(sfx_volume_text) ==  SFX_MAX_CHAR_LIMIT:
            self.typing_sfx_volume = False
        elif self.typing_name and len(self.user_name_text) == NAME_MAX_CHAR_LIMIT:
            self.typing_name = False
        elif self.typing_password and len(self.user_password_text) == PASSWORD_MAX_CHAR_LIMIT:
            self.typing_password = False