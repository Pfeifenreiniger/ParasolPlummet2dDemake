'''
Game Menu
Graphics and code by Kevin Spathmann (Pfeifenreiniger on GitHub: https://github.com/Pfeifenreiniger)
Inspired by Nintendo™ originals
'''

numb_of_players = 0


import pygame, sys, random, main
pygame.init()

## menu music ##
title_music = pygame.mixer.Sound("music/mparty3_Inside_the_Castle.mp3")
title_music.set_volume(0.5)
title_music_played = False

score_music = pygame.mixer.Sound("music/mparty3_The_Winner_is....Me!.mp3")
score_music.set_volume(0.7)
score_music_played = False

# menu sfx #
sfx_cursor_movement = pygame.mixer.Sound("sfx/menu/ssb_dot.wav")
sfx_cursor_movement.set_volume(0.4)
sfx_cursor_select = pygame.mixer.Sound("sfx/menu/ssb_select.wav")
sfx_cursor_select.set_volume(0.4)

sfx_koopa = pygame.mixer.Sound("sfx/menu/ssb_dot.wav")
sfx_koopa.set_volume(0.2)

sfx_score_screen = pygame.mixer.Sound("sfx/menu/sm64_high_score.wav")
sfx_score_screen.set_volume(0.8)
sfx_score_screen_played = False

voice_mario_selected = pygame.mixer.Sound("voices/mario/sm64_mario_its_me_(selected).wav")
voice_mario_selected.set_volume(0.5)
voice_peach_selected = pygame.mixer.Sound("voices/peach/mparty5_hooray_(selected).wav")
voice_peach_selected.set_volume(0.5)
voice_yoshi_selected = pygame.mixer.Sound("voices/yoshi/mparty5_yoshi_yooshi_(selected).wav")
voice_yoshi_selected.set_volume(0.5)
voice_waluigi_selected1 = pygame.mixer.Sound("voices/waluigi/mparty5_waluigi_whoahaha_(selected).wav")
voice_waluigi_selected1.set_volume(0.5)
voice_waluigi_selected2 = pygame.mixer.Sound("voices/waluigi/mparty5_waluigi_good_choice_(selected).wav")
voice_waluigi_selected2.set_volume(0.5)

## menu graphics ##
# bgs #
bg_numb_of_players = pygame.image.load("graphics/menu/bg_number_of_players.png").convert()
bg_char_select = pygame.image.load("graphics/menu/bg_character_selection.png").convert()
bg_control_mapping = pygame.image.load("graphics/menu/bg_control_mapping.png").convert()
bg_score_screen = pygame.image.load("graphics/menu/bg_score_screen.png").convert()
# control key mapping #
keys_numb_players_up_down = pygame.image.load("graphics/menu/control_mapping/control_keys_numbOfPlayers.png").convert_alpha()
keys_numb_players_enter = pygame.image.load("graphics/menu/control_mapping/control_keys_enter.png").convert_alpha()
keys_char_select_p1 = pygame.image.load("graphics/menu/control_mapping/p1_char_select.png").convert_alpha()
keys_char_select_p2 = pygame.image.load("graphics/menu/control_mapping/p2_char_select.png").convert_alpha()
keys_char_select_p3 = pygame.image.load("graphics/menu/control_mapping/p3_char_select.png").convert_alpha()
keys_char_select_p4 = pygame.image.load("graphics/menu/control_mapping/p4_char_select.png").convert_alpha()
keys_ingame_p1 = pygame.image.load("graphics/menu/control_mapping/p1_ingame_control.png").convert_alpha()
keys_ingame_p2 = pygame.image.load("graphics/menu/control_mapping/p2_ingame_control.png").convert_alpha()
keys_ingame_p3 = pygame.image.load("graphics/menu/control_mapping/p3_ingame_control.png").convert_alpha()
keys_ingame_p4 = pygame.image.load("graphics/menu/control_mapping/p4_ingame_control.png").convert_alpha()

# koopas #
menu_koopas = [pygame.image.load("graphics/menu/koopa/menu_koopa_1.png").convert_alpha(),
               pygame.image.load("graphics/menu/koopa/menu_koopa_2.png").convert_alpha()]
menu_koopa_counter = 0
menu_koopa_frameanimation = 0.005
menu_koopa_balloon = pygame.image.load("graphics/menu/koopa/balloon_koopa.png").convert_alpha()

which_menu = "numb_of_players"

def menu_change():
    global which_menu, Menucursor, koopa_advice1_t_counter, koopa_advice2_t_counter, koopa_advice3_t_counter, koopa_advice4_t_counter, koopa_advice5_t_counter, koopa_advice6_t_counter, koopa_advice7_t_counter, koopa_advice8_t_counter
    if which_menu == "numb_of_players":
        Menucursor.pressed = True
        which_menu = "char_select"
        koopa_advice1_t_counter = 0
        koopa_advice2_t_counter = 0
    elif which_menu == "char_select":
        which_menu = "control_mapping"
        koopa_advice3_t_counter = 0
        koopa_advice4_t_counter = 0
    elif which_menu == "control_mapping":
        which_menu = "score_screen"
        koopa_advice5_t_counter = 0
        koopa_advice6_t_counter = 0
    elif which_menu == "score_screen":
        which_menu = "numb_of_players"
        koopa_advice7_t_counter = 0
        koopa_advice8_t_counter = 0

p1_char = False
p2_char = False
p3_char = False
p4_char = False
def char_selected():
    global p1_char, p2_char, p3_char, p4_char
    if p1_char_select.character != "":
        p1_char = True
    if p2_char_select.character != "":
        p2_char = True
    if p3_char_select.character != "":
        p3_char = True
    if p4_char_select.character != "":
        p4_char = True

def char_selected_reset():
    global menu_cursor, p1_char, p2_char, p3_char, p4_char, p1_char_select, p2_char_select, p3_char_select, p4_char_select
    menu_cursor.x = 520
    menu_cursor.y = 50
    menu_cursor.number_of_players = 0
    menu_cursor.pressed = False
    if p1_char_select.character != "":
        p1_char = False
        p1_char_select.character = ""
        p1_char_select.x = 288
        p1_char_select.y = 50
        p1_char_select.pressed = False
    if p2_char_select.character != "":
        p2_char = False
        p2_char_select.character = ""
        p2_char_select.x = 305
        p2_char_select.y = 50
        p2_char_select.pressed = False
    if p3_char_select.character != "":
        p3_char = False
        p3_char_select.character = ""
        p3_char_select.x = 322
        p3_char_select.y = 50
        p3_char_select.pressed = False
    if p4_char_select.character != "":
        p4_char = False
        p4_char_select.character = ""
        p4_char_select.x = 339
        p4_char_select.y = 50
        p4_char_select.pressed = False

p1_rect_color = (255, 0, 0)
p2_rect_color = (0, 26, 255)
p3_rect_color = (37, 218, 21)
p4_rect_color = (235, 181, 47)
def char_select_rect():
    if p1_char:
        if p1_char_select.character == "mario":
            pygame.draw.rect(main.screen, p1_rect_color, p1_char_select.char_select_rect, 3, 2) # 3 line stroke, 2 smooth edges
        elif p1_char_select.character == "peach":
            pygame.draw.rect(main.screen, p1_rect_color, p1_char_select.char_select_rect, 3, 2)
        elif p1_char_select.character == "yoshi":
            pygame.draw.rect(main.screen, p1_rect_color, p1_char_select.char_select_rect, 3, 2)
        elif p1_char_select.character == "waluigi":
            pygame.draw.rect(main.screen, p1_rect_color, p1_char_select.char_select_rect, 3, 2)
    if p2_char:
        if p2_char_select.character == "mario":
            pygame.draw.rect(main.screen, p2_rect_color, p2_char_select.char_select_rect, 3, 2)
        elif p2_char_select.character == "peach":
            pygame.draw.rect(main.screen, p2_rect_color, p2_char_select.char_select_rect, 3, 2)
        elif p2_char_select.character == "yoshi":
            pygame.draw.rect(main.screen, p2_rect_color, p2_char_select.char_select_rect, 3, 2)
        elif p2_char_select.character == "waluigi":
            pygame.draw.rect(main.screen, p2_rect_color, p2_char_select.char_select_rect, 3, 2)
    if p3_char:
        if p3_char_select.character == "mario":
            pygame.draw.rect(main.screen, p3_rect_color, p3_char_select.char_select_rect, 3, 2)
        elif p3_char_select.character == "peach":
            pygame.draw.rect(main.screen, p3_rect_color, p3_char_select.char_select_rect, 3, 2)
        elif p3_char_select.character == "yoshi":
            pygame.draw.rect(main.screen, p3_rect_color, p3_char_select.char_select_rect, 3, 2)
        elif p3_char_select.character == "waluigi":
            pygame.draw.rect(main.screen, p3_rect_color, p3_char_select.char_select_rect, 3, 2)
    if p4_char:
        if p4_char_select.character == "mario":
            pygame.draw.rect(main.screen, p4_rect_color, p4_char_select.char_select_rect, 3, 2)
        elif p4_char_select.character == "peach":
            pygame.draw.rect(main.screen, p4_rect_color, p4_char_select.char_select_rect, 3, 2)
        elif p4_char_select.character == "yoshi":
            pygame.draw.rect(main.screen, p4_rect_color, p4_char_select.char_select_rect, 3, 2)
        elif p4_char_select.character == "waluigi":
            pygame.draw.rect(main.screen, p4_rect_color, p4_char_select.char_select_rect, 3, 2)


p1_rect_breite = 98
p1_rect_hoehe = 92
p2_rect_breite = 100
p2_rect_hoehe = 94
p3_rect_breite = 102
p3_rect_hoehe = 96
p4_rect_breite = 104
p4_rect_hoehe = 98
class Menucursor():
    def __init__(self, player=0, which_menu="numb_of_players"):
        self.player = player
        self.which_menu = which_menu
        if self.player == 0:
            self.img = pygame.image.load("graphics/menu/menu_cursor.png").convert_alpha()
        elif self.player == 1:
            self.img = pygame.image.load("graphics/menu/menu_cursor_p1.png").convert_alpha()
        elif self.player == 2:
            self.img = pygame.image.load("graphics/menu/menu_cursor_p2.png").convert_alpha()
        elif self.player == 3:
            self.img = pygame.image.load("graphics/menu/menu_cursor_p3.png").convert_alpha()
        elif self.player == 4:
            self.img = pygame.image.load("graphics/menu/menu_cursor_p4.png").convert_alpha()
        if self.which_menu == "numb_of_players":
            self.x = 520
            self.y = 50
        elif self.which_menu == "char_select":
            self.y = 50
            if self.player == 1:
                self.x = 288
            elif self.player == 2:
                self.x = 305
            elif self.player == 3:
                self.x = 322
            elif self.player == 4:
                self.x = 339
        self.pressed = False
        self.number_of_players = 0
        self.char_select_rect = pygame.Rect(self.x, self.y, 98, 92)
        self.character = ""
    def menu_input(self):
        global numb_of_players
        keys = pygame.key.get_pressed()
        if self.which_menu == "numb_of_players":
            if keys[pygame.K_w] and (self.y - 55 >= 50) and self.pressed != True:
                self.y -= 55
                self.pressed = True
                sfx_cursor_movement.play()
            elif keys[pygame.K_s] and (self.y + 55 <= 243) and self.pressed != True:
                self.y += 55
                self.pressed = True
                sfx_cursor_movement.play()
            elif keys[pygame.K_RETURN] and self.y == 50:
                self.number_of_players = 1
                self.pressed = True
                numb_of_players = 1
                sfx_cursor_select.play()
                menu_change()
            elif keys[pygame.K_RETURN] and self.y == 105:
                self.number_of_players = 2
                self.pressed = True
                numb_of_players = 2
                sfx_cursor_select.play()
                menu_change()
            elif keys[pygame.K_RETURN] and self.y == 160:
                self.number_of_players = 3
                self.pressed = True
                numb_of_players = 3
                sfx_cursor_select.play()
                menu_change()
            elif keys[pygame.K_RETURN] and self.y == 215:
                self.number_of_players = 4
                self.pressed = True
                numb_of_players = 4
                sfx_cursor_select.play()
                menu_change()
        elif self.which_menu == "char_select":
            if self.player == 1 and keys[pygame.K_w] and (self.y - 110 >= 50) and self.pressed != True:
                self.y -= 110
                self.pressed = True
                sfx_cursor_movement.play()
            elif self.player == 1 and keys[pygame.K_s] and (self.y + 110 <= 160) and self.pressed != True:
                self.y += 110
                self.pressed = True
                sfx_cursor_movement.play()
            elif self.player == 1 and keys[pygame.K_a] and (self.x - 132 >= 288) and self.pressed != True:
                self.x -= 132
                self.pressed = True
                sfx_cursor_movement.play()
            elif self.player == 1 and keys[pygame.K_d] and (self.x + 132 <= 420) and self.pressed != True:
                self.x += 132
                self.pressed = True
                sfx_cursor_movement.play()
            elif self.player == 1 and keys[pygame.K_x] and self.x == 288 and self.y == 50 and self.pressed != True:  # upper left
                self.character = "mario"
                self.char_select_rect = pygame.Rect(self.x-2, self.y+31, 98, 92)
                self.pressed = True
                voice_mario_selected.play()
                char_selected()
            elif self.player == 1 and keys[pygame.K_x] and self.x == 420 and self.y == 50 and self.pressed != True:  # upper right
                self.character = "peach"
                self.char_select_rect = pygame.Rect(self.x - 2, self.y + 31, p1_rect_breite, p1_rect_hoehe)
                self.pressed = True
                voice_peach_selected.play()
                char_selected()
            elif self.player == 1 and keys[pygame.K_x] and self.x == 288 and self.y == 160 and self.pressed != True: # down left
                self.character = "yoshi"
                self.char_select_rect = pygame.Rect(self.x - 2, self.y + 30, p1_rect_breite, p1_rect_hoehe)
                self.pressed = True
                voice_yoshi_selected.play()
                char_selected()
            elif self.player == 1 and keys[pygame.K_x] and self.x == 420 and self.y == 160 and self.pressed != True: # down right
                self.character = "waluigi"
                self.char_select_rect = pygame.Rect(self.x - 2, self.y + 30, p1_rect_breite, p1_rect_hoehe)
                self.pressed = True
                if random.randint(0,10) > 8:
                    voice_waluigi_selected2.play()
                else: voice_waluigi_selected1.play()
                char_selected()
            if self.player == 2 and keys[pygame.K_i] and (self.y - 110 >= 50) and self.pressed != True:
                self.y -= 110
                self.pressed = True
                sfx_cursor_movement.play()
            elif self.player == 2 and keys[pygame.K_k] and (self.y + 110 <= 160) and self.pressed != True:
                self.y += 110
                self.pressed = True
                sfx_cursor_movement.play()
            elif self.player == 2 and keys[pygame.K_j] and (self.x - 132 >= 305) and self.pressed != True:
                self.x -= 132
                self.pressed = True
                sfx_cursor_movement.play()
            elif self.player == 2 and keys[pygame.K_l] and (self.x + 132 <= 437) and self.pressed != True:
                self.x += 132
                self.pressed = True
                sfx_cursor_movement.play()
            elif self.player == 2 and keys[pygame.K_m] and self.x == 305 and self.y == 50 and self.pressed != True:
                self.character = "mario"
                self.char_select_rect = pygame.Rect(self.x - 21, self.y + 30, p2_rect_breite, p2_rect_hoehe)
                self.pressed = True
                voice_mario_selected.play()
                char_selected()
            elif self.player == 2 and keys[pygame.K_m] and self.x == 437 and self.y == 50 and self.pressed != True:
                self.character = "peach"
                self.char_select_rect = pygame.Rect(self.x - 21, self.y + 30, p2_rect_breite, p2_rect_hoehe)
                self.pressed = True
                voice_peach_selected.play()
                char_selected()
            elif self.player == 2 and keys[pygame.K_m] and self.x == 305 and self.y == 160 and self.pressed != True:
                self.character = "yoshi"
                self.char_select_rect = pygame.Rect(self.x - 21, self.y + 30, p2_rect_breite, p2_rect_hoehe)
                self.pressed = True
                voice_yoshi_selected.play()
                char_selected()
            elif self.player == 2 and keys[pygame.K_m] and self.x == 437 and self.y == 160 and self.pressed != True:
                self.character = "waluigi"
                self.char_select_rect = pygame.Rect(self.x - 21, self.y + 30, p2_rect_breite, p2_rect_hoehe)
                self.pressed = True
                if random.randint(0,10) > 8:
                    voice_waluigi_selected2.play()
                else: voice_waluigi_selected1.play()
                char_selected()
            if self.player == 3 and keys[pygame.K_UP] and (self.y - 110 >= 50) and self.pressed != True:
                self.y -= 110
                self.pressed = True
                sfx_cursor_movement.play()
            elif self.player == 3 and keys[pygame.K_DOWN] and (self.y + 110 <= 160) and self.pressed != True:
                self.y += 110
                self.pressed = True
                sfx_cursor_movement.play()
            elif self.player == 3 and keys[pygame.K_LEFT] and (self.x - 132 >= 322) and self.pressed != True:
                self.x -= 132
                self.pressed = True
                sfx_cursor_movement.play()
            elif self.player == 3 and keys[pygame.K_RIGHT] and (self.x + 132 <= 454) and self.pressed != True:
                self.x += 132
                self.pressed = True
                sfx_cursor_movement.play()
            elif self.player == 3 and keys[pygame.K_KP0] and self.x == 322 and self.y == 50 and self.pressed != True:
                self.character = "mario"
                self.char_select_rect = pygame.Rect(self.x - 40, self.y + 30, p3_rect_breite, p3_rect_hoehe)
                self.pressed = True
                voice_mario_selected.play()
                char_selected()
            elif self.player == 3 and keys[pygame.K_KP0] and self.x == 454 and self.y == 50 and self.pressed != True:
                self.character = "peach"
                self.char_select_rect = pygame.Rect(self.x - 40, self.y + 30, p3_rect_breite, p3_rect_hoehe)
                self.pressed = True
                voice_peach_selected.play()
                char_selected()
            elif self.player == 3 and keys[pygame.K_KP0] and self.x == 322 and self.y == 160 and self.pressed != True:
                self.character = "yoshi"
                self.char_select_rect = pygame.Rect(self.x - 40, self.y + 30, p3_rect_breite, p3_rect_hoehe)
                self.pressed = True
                voice_yoshi_selected.play()
                char_selected()
            elif self.player == 3 and keys[pygame.K_KP0] and self.x == 454 and self.y == 160 and self.pressed != True:
                self.character = "waluigi"
                self.char_select_rect = pygame.Rect(self.x - 40, self.y + 30, p3_rect_breite, p3_rect_hoehe)
                self.pressed = True
                if random.randint(0,10) > 8:
                    voice_waluigi_selected2.play()
                else: voice_waluigi_selected1.play()
                char_selected()
            if self.player == 4 and keys[pygame.K_KP8] and (self.y - 110 >= 50) and self.pressed != True:
                self.y -= 110
                self.pressed = True
                sfx_cursor_movement.play()
            elif self.player == 4 and keys[pygame.K_KP5] and (self.y + 110 <= 160) and self.pressed != True:
                self.y += 110
                self.pressed = True
                sfx_cursor_movement.play()
            elif self.player == 4 and keys[pygame.K_KP4] and (self.x - 132 >= 339) and self.pressed != True:
                self.x -= 132
                self.pressed = True
                sfx_cursor_movement.play()
            elif self.player == 4 and keys[pygame.K_KP6] and (self.x + 132 <= 471) and self.pressed != True:
                self.x += 132
                self.pressed = True
                sfx_cursor_movement.play()
            elif self.player == 4 and keys[pygame.K_KP2] and self.x == 339 and self.y == 50 and self.pressed != True:
                self.character = "mario"
                self.char_select_rect = pygame.Rect(self.x - 58, self.y + 29, p4_rect_breite, p4_rect_hoehe)
                self.pressed = True
                voice_mario_selected.play()
                char_selected()
            elif self.player == 4 and keys[pygame.K_KP2] and self.x == 471 and self.y == 50 and self.pressed != True:
                self.character = "peach"
                self.char_select_rect = pygame.Rect(self.x - 58, self.y + 29, p4_rect_breite, p4_rect_hoehe)
                self.pressed = True
                voice_peach_selected.play()
                char_selected()
            elif self.player == 4 and keys[pygame.K_KP2] and self.x == 339 and self.y == 160 and self.pressed != True:
                self.character = "yoshi"
                self.char_select_rect = pygame.Rect(self.x - 58, self.y + 29, p4_rect_breite, p4_rect_hoehe)
                self.pressed = True
                voice_yoshi_selected.play()
                char_selected()
            elif self.player == 4 and keys[pygame.K_KP2] and self.x == 471 and self.y == 160 and self.pressed != True:
                self.character = "waluigi"
                self.char_select_rect = pygame.Rect(self.x - 58, self.y + 29, p4_rect_breite, p4_rect_hoehe)
                self.pressed = True
                if random.randint(0,10) > 8:
                    voice_waluigi_selected2.play()
                else: voice_waluigi_selected1.play()
                char_selected()
    def menu_display(self):
        main.screen.blit(self.img, (self.x, self.y))
    def menu_update(self):
        self.menu_input()
        self.menu_display()
menu_cursor = Menucursor()  # without arguments; therefore, for number of players selector

p1_char_select = Menucursor(1,"char_select")
p2_char_select = Menucursor(2,"char_select")
p3_char_select = Menucursor(3,"char_select")
p4_char_select = Menucursor(4,"char_select")



## texts ##
# select number of players #
onePlayer = main.mario64_font.render("1 Player", False, (25, 25, 25))
onePlayer_rect = onePlayer.get_rect(center=(400, 101))
twoPlayer = main.mario64_font.render("2 Players", False, (25, 25, 25))
twoPlayer_rect = twoPlayer.get_rect(center=(400, 155))
threePlayer = main.mario64_font.render("3 Players", False, (25, 25, 25))
threePlayer_rect = threePlayer.get_rect(center=(400, 210))
fourPlayer = main.mario64_font.render("4 Players", False, (25, 25, 25))
fourPlayer_rect = fourPlayer.get_rect(center=(400, 265))
# koopa advice - textspeed #
koopa_t_speed = 0.4
# koopa advice - number of players #
koopa_advice1_text = "Select the number of players"
koopa_advice1_t_counter = 0
koopa_advice2_text = "who would like to play."
koopa_advice2_t_counter = 0

def display_menu_numb_of_players():
    global menu_koopa_counter, koopa_advice1_t_counter, koopa_advice2_t_counter
    main.screen.blit(bg_numb_of_players, (0, 0))
    main.screen.blit(keys_numb_players_up_down, (22, 97))
    main.screen.blit(keys_numb_players_enter, (682, 97))
    # text koopa advice
    koopa_advice1 = main.mario64_font.render(koopa_advice1_text[:round(koopa_advice1_t_counter)], False, (25, 25, 25))
    koopa_advice1_rect = koopa_advice1.get_rect(topleft=(95, 444))
    koopa_advice2 = main.mario64_font.render(koopa_advice2_text[:round(koopa_advice2_t_counter)], False, (25, 25, 25))
    koopa_advice2_rect = koopa_advice2.get_rect(topleft=(95, 500))
    main.screen.blit(menu_koopa_balloon, (69, 422))
    if round(koopa_advice1_t_counter) + 1 > len(koopa_advice1_text):
        koopa_advice1_t_counter = len(koopa_advice1_text)
        if round(koopa_advice2_t_counter)+ 1 > len(koopa_advice2_text):
            koopa_advice2_t_counter = len(koopa_advice2_text)
        else:
            koopa_advice2_t_counter += koopa_t_speed
            if round(koopa_advice2_t_counter) == (int(koopa_advice2_t_counter + 1)):
                sfx_koopa.play()
    else:
        koopa_advice1_t_counter += koopa_t_speed
        if round(koopa_advice1_t_counter) == (int(koopa_advice1_t_counter + 1)):
            sfx_koopa.play()
    main.screen.blit(koopa_advice1, koopa_advice1_rect)
    main.screen.blit(koopa_advice2, koopa_advice2_rect)
    # animated koopa
    main.screen.blit(menu_koopas[round(menu_koopa_counter)], (565, 320))
    if menu_koopa_counter > 0.55:
        menu_koopa_counter = 0
    else:
        menu_koopa_counter += menu_koopa_frameanimation
    # text of number of players
    main.screen.blit(onePlayer, onePlayer_rect)
    main.screen.blit(twoPlayer, twoPlayer_rect)
    main.screen.blit(threePlayer, threePlayer_rect)
    main.screen.blit(fourPlayer, fourPlayer_rect)

# koopa advice - char select #
koopa_advice3_text = "" # text will be set in display_char_select() function
koopa_advice3_t_counter = 0
koopa_advice4_text = ""
koopa_advice4_t_counter = 0

# graphics of characters for char select screen #
mar_head1 = pygame.image.load("graphics/menu/char_select_heads/mar_unselected.png").convert_alpha()
mar_head2 = pygame.image.load("graphics/menu/char_select_heads/mar_selected.png").convert_alpha()
pea_head1 = pygame.image.load("graphics/menu/char_select_heads/pea_unselected.png").convert_alpha()
pea_head2 = pygame.image.load("graphics/menu/char_select_heads/pea_selected.png").convert_alpha()
yos_head1 = pygame.image.load("graphics/menu/char_select_heads/yos_unselected.png").convert_alpha()
yos_head2 = pygame.image.load("graphics/menu/char_select_heads/yos_selected.png").convert_alpha()
wal_head1 = pygame.image.load("graphics/menu/char_select_heads/wal_unselected.png").convert_alpha()
wal_head2 = pygame.image.load("graphics/menu/char_select_heads/wal_selected.png").convert_alpha()
def display_char_heads():
    # mario
    if p1_char_select.character == "mario" or p2_char_select.character == "mario" or p3_char_select.character == "mario" or p4_char_select.character == "mario":
        main.screen.blit(mar_head2, (285, 83))
    else: main.screen.blit(mar_head1, (285, 83))
    # peach
    if p1_char_select.character == "peach" or p2_char_select.character == "peach" or p3_char_select.character == "peach" or p4_char_select.character == "peach":
        main.screen.blit(pea_head2, (418, 83))
    else: main.screen.blit(pea_head1, (418, 83))
    # yoshi
    if p1_char_select.character == "yoshi" or p2_char_select.character == "yoshi" or p3_char_select.character == "yoshi" or p4_char_select.character == "yoshi":
        main.screen.blit(yos_head2, (285, 190))
    else: main.screen.blit(yos_head1, (285, 190))
    # waluigi
    if p1_char_select.character == "waluigi" or p2_char_select.character == "waluigi" or p3_char_select.character == "waluigi" or p4_char_select.character == "waluigi":
        main.screen.blit(wal_head2, (418, 190))
    else: main.screen.blit(wal_head1, (418, 190))

def display_char_select():
    global menu_koopa_counter, koopa_advice3_text, koopa_advice4_text, koopa_advice3_t_counter, koopa_advice4_t_counter
    if numb_of_players == 1:    # in case of single player
        koopa_advice3_text = "Choose which character"
        koopa_advice4_text = "the player will use."
    else:   # else multi player
        koopa_advice3_text = "Choose which characters"
        koopa_advice4_text = "the players will use."
    main.screen.blit(bg_char_select, (0,0))
    display_char_heads()
    main.screen.blit(keys_char_select_p1, (10, 5))
    if numb_of_players > 1:
        main.screen.blit(keys_char_select_p2, (560, 5))
        if numb_of_players > 2:
            main.screen.blit(keys_char_select_p3, (10, 170))
            if numb_of_players > 3:
                main.screen.blit(keys_char_select_p4, (560, 170))
    # text koopa advice
    koopa_advice3 = main.mario64_font.render(koopa_advice3_text[:round(koopa_advice3_t_counter)], False, (25, 25, 25))
    koopa_advice3_rect = koopa_advice3.get_rect(topleft=(95, 444))
    koopa_advice4 = main.mario64_font.render(koopa_advice4_text[:round(koopa_advice4_t_counter)], False, (25, 25, 25))
    koopa_advice4_rect = koopa_advice4.get_rect(topleft=(95, 500))
    main.screen.blit(menu_koopa_balloon, (69, 422))
    if round(koopa_advice3_t_counter) + 1 > len(koopa_advice3_text):
        koopa_advice3_t_counter = len(koopa_advice3_text)
        if round(koopa_advice4_t_counter)+ 1 > len(koopa_advice4_text):
            koopa_advice4_t_counter = len(koopa_advice4_text)
        else:
            koopa_advice4_t_counter += koopa_t_speed
            if round(koopa_advice4_t_counter) == (int(koopa_advice4_t_counter + 1)):
                sfx_koopa.play()
    else:
        koopa_advice3_t_counter += koopa_t_speed
        if round(koopa_advice3_t_counter) == (int(koopa_advice3_t_counter + 1)):
            sfx_koopa.play()
    main.screen.blit(koopa_advice3, koopa_advice3_rect)
    main.screen.blit(koopa_advice4, koopa_advice4_rect)
    # animated koopa
    main.screen.blit(menu_koopas[round(menu_koopa_counter)], (565, 320))
    if menu_koopa_counter > 0.55:
        menu_koopa_counter = 0
    else:
        menu_koopa_counter += menu_koopa_frameanimation

# koopa advice - control mapping #
koopa_advice5_text = "Your game control. Be careful!"
koopa_advice5_t_counter = 0
koopa_advice6_text = "Press Enter to start."
koopa_advice6_t_counter = 0
def display_control_mapping():
    global menu_koopa_counter, koopa_advice5_t_counter, koopa_advice6_t_counter
    main.screen.blit(bg_control_mapping, (0,0))
    main.screen.blit(keys_ingame_p1, (10, 130))
    if numb_of_players > 1:
        main.screen.blit(keys_ingame_p2, (210, 130))
        if numb_of_players > 2:
            main.screen.blit(keys_ingame_p3, (410, 130))
            if numb_of_players > 3:
                main.screen.blit(keys_ingame_p4, (610, 130))
    # text koopa advice
    koopa_advice5 = main.mario64_font.render(koopa_advice5_text[:round(koopa_advice5_t_counter)], False, (25, 25, 25))
    koopa_advice5_rect = koopa_advice5.get_rect(topleft=(95, 444))
    koopa_advice6 = main.mario64_font.render(koopa_advice6_text[:round(koopa_advice6_t_counter)], False, (25, 25, 25))
    koopa_advice6_rect = koopa_advice6.get_rect(topleft=(95, 500))
    main.screen.blit(menu_koopa_balloon, (69, 422))
    if round(koopa_advice5_t_counter) + 1 > len(koopa_advice5_text):
        koopa_advice5_t_counter = len(koopa_advice5_text)
        if round(koopa_advice6_t_counter)+ 1 > len(koopa_advice6_text):
            koopa_advice6_t_counter = len(koopa_advice6_text)
        else:
            koopa_advice6_t_counter += koopa_t_speed
            if round(koopa_advice6_t_counter) == (int(koopa_advice6_t_counter + 1)):
                sfx_koopa.play()
    else:
        koopa_advice5_t_counter += koopa_t_speed
        if round(koopa_advice5_t_counter) == (int(koopa_advice5_t_counter + 1)):
            sfx_koopa.play()
    main.screen.blit(koopa_advice5, koopa_advice5_rect)
    main.screen.blit(koopa_advice6, koopa_advice6_rect)
    # animated koopa
    main.screen.blit(menu_koopas[round(menu_koopa_counter)], (565, 320))
    if menu_koopa_counter > 0.55:
        menu_koopa_counter = 0
    else:
        menu_koopa_counter += menu_koopa_frameanimation

# koopa advice - score screen #
koopa_advice7_text = "Press enter to retry..."
koopa_advice7_t_counter = 0
koopa_advice8_text = "...or space to restart the game."
koopa_advice8_t_counter = 0
def display_score_screen():
    global menu_koopa_counter, koopa_advice7_t_counter, koopa_advice8_t_counter, which_menu, sfx_score_screen_played
    if sfx_score_screen_played != True:
        sfx_score_screen.play()
        sfx_score_screen_played = True
    which_menu = "score_screen"
    main.screen.blit(bg_score_screen, (0, 0))
    # text koopa advice
    koopa_advice7 = main.mario64_font.render(koopa_advice7_text[:round(koopa_advice7_t_counter)], False, (25, 25, 25))
    koopa_advice7_rect = koopa_advice7.get_rect(topleft=(95, 444))
    koopa_advice8 = main.mario64_font.render(koopa_advice8_text[:round(koopa_advice8_t_counter)], False, (25, 25, 25))
    koopa_advice8_rect = koopa_advice8.get_rect(topleft=(95, 500))
    main.screen.blit(menu_koopa_balloon, (69, 422))
    if round(koopa_advice7_t_counter) + 1 > len(koopa_advice7_text):
        koopa_advice7_t_counter = len(koopa_advice7_text)
        if round(koopa_advice8_t_counter) + 1 > len(koopa_advice8_text):
            koopa_advice8_t_counter = len(koopa_advice8_text)
        else:
            koopa_advice8_t_counter += koopa_t_speed
            if round(koopa_advice8_t_counter) == (int(koopa_advice8_t_counter + 1)):
                sfx_koopa.play()
    else:
        koopa_advice7_t_counter += koopa_t_speed
        if round(koopa_advice7_t_counter) == (int(koopa_advice7_t_counter + 1)):
            sfx_koopa.play()
    main.screen.blit(koopa_advice7, koopa_advice7_rect)
    main.screen.blit(koopa_advice8, koopa_advice8_rect)
    # animated koopa
    main.screen.blit(menu_koopas[round(menu_koopa_counter)], (565, 320))
    if menu_koopa_counter > 0.55:
        menu_koopa_counter = 0
    else:
        menu_koopa_counter += menu_koopa_frameanimation