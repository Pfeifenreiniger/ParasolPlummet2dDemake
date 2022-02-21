'''
2D pixelart demake of the glorious Mario Party 3 minigame Parasol Plummet
https://www.mariowiki.com/Parasol_Plummet
Code and graphics by Kevin Spathmann (Pfeifenreiniger on GitHub: https://github.com/Pfeifenreiniger)
Fonts used: "Mario Kart DS" by David (https://www.dafont.com/mario-kart-ds.font)
            "Super Mario 64 DS" by David (https://www.dafont.com/super-mario-64-ds.font)
Musics, SFX, and voices used from Nintendo™ originals (like Mario Party 5, Super Smash Bros. 64 or Super Mario 64)
Original Game (included in Mario Party 3) by Hudson Soft™ and Nintendo™
'''

import pygame, sys, random, PP_menu
pygame.init()
## fonts ##
marioKart_font = pygame.font.Font("font/Mario-Kart-DS.ttf", 35)
marioKart_font_large = pygame.font.Font("font/Mario-Kart-DS.ttf", 60)
marioKart_font_xlarge = pygame.font.Font("font/Mario-Kart-DS.ttf", 80)
mario64_font = pygame.font.Font("font/Super-Mario-64-DS.ttf", 20)

## display screen ##
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Parasol Plummet 2D Demake")
icon = pygame.image.load("graphics/game_icon.png").convert_alpha()
pygame.display.set_icon(icon)
fps = 30
clock = pygame.time.Clock()

## game music, effects, and voices ##
# music #
game_music = pygame.mixer.Sound("music/mparty3_Looking_Ahead.mp3")
game_music.set_volume(0.5)
# sfx #
sfx_coin = pygame.mixer.Sound("sfx/items/smw_coin.wav")
sfx_coin.set_volume(0.7)
sfx_bag = pygame.mixer.Sound("sfx/items/sm64_coin.wav")
sfx_bag.set_volume(0.7)
sfx_hammer_thrown = pygame.mixer.Sound("sfx/items/ssb_hammer_whoosh.wav")
sfx_hammer_thrown.set_volume(0.7)
sfx_hammer_hit1 = pygame.mixer.Sound("sfx/items/ssb_smash_hit_1.wav")
sfx_hammer_hit1.set_volume(0.7)
sfx_hammer_hit2 = pygame.mixer.Sound("sfx/items/ssb_smash_hit_2.wav")
sfx_hammer_hit2.set_volume(0.7)

## time limit ##
time_limit = 30
limit_time = 0
def display_time():
    global game_active
    current_time = int(time_limit - ((pygame.time.get_ticks() / 1000) - limit_time))
    if current_time <= 10:
        font = marioKart_font_xlarge
        time_color = (255, 0, 0)
    else:
        font = marioKart_font_large
        time_color = (250, 163, 27)
    time_surf = font.render(str(current_time), False, time_color)
    time_rect = time_surf.get_rect(center = (400, 60))
    screen.blit(time_surf, time_rect)
    if current_time <= 0:
        game_active = False

## player ##
class Player(pygame.sprite.Sprite):
    def __init__(self, playernumb, character):
        super().__init__()
        self.playernumb = playernumb
        self.character = character
        self.player_start_pos()
        self.player_img()
        self.floating_frame_numb = 0
        self.hitted_frame_numb = 0
        self.moving_speed = 10
        self.falling_state = False
        self.hitted_state = False
        self.collision_immune = False
        self.collision_time = 0
        self.coins = 0  # die zu sammelnden muenzen
        # voices #
        if self.character == "mario":
            if random.randint(1,2) > 1:
                self.got_coin = pygame.mixer.Sound("voices/mario/mparty5_mario_i_got_it_(got_coin).wav")
            else: self.got_coin = pygame.mixer.Sound("voices/mario/mparty5_mario_whoo_ohh_(got_coin).wav")
            self.hitted = pygame.mixer.Sound("voices/mario/sm64_mario_doh_(hitted_by_hammer).wav")
            self.crash = pygame.mixer.Sound("voices/mario/mparty5_mario_ouuu_(crash_with_another_player).wav")
        elif self.character == "peach":
            randomPea = random.randint(1,3)
            if randomPea == 1:
                self.got_coin = pygame.mixer.Sound("voices/peach/mparty5_peach_yay_(got_coin).wav")
            elif randomPea == 2:
                self.got_coin = pygame.mixer.Sound("voices/peach/mparty5_peach_yes_(got_coin).wav")
            elif randomPea == 3:
                self.got_coin = pygame.mixer.Sound("voices/peach/mparty5_peach_whoohoo_(got_coin).wav")
            self.hitted = pygame.mixer.Sound("voices/peach/mparty5_peach_nooo_(hitted_by_hammer).wav")
            self.crash = pygame.mixer.Sound("voices/peach/mparty5_peach_oh_(crash_with_another_player).wav")
        elif self.character == "yoshi":
            if random.randint(1,2) == 1:
                self.got_coin = pygame.mixer.Sound("voices/yoshi/mparty5_yoshi_yeaa_(got_coin).wav")
            else: self.got_coin = pygame.mixer.Sound("voices/yoshi/mparty5_yoshi_whaahoo_(got_coin).wav")
            randomYosh = random.randint(1,3)
            if randomYosh == 1:
                self.hitted = pygame.mixer.Sound("voices/yoshi/mparty5_yoshi_auauau_(hitted_by_hammer).wav")
            elif randomYosh == 2:
                self.hitted = pygame.mixer.Sound("voices/yoshi/mparty5_yoshi_awawaw_(hitted_by_hammer).wav")
            elif randomYosh == 3:
                self.hitted = pygame.mixer.Sound("voices/yoshi/mparty5_yoshi_haaa_(hitted_by_hammer).wav")
            self.crash = pygame.mixer.Sound("voices/yoshi/mparty5_yoshi_hou_(crash_with_another_player).wav")
        elif self.character == "waluigi":
            if random.randint(1,2) == 1:
                self.got_coin = pygame.mixer.Sound("voices/waluigi/mparty5_waluigi_yea_(got_coin).wav")
            else: self.got_coin = pygame.mixer.Sound("voices/waluigi/mparty5_waluigi_hehehe_(got_coin).wav")
            self.hitted = pygame.mixer.Sound("voices/waluigi/mparty5_waluigi_whahoahoa_(hitted_by_hammer).wav")
            self.crash = pygame.mixer.Sound("voices/waluigi/mparty5_waluigi_woua_(crash_with_another_player).wav")
    def player_img(self):
        if self.character == "waluigi":
            self.falling_frame = pygame.image.load("graphics/player/waluigi/falling/wal_falling.png").convert_alpha()
            self.floating_frames = [pygame.image.load("graphics/player/waluigi/floating/6uhr.png").convert_alpha(),
                                    pygame.image.load("graphics/player/waluigi/floating/5uhr.png").convert_alpha(),
                                    pygame.image.load("graphics/player/waluigi/floating/7uhr.png").convert_alpha()]
            self.hitted_frames = [pygame.image.load("graphics/player/waluigi/hitted/wal_hitted_6uhr.png").convert_alpha(),
                                  pygame.image.load("graphics/player/waluigi/hitted/wal_hitted_7uhr.png").convert_alpha(),
                                  pygame.image.load("graphics/player/waluigi/hitted/wal_hitted_9uhr.png").convert_alpha(),
                                  pygame.image.load("graphics/player/waluigi/hitted/wal_hitted_11uhr.png").convert_alpha(),
                                  pygame.image.load("graphics/player/waluigi/hitted/wal_hitted_12uhr.png").convert_alpha(),
                                  pygame.image.load("graphics/player/waluigi/hitted/wal_hitted_1uhr.png").convert_alpha(),
                                  pygame.image.load("graphics/player/waluigi/hitted/wal_hitted_3uhr.png").convert_alpha(),
                                  pygame.image.load("graphics/player/waluigi/hitted/wal_hitted_5uhr.png").convert_alpha()]
            self.score_img = pygame.image.load("graphics/player/waluigi/score/score_waluigi.png").convert_alpha()
        elif self.character == "peach":
            self.falling_frame = pygame.image.load("graphics/player/peach/falling/pea_falling.png").convert_alpha()
            self.floating_frames = [pygame.image.load("graphics/player/peach/floating/6uhr.png").convert_alpha(),
                                    pygame.image.load("graphics/player/peach/floating/5uhr.png").convert_alpha(),
                                    pygame.image.load("graphics/player/peach/floating/7uhr.png").convert_alpha()]
            self.hitted_frames = [pygame.image.load("graphics/player/peach/hitted/pea_6uhr.png").convert_alpha(),
                                  pygame.image.load("graphics/player/peach/hitted/pea_7uhr.png").convert_alpha(),
                                  pygame.image.load("graphics/player/peach/hitted/pea_9uhr.png").convert_alpha(),
                                  pygame.image.load("graphics/player/peach/hitted/pea_11uhr.png").convert_alpha(),
                                  pygame.image.load("graphics/player/peach/hitted/pea_12uhr.png").convert_alpha(),
                                  pygame.image.load("graphics/player/peach/hitted/pea_1uhr.png").convert_alpha(),
                                  pygame.image.load("graphics/player/peach/hitted/pea_3uhr.png").convert_alpha(),
                                  pygame.image.load("graphics/player/peach/hitted/pea_5uhr.png").convert_alpha()]
            self.score_img = pygame.image.load("graphics/player/peach/score/score_peach.png").convert_alpha()
        elif self.character == "yoshi":
            self.rare_chance = random.randint(1,10)
            if self.rare_chance <= 9:
                self.falling_frame = pygame.image.load("graphics/player/yoshi/falling/yoshi_falling.png").convert_alpha()
                self.floating_frames = [pygame.image.load("graphics/player/yoshi/floating/6uhr.png").convert_alpha(),
                                        pygame.image.load("graphics/player/yoshi/floating/5uhr.png").convert_alpha(),
                                        pygame.image.load("graphics/player/yoshi/floating/7uhr.png").convert_alpha()]
                self.hitted_frames = [pygame.image.load("graphics/player/yoshi/hitted/yos_hitted_6uhr.png").convert_alpha(),
                                      pygame.image.load("graphics/player/yoshi/hitted/yos_hitted_7uhr.png").convert_alpha(),
                                      pygame.image.load("graphics/player/yoshi/hitted/yos_hitted_9uhr.png").convert_alpha(),
                                      pygame.image.load("graphics/player/yoshi/hitted/yos_hitted_11uhr.png").convert_alpha(),
                                      pygame.image.load("graphics/player/yoshi/hitted/yos_hitted_12uhr.png").convert_alpha(),
                                      pygame.image.load("graphics/player/yoshi/hitted/yos_hitted_1uhr.png").convert_alpha(),
                                      pygame.image.load("graphics/player/yoshi/hitted/yos_hitted_3uhr.png").convert_alpha(),
                                      pygame.image.load("graphics/player/yoshi/hitted/yos_hitted_5uhr.png").convert_alpha()]
                self.score_img = pygame.image.load("graphics/player/yoshi/score/score_yoshi.png").convert_alpha()
            else:
                self.falling_frame = pygame.image.load("graphics/player/yoshi/falling/rare/yos_falling.png").convert_alpha()
                self.floating_frames = [pygame.image.load("graphics/player/yoshi/floating/rare/6uhr.png").convert_alpha(),
                                        pygame.image.load("graphics/player/yoshi/floating/rare/5uhr.png").convert_alpha(),
                                        pygame.image.load("graphics/player/yoshi/floating/rare/7uhr.png").convert_alpha()]
                self.hitted_frames = [pygame.image.load("graphics/player/yoshi/hitted/rare/yos_hitted_rare_6uhr.png").convert_alpha(),
                                      pygame.image.load("graphics/player/yoshi/hitted/rare/yos_hitted_rare_7uhr.png").convert_alpha(),
                                      pygame.image.load("graphics/player/yoshi/hitted/rare/yos_hitted_rare_9uhr.png").convert_alpha(),
                                      pygame.image.load("graphics/player/yoshi/hitted/rare/yos_hitted_rare_11uhr.png").convert_alpha(),
                                      pygame.image.load("graphics/player/yoshi/hitted/rare/yos_hitted_rare_12uhr.png").convert_alpha(),
                                      pygame.image.load("graphics/player/yoshi/hitted/rare/yos_hitted_rare_1uhr.png").convert_alpha(),
                                      pygame.image.load("graphics/player/yoshi/hitted/rare/yos_hitted_rare_3uhr.png").convert_alpha(),
                                      pygame.image.load("graphics/player/yoshi/hitted/rare/yos_hitted_rare_5uhr.png").convert_alpha()]
                self.score_img = pygame.image.load("graphics/player/yoshi/score/rare/score_yoshi_rare.png").convert_alpha()
        elif self.character == "mario":
            self.falling_frame = pygame.image.load("graphics/player/mario/falling/mar_falling.png").convert_alpha()
            self.floating_frames = [pygame.image.load("graphics/player/mario/floating/6uhr.png").convert_alpha(),
                                    pygame.image.load("graphics/player/mario/floating/5uhr.png").convert_alpha(),
                                    pygame.image.load("graphics/player/mario/floating/7uhr.png").convert_alpha()]
            self.hitted_frames = [pygame.image.load("graphics/player/mario/hitted/mar_hitted_6uhr.png").convert_alpha(),
                                  pygame.image.load("graphics/player/mario/hitted/mar_hitted_7uhr.png").convert_alpha(),
                                  pygame.image.load("graphics/player/mario/hitted/mar_hitted_9uhr.png").convert_alpha(),
                                  pygame.image.load("graphics/player/mario/hitted/mar_hitted_11uhr.png").convert_alpha(),
                                  pygame.image.load("graphics/player/mario/hitted/mar_hitted_12uhr.png").convert_alpha(),
                                  pygame.image.load("graphics/player/mario/hitted/mar_hitted_1uhr.png").convert_alpha(),
                                  pygame.image.load("graphics/player/mario/hitted/mar_hitted_3uhr.png").convert_alpha(),
                                  pygame.image.load("graphics/player/mario/hitted/mar_hitted_5uhr.png").convert_alpha()]
            self.score_img = pygame.image.load("graphics/player/mario/score/score_mario.png").convert_alpha()
        self.rect = self.floating_frames[0].get_rect(topleft=(self.x, self.y))
        if self.playernumb == 1:
            self.score_rect = self.score_img.get_rect(topleft=(60, 38))
        elif self.playernumb == 2:
            self.score_rect = self.score_img.get_rect(topleft=(568, 38))
        elif self.playernumb == 3:
            self.score_rect = self.score_img.get_rect(topleft=(60, 519))
        elif self.playernumb == 4:
            self.score_rect = self.score_img.get_rect(topleft=(568, 519))
    def player_start_pos(self):
        if self.playernumb == 1:  # starting pos of x depending on player number
            self.x = 161
        elif self.playernumb == 2:
            self.x = 296
        elif self.playernumb == 3:
            self.x = 400
        elif self.playernumb == 4:
            self.x = 564
        self.y = 600  # starting pos of y at the beginning right at the bottom of the screen
    def player_input(self):
        keys = pygame.key.get_pressed()
        if self.playernumb == 1:    ## a and d
            if self.falling_state != True and keys[pygame.K_a] and self.rect.left > 133:
                self.rect.left -= self.moving_speed
                self.floating_frame_numb = 1
            elif self.falling_state != True and keys[pygame.K_d] and self.rect.right < 668:
                self.rect.left += self.moving_speed
                self.floating_frame_numb = 2
            else:
                self.floating_frame_numb = 0
        elif self.playernumb == 2:    ## j and l
            if self.falling_state != True and keys[pygame.K_j] and self.rect.left > 133:
                self.rect.left -= self.moving_speed
                self.floating_frame_numb = 1
            elif self.falling_state != True and keys[pygame.K_l] and self.rect.right < 668:
                self.rect.left += self.moving_speed
                self.floating_frame_numb = 2
            else:
                self.floating_frame_numb = 0
        elif self.playernumb == 3:  ## arrow keys
            if self.falling_state != True and keys[pygame.K_LEFT] and self.rect.left > 133:
                self.rect.left -= self.moving_speed
                self.floating_frame_numb = 1
            elif self.falling_state != True and keys[pygame.K_RIGHT] and self.rect.right < 668:
                self.rect.left += self.moving_speed
                self.floating_frame_numb = 2
            else:
                self.floating_frame_numb = 0
        elif self.playernumb == 4:  ## numb pad 4 and 6
            if self.falling_state != True and keys[pygame.K_KP4] and self.rect.left > 133:
                self.rect.left -= self.moving_speed
                self.floating_frame_numb = 1
            elif self.falling_state != True and keys[pygame.K_KP6] and self.rect.right < 668:
                self.rect.left += self.moving_speed
                self.floating_frame_numb = 2
            else:
                self.floating_frame_numb = 0
    def player_movement(self):
        if self.falling_state != True:
            if self.rect.top > -10:
                self.rect.top -= 8
            else:
                self.falling_state = True
        elif self.falling_state and self.hitted_state:
            self.rect.top += 20
            if self.rect.top + 20 >= 500:
                self.hitted_state = False
                self.falling_state = False
        elif self.falling_state:
            self.rect.top += 20
            if self.rect.top + 20 >= 500:
                self.falling_state = False
    def player_drawing(self):
        if self.falling_state != True:
            if self.collision_immune != True:
                screen.blit(self.floating_frames[self.floating_frame_numb], self.rect)
            else:
                self.inv_model = self.floating_frames[self.floating_frame_numb].copy()
                self.inv_model.set_alpha(128)
                screen.blit(self.inv_model, self.rect)
        elif self.falling_state and self.hitted_state and self.collision_immune:
            self.inv_model = self.hitted_frames[round(self.hitted_frame_numb)].copy()
            self.inv_model.set_alpha(128)
            screen.blit(self.inv_model, self.rect)
            if round(self.hitted_frame_numb + 0.4) > 7:
                self.hitted_frame_numb = 0
            else:
                self.hitted_frame_numb += 0.4
        else:
            if self.collision_immune != True:
                screen.blit(self.falling_frame, self.rect)
            else:
                self.inv_model = self.falling_frame.copy()
                self.inv_model.set_alpha(128)
                screen.blit(self.inv_model, self.rect)
    def score_display(self):
        screen.blit(self.score_img, self.score_rect)
        self.score_font_surf = marioKart_font.render("x  " + str(self.coins), False, (250, 163, 27))
        if self.playernumb == 1:
            self.score_font_rect = self.score_font_surf.get_rect(topleft=(148,46))
        elif self.playernumb == 2:
            self.score_font_rect = self.score_font_surf.get_rect(topleft=(658,46))
        elif self.playernumb == 3:
            self.score_font_rect = self.score_font_surf.get_rect(topleft=(148,527))
        elif self.playernumb == 4:
            self.score_font_rect = self.score_font_surf.get_rect(topleft=(658,527))
        screen.blit(self.score_font_surf, self.score_font_rect)
    def player_update(self):
        self.coin_collected = False
        self.player_input()
        self.player_movement()
        self.player_drawing()
        self.score_display()
    def player_reset(self):
        self.player_start_pos()
        self.player_img()
        self.floating_frame_numb = 0
        self.hitted_frame_numb = 0
        self.moving_speed = 10
        self.falling_state = False
        self.hitted_state = False
        self.collision_immune = False
        self.collision_time = 0
        self.coins = 0  # coins to collect = game score
player1 = Player(1, "waluigi")  # testplayer1
player2 = Player(2, "waluigi") # testplayer2
player3 = Player(3, "waluigi") # testplayer3
player4 = Player(4, "waluigi") # testplayer4
numb_of_players = PP_menu.numb_of_players

player_collision_bounce = 40
def player_collision():
    if numb_of_players > 1:
        ## 1 vs 2 player
        if pygame.sprite.collide_rect(player1, player2):  ## top-bottom p1
            if player1.falling_state != True and player2.falling_state != True:
                if player1.rect.bottom >= player2.rect.top and player1.rect.bottom <= player2.rect.bottom:
                    player1.rect.top -= player_collision_bounce
                    player2.rect.top += player_collision_bounce
                    player2.crash.play()
        if pygame.sprite.collide_rect(player2, player1):  ## top-bottom p2
            if player2.falling_state != True and player1.falling_state != True:
                if player2.rect.bottom >= player1.rect.top and player2.rect.bottom <= player1.rect.bottom:
                    player2.rect.top -= player_collision_bounce
                    player1.rect.top += player_collision_bounce
                    player1.crash.play()
    if numb_of_players > 2:
        ## 3 player vs 1 and 2
        if pygame.sprite.collide_rect(player3, player1):  ## top-bottom p3
            if player3.falling_state != True and player1.falling_state != True:
                if player3.rect.bottom >= player1.rect.top and player3.rect.bottom <= player1.rect.bottom:
                    player3.rect.top -= player_collision_bounce
                    player1.rect.top += player_collision_bounce
                    player1.crash.play()
        if pygame.sprite.collide_rect(player1, player3):  ## top-bottom p1
            if player1.falling_state != True and player3.falling_state != True:
                if player1.rect.bottom >= player3.rect.top and player1.rect.bottom <= player3.rect.bottom:
                    player1.rect.top -= player_collision_bounce
                    player3.rect.top += player_collision_bounce
                    player3.crash.play()
        if pygame.sprite.collide_rect(player3, player2):  ## top-bottom p3
            if player3.falling_state != True and player2.falling_state != True:
                if player3.rect.bottom >= player2.rect.top and player3.rect.bottom <= player2.rect.bottom:
                    player3.rect.top -= player_collision_bounce
                    player2.rect.top += player_collision_bounce
                    player2.crash.play()
        if pygame.sprite.collide_rect(player2, player3):  ## top-bottom p2
            if player2.falling_state != True and player3.falling_state != True:
                if player2.rect.bottom >= player3.rect.top and player2.rect.bottom <= player3.rect.bottom:
                    player2.rect.top -= player_collision_bounce
                    player3.rect.top += player_collision_bounce
                    player3.crash.play()
    if numb_of_players > 3:
        ## 4 player vs 1 vs 2 and vs 3
        if pygame.sprite.collide_rect(player4, player1):  ## top-bottom p4
            if player4.falling_state != True and player4.falling_state != True:
                if player4.rect.bottom >= player1.rect.top and player4.rect.bottom <= player1.rect.bottom:
                    player4.rect.top -= player_collision_bounce
                    player1.rect.top += player_collision_bounce
                    player1.crash.play()
        if pygame.sprite.collide_rect(player1, player4):  ## top-bottom p1
            if player1.falling_state != True and player4.falling_state != True:
                if player1.rect.bottom >= player4.rect.top and player1.rect.bottom <= player4.rect.bottom:
                    player1.rect.top -= player_collision_bounce
                    player4.rect.top += player_collision_bounce
                    player4.crash.play()
        if pygame.sprite.collide_rect(player4, player2):  ## top-bottom p4
            if player4.falling_state != True and player2.falling_state != True:
                if player4.rect.bottom >= player2.rect.top and player4.rect.bottom <= player2.rect.bottom:
                    player4.rect.top -= player_collision_bounce
                    player2.rect.top += player_collision_bounce
                    player2.crash.play()
        if pygame.sprite.collide_rect(player2, player4):  ## top-bottom p2
            if player2.falling_state != True and player4.falling_state != True:
                if player2.rect.bottom >= player4.rect.top and player2.rect.bottom <= player4.rect.bottom:
                    player2.rect.top -= player_collision_bounce
                    player4.rect.top += player_collision_bounce
                    player4.crash.play()
        if pygame.sprite.collide_rect(player4, player3):  ## top-bottom p4
            if player4.falling_state != True and player3.falling_state != True:
                if player4.rect.bottom >= player3.rect.top and player4.rect.bottom <= player3.rect.bottom:
                    player4.rect.top -= player_collision_bounce
                    player3.rect.top += player_collision_bounce
                    player3.crash.play()
        if pygame.sprite.collide_rect(player3, player4):  ## top-bottom p3
            if player3.falling_state != True and player4.falling_state != True:
                if player3.rect.bottom >= player4.rect.top and player3.rect.bottom <= player4.rect.bottom:
                    player3.rect.top -= player_collision_bounce
                    player4.rect.top += player_collision_bounce
                    player4.crash.play()

## items ##
# hammers #
class Hammer(pygame.sprite.Sprite):
    def __init__(self, side):
        super().__init__()
        self.side = side
        self.frames = [pygame.image.load("graphics/items/hammer/hammer6uhr.png").convert_alpha(),
                       pygame.image.load("graphics/items/hammer/hammer7uhr.png").convert_alpha(),
                       pygame.image.load("graphics/items/hammer/hammer9uhr.png").convert_alpha(),
                       pygame.image.load("graphics/items/hammer/hammer11uhr.png").convert_alpha(),
                       pygame.image.load("graphics/items/hammer/hammer12uhr.png").convert_alpha(),
                       pygame.image.load("graphics/items/hammer/hammer1uhr.png").convert_alpha(),
                       pygame.image.load("graphics/items/hammer/hammer3uhr.png").convert_alpha(),
                       pygame.image.load("graphics/items/hammer/hammer6uhr.png").convert_alpha()]
        if self.side == "left":
            self.x = 96
        else:
            self.x = 655
        self.swing = random.randint(2,5)
        self.y = 110
        self.framecounter = 0
    def animation(self):
        self.rect = self.frames[0].get_rect(topleft=(self.x, self.y))
        screen.blit(self.frames[round(self.framecounter)], self.rect)
        if round(self.framecounter + 0.3) > 7:
            self.framecounter = 0
        else:
            self.framecounter += 0.3
    def moving(self):
        if self.side == "left":
            self.x += round(self.swing)
        else:
            self.x -= round(self.swing)
        if self.swing <= 0:
            self.swing = 0
        else: self.swing -= 0.01
        self.y += 4
    def destroy(self):
        if self.y > 600:
            self.kill()
    def update(self):
        self.animation()
        self.moving()
        self.destroy()

# coins #
class Coin(pygame.sprite.Sprite):
    def __init__(self, side):
        super().__init__()
        self.side = side
        self.frames = [pygame.image.load("graphics/items/coin/coin_1.png").convert_alpha(),
                       pygame.image.load("graphics/items/coin/coin_2.png").convert_alpha(),
                       pygame.image.load("graphics/items/coin/coin_3.png").convert_alpha(),
                       pygame.image.load("graphics/items/coin/coin_4.png").convert_alpha(),
                       pygame.image.load("graphics/items/coin/coin_5.png").convert_alpha(),
                       pygame.image.load("graphics/items/coin/coin_6.png").convert_alpha(),
                       pygame.image.load("graphics/items/coin/coin_7.png").convert_alpha(),
                       pygame.image.load("graphics/items/coin/coin_8.png").convert_alpha(),
                       pygame.image.load("graphics/items/coin/coin_9.png").convert_alpha(),
                       pygame.image.load("graphics/items/coin/coin_10.png").convert_alpha()]
        if self.side == "left":
            self.x = 96
        else:
            self.x = 655
        self.swing = random.randint(1,6)
        self.y = 110
        self.framecounter = 0
        self.collected = False
    def animation(self):
        self.rect = self.frames[0].get_rect(topleft=(self.x, self.y))
        screen.blit(self.frames[round(self.framecounter)], self.rect)
        if round(self.framecounter + 0.6) > 9:
            self.framecounter = 0
        else:
            self.framecounter += 0.6
    def moving(self):
        if self.side == "left":
            self.x += round(self.swing)
        else:
            self.x -= round(self.swing)
        if self.swing <= 0:
            self.swing = 0
        else: self.swing -= 0.01
        self.y += 2
    def got_collected(self):
        self.collected = True
    def destroy(self):
        if self.y > 600:
            self.kill()
        if self.collected:
            self.kill()
    def update(self):
        self.animation()
        self.moving()
        self.destroy()

# bags #
class Bag(pygame.sprite.Sprite):
    def __init__(self, side):
        super().__init__()
        self.side = side
        self.img = pygame.image.load("graphics/items/bag/coinbag.png").convert_alpha()
        if self.side == "left":
            self.x = 96
        else:
            self.x = 655
        self.swing = random.randint(2, 4)
        self.y = 110
        self.collected = False
    def draw(self):
        self.rect = self.img.get_rect(topleft=(self.x, self.y))
        screen.blit(self.img, self.rect)
    def moving(self):
        if self.side == "left":
            self.x += round(self.swing)
        else:
            self.x -= round(self.swing)
        if self.swing <= 0:
            self.swing = 0
        else: self.swing -= 0.01
        self.y += 5
    def got_collected(self):
        self.collected = True
    def destroy(self):
        if self.y > 600:
            self.kill()
        if self.collected:
            self.kill()
    def update(self):
        self.draw()
        self.moving()
        self.destroy()

## koopas ##
class Koopa(pygame.sprite.Sprite):
    def __init__(self, side):
        super().__init__()
        self.side = side
        if self.side == "left":
            self.frames = [pygame.image.load("graphics/koopas/l_koopa1.png").convert_alpha(),
                           pygame.image.load("graphics/koopas/l_koopa2.png").convert_alpha()]
            self.x = 71
        else:
            self.frames = [pygame.image.load("graphics/koopas/r_koopa1.png").convert_alpha(),
                           pygame.image.load("graphics/koopas/r_koopa2.png").convert_alpha()]
            self.x = 665
        self.y = 682
        self.frame = 0
    def animation(self):
        if self.y <= 110:
            self.frame = 1
    def moving(self):
        self.y -= 14
    def draw(self):
        self.rect = self.frames[self.frame].get_rect(topleft=(self.x, self.y))
        screen.blit(self.frames[self.frame], self.rect)
    def koopa_at_pos(self):
        if self.y <= 120 and self.y > 106:
            global koopa_at_pos
            koopa_at_pos = True
    def destroy(self):
        if self.y <= -82:
            self.kill()
    def update(self):
        self.animation()
        self.draw()
        self.moving()
        self.koopa_at_pos()
        self.destroy()

## bg ##
# wall #
class Wallframes:
    def __init__(self):
        self.imgs = [pygame.image.load("graphics/bg/wall/bg0.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg1.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg2.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg3.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg4.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg5.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg6.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg7.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg8.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg9.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg10.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg11.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg12.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg13.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg14.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg15.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg16.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg17.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg18.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg19.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg20.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg21.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg22.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg23.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg24.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg25.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg26.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg27.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg28.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg29.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg30.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg31.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg32.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg33.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg34.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg35.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg36.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg37.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg38.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg39.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg40.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg41.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg42.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg43.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg44.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg45.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg46.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg47.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg48.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg49.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg50.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg51.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg52.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg53.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg54.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg55.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg56.png").convert_alpha(), pygame.image.load("graphics/bg/wall/bg57.png").convert_alpha(),
                     pygame.image.load("graphics/bg/wall/bg58.png").convert_alpha()]
bg_wall = Wallframes()
bg_wall_framecounter = 0
bg_wall_framecounter_add = 1

def wall_bg_frames():
    global bg_wall_framecounter, bg_wall_framecounter_add
    screen.blit(bg_wall.imgs[bg_wall_framecounter], (0,0))
    if bg_wall_framecounter + bg_wall_framecounter_add > 58:
        bg_wall_framecounter = 0
    else: bg_wall_framecounter += bg_wall_framecounter_add

# clouds big #
class CloudBig(pygame.sprite.Sprite):
    def __init__(self, side):
        super().__init__()
        self.image = pygame.image.load("graphics/bg/clouds/big/cloud_big.png").convert_alpha()
        self.side = side
        if self.side == "left":
            self.turnL = False
            self.turnR = True
        else:
            self.turnL = True
            self.turnR = False
        if self.side == "left":
            self.x = -262
            self.y = 960
        else:
            self.x = 568
            self.y = 990
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
    def moving(self):
        screen.blit(self.image, (self.x, self.y))
        if self.side == "left":     # left clouds
            if self.turnR:
                if self.x + 3 > -162:
                    self.turnR = False
                    self.turnL = True
                self.x += 3
            elif self.turnL:
                if self.x - 3 <= -262:
                    self.turnL = False
                    self.turnR = True
                self.x -= 3
            self.y -= 10
        else:                       # right clouds
            if self.turnR:
                if self.x + 3 > 568:
                    self.turnR = False
                    self.turnL = True
                self.x += 3
            elif self.turnL:
                if self.x - 3 <= 468:
                    self.turnL = False
                    self.turnR = True
                self.x -= 3
            self.y -= 10
    def destroy(self):
        if self.y < -355:
            self.kill()
    def update(self):
        self.moving()
        self.destroy()

# clouds cute #
class CloudCute(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = [pygame.image.load("graphics/bg/clouds/cute/cloud_cute0.png").convert_alpha(),
                      pygame.image.load("graphics/bg/clouds/cute/cloud_cute1.png").convert_alpha(),
                      pygame.image.load("graphics/bg/clouds/cute/cloud_cute2.png").convert_alpha(),
                      pygame.image.load("graphics/bg/clouds/cute/cloud_cute3.png").convert_alpha()]
        self.x = random.randint(133, 458)
        self.y = 690
        self.framecounter = 0
        self.growing = False
        self.shrinking = True
    def animation(self):
        self.rect = self.frames[round(self.framecounter)].get_rect(topleft=(self.x, self.y))
        screen.blit(self.frames[round(self.framecounter)], self.rect)
        if self.shrinking and round(self.framecounter + 0.2) >= 4:
            self.shrinking = False
            self.growing = True
        elif self.growing and round(self.framecounter - 0.2) <= -1:
            self.growing = False
            self.shrinking = True
        if self.shrinking:
            self.framecounter += 0.2
        elif self.growing:
            self.framecounter -= 0.2
    def moving(self):
        self.y -= 12
    def destroy(self):
        if self.y < -90:
            self.kill()
    def update(self):
        self.animation()
        self.moving()
        self.destroy()

# tendrils #
bg_tendril_left_surf = pygame.image.load("graphics/bg/tendrils/tendril_left.png").convert_alpha()
bg_tendril_left_y = -36
bg_tendril_right_surf = pygame.image.load("graphics/bg/tendrils/tendril_right.png").convert_alpha()
bg_tendril_right_y = -36

def tendril_bg_frames():
    global bg_tendril_left_y, bg_tendril_right_y
    bg_tendril_left_rect = bg_tendril_left_surf.get_rect(topleft=(-4, bg_tendril_left_y))
    bg_tendril_right_rect = bg_tendril_left_surf.get_rect(topleft=(668, bg_tendril_right_y))
    screen.blit(bg_tendril_left_surf, bg_tendril_left_rect)
    screen.blit(bg_tendril_right_surf, bg_tendril_right_rect)
    if bg_tendril_left_y - 14 < -316:
        bg_tendril_left_y = -36
    else: bg_tendril_left_y -= 14
    if bg_tendril_right_y - 14 < -316:
        bg_tendril_right_y = -36
    else: bg_tendril_right_y -= 14

## groups ##
clouds_big_grp = pygame.sprite.Group()
clouds_cute_grp = pygame.sprite.Group()
hammer_grp = pygame.sprite.Group()
coin_grp = pygame.sprite.Group()
bag_grp = pygame.sprite.Group()
koopa_grp = pygame.sprite.Group()

## timers ##
clouds_big_timer = pygame.USEREVENT + 1
pygame.time.set_timer(clouds_big_timer, 1200)
l_big_cloud = False
r_big_cloud = True
clouds_cute_timer = pygame.USEREVENT + 2
pygame.time.set_timer(clouds_cute_timer, 500)
koopa_timer = pygame.USEREVENT +3

## game restart function ##
def game_restart():
    global bg_tendril_left_y, bg_tendril_right_y, bg_wall_framecounter, koopaside, itemside, koopa_at_pos, game_active, limit_time, PP_menu
    PP_menu.title_music.stop()
    PP_menu.score_music.stop()
    PP_menu.title_music_played = False
    PP_menu.score_music_played = False
    PP_menu.menu_change()
    PP_menu.sfx_score_screen_played = False
    hammer_grp.empty()
    coin_grp.empty()
    bag_grp.empty()
    koopa_grp.empty()
    clouds_cute_grp.empty()
    clouds_big_grp.empty()
    bg_tendril_left_y = -36
    bg_tendril_right_y = -36
    bg_wall_framecounter = 0
    koopaside = "left"
    itemside = "left"
    koopa_at_pos = False
    game_active = True
    limit_time = (pygame.time.get_ticks() / 1000)
    player1.player_reset()
    if numb_of_players > 1:
        player2.player_reset()
    if numb_of_players > 2:
        player3.player_reset()
    if numb_of_players > 3:
        player4.player_reset()
    pygame.time.set_timer(koopa_timer, 1757)

if __name__ == "__main__":
    ### Gameloop ###
    game_active = False
    first_start = True
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if game_active:
                if event.type == clouds_big_timer:
                    if l_big_cloud != True:
                        r_big_cloud = False
                        clouds_big_grp.add(CloudBig("left"))
                        l_big_cloud = True
                    else:
                        l_big_cloud = False
                        clouds_big_grp.add(CloudBig("right"))
                        r_big_cloud = True
                if event.type == clouds_cute_timer:
                    if random.randint(0,10) > 7:
                        clouds_cute_grp.add(CloudCute())
                if event.type == koopa_timer:
                    koopa_grp.add(Koopa(koopaside))
                    if koopaside == "left":
                        koopaside = "right"
                    else: koopaside = "left"
                if koopa_at_pos:
                    itemnumb = random.randint(0,10)
                    if itemnumb <= 3:
                        coin_grp.add(Coin(itemside))
                    elif itemnumb > 3 and itemnumb <=6:
                        hammer_grp.add(Hammer(itemside))
                        sfx_hammer_thrown.play()
                    elif itemnumb > 6 and itemnumb <=8:
                        bag_grp.add(Bag(itemside))
                    elif itemnumb > 8 and itemnumb <=9:
                        coin_grp.add(Coin(itemside))
                        hammer_grp.add(Hammer(itemside))
                        sfx_hammer_thrown.play()
                    elif itemnumb == 10:
                        coin_grp.add(Coin(itemside))
                        hammer_grp.add(Hammer(itemside))
                        bag_grp.add(Bag(itemside))
                        sfx_hammer_thrown.play()
                    if itemside == "left":
                        itemside = "right"
                    else: itemside = "left"
                    koopa_at_pos = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s and player1.falling_state and player1.hitted_state != True:
                        player1.falling_state = False
                    elif event.key == pygame.K_s and player1.falling_state != True:
                        player1.falling_state = True
                    if numb_of_players > 1:
                        if event.key == pygame.K_k and player2.falling_state and player2.hitted_state != True:
                            player2.falling_state = False
                        elif event.key == pygame.K_k and player2.falling_state != True:
                            player2.falling_state = True
                    if numb_of_players > 2:
                        if event.key == pygame.K_DOWN and player3.falling_state and player3.hitted_state != True:
                            player3.falling_state = False
                        elif event.key == pygame.K_DOWN and player3.falling_state != True:
                            player3.falling_state = True
                    if numb_of_players > 3:
                        if event.key == pygame.K_KP5 and player4.falling_state and player4.hitted_state != True:
                            player4.falling_state = False
                        elif event.key == pygame.K_KP5 and player4.falling_state != True:
                            player4.falling_state = True
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and PP_menu.which_menu == "numb_of_players":
                        PP_menu.menu_cursor.menu_update()
                        numb_of_players = PP_menu.menu_cursor.number_of_players
                    elif event.key == pygame.K_RETURN and (PP_menu.which_menu == "control_mapping" or PP_menu.which_menu == "score_screen"): # game retry
                        game_restart()
                        first_start = False
                        game_music.play(loops=-1)
                    elif event.key == pygame.K_SPACE and PP_menu.which_menu == "score_screen": # full game restart
                        game_restart()
                        PP_menu.char_selected_reset()
                        first_start = True
                        game_active = False
                    if PP_menu.which_menu == "numb_of_players":
                        PP_menu.menu_cursor.pressed = False
                    elif PP_menu.which_menu == "char_select":
                        PP_menu.p1_char_select.pressed = False
                        if numb_of_players > 1:
                            PP_menu.p2_char_select.pressed = False
                            if numb_of_players > 2:
                                PP_menu.p3_char_select.pressed = False
                                if numb_of_players > 3:
                                    PP_menu.p4_char_select.pressed = False


        if game_active:

            if pygame.time.get_ticks() - player1.collision_time > 1500:     # end of inv. frames after 1.5 seconds
                player1.collision_immune = False
            if numb_of_players > 1:
                if pygame.time.get_ticks() - player2.collision_time > 1500:
                    player2.collision_immune = False
            if numb_of_players > 2:
                if pygame.time.get_ticks() - player3.collision_time > 1500:
                    player3.collision_immune = False
            if numb_of_players > 3:
                if pygame.time.get_ticks() - player4.collision_time > 1500:
                    player4.collision_immune = False

            wall_bg_frames()
            clouds_big_grp.update()
            clouds_cute_grp.update()

            tendril_bg_frames()

            koopa_grp.update()
            coin_grp.update()
            bag_grp.update()

            player1.player_update()
            if numb_of_players > 1:
                player2.player_update()
            if numb_of_players > 2:
                player3.player_update()
            if numb_of_players > 3:
                player4.player_update()

            hammer_grp.update()

            display_time()

            player_collision()


            if player1.collision_immune != True:
                if pygame.sprite.spritecollide(player1, coin_grp, True):
                    player1.coins += 1
                    sfx_coin.play()
                    player1.got_coin.play()
                if pygame.sprite.spritecollide(player1, bag_grp, True):
                    player1.coins += 3
                    sfx_bag.play()
                    player1.got_coin.play()
            if numb_of_players > 1:
                if player2.collision_immune != True:
                    if pygame.sprite.spritecollide(player2, coin_grp, True):
                        player2.coins += 1
                        sfx_coin.play()
                        player2.got_coin.play()
                    if pygame.sprite.spritecollide(player2, bag_grp, True):
                        player2.coins += 3
                        sfx_bag.play()
                        player2.got_coin.play()
            if numb_of_players > 2:
                if player3.collision_immune != True:
                    if pygame.sprite.spritecollide(player3, coin_grp, True):
                        player3.coins += 1
                        sfx_coin.play()
                        player3.got_coin.play()
                    if pygame.sprite.spritecollide(player3, bag_grp, True):
                        player3.coins += 3
                        sfx_bag.play()
                        player3.got_coin.play()
            if numb_of_players > 3:
                if player4.collision_immune != True:
                    if pygame.sprite.spritecollide(player4, coin_grp, True):
                        player4.coins += 1
                        sfx_coin.play()
                        player4.got_coin.play()
                    if pygame.sprite.spritecollide(player4, bag_grp, True):
                        player4.coins += 3
                        sfx_bag.play()
                        player4.got_coin.play()

            if pygame.sprite.spritecollideany(player1, hammer_grp) and player1.collision_immune != True:     # player 1 : hitted by hammer
                if random.randint(1,10) >= 5:
                    sfx_hammer_hit1.play()
                else: sfx_hammer_hit2.play()
                player1.hitted.play()
                player1.hitted_state = True
                player1.falling_state = True
                player1.collision_immune = True
                player1.collision_time = pygame.time.get_ticks()
            if numb_of_players > 1:
                if pygame.sprite.spritecollideany(player2, hammer_grp) and player2.collision_immune != True:  # player 2 : hitted by hammer
                    if random.randint(1, 10) >= 5:
                        sfx_hammer_hit1.play()
                    else:
                        sfx_hammer_hit2.play()
                    player2.hitted.play()
                    player2.hitted_state = True
                    player2.falling_state = True
                    player2.collision_immune = True
                    player2.collision_time = pygame.time.get_ticks()
            if numb_of_players > 2:
                if pygame.sprite.spritecollideany(player3, hammer_grp) and player3.collision_immune != True:  # player 3 : hitted by hammer
                    if random.randint(1, 10) >= 5:
                        sfx_hammer_hit1.play()
                    else:
                        sfx_hammer_hit2.play()
                    player3.hitted.play()
                    player3.hitted_state = True
                    player3.falling_state = True
                    player3.collision_immune = True
                    player3.collision_time = pygame.time.get_ticks()
            if numb_of_players > 3:
                if pygame.sprite.spritecollideany(player4, hammer_grp) and player4.collision_immune != True:  # player 4 : hitted by hammer
                    if random.randint(1, 10) >= 5:
                        sfx_hammer_hit1.play()
                    else:
                        sfx_hammer_hit2.play()
                    player4.hitted.play()
                    player4.hitted_state = True
                    player4.falling_state = True
                    player4.collision_immune = True
                    player4.collision_time = pygame.time.get_ticks()

        else:   # menu screens

            if first_start:

                if PP_menu.title_music_played != True:
                    game_music.stop()
                    PP_menu.title_music.play(loops=-1)
                    PP_menu.title_music_played = True

                if PP_menu.which_menu == "numb_of_players":
                    PP_menu.display_menu_numb_of_players()
                    PP_menu.menu_cursor.menu_update()
                elif PP_menu.which_menu == "char_select":
                    PP_menu.display_char_select()
                    PP_menu.char_select_rect()
                    PP_menu.p1_char_select.menu_update()
                    if PP_menu.p1_char:
                        player1 = Player(1,PP_menu.p1_char_select.character)
                        if numb_of_players == 1 and PP_menu.p1_char:
                            PP_menu.menu_change()
                    if numb_of_players > 1:
                        PP_menu.p2_char_select.menu_update()
                        if PP_menu.p2_char:
                            player2 = Player(2,PP_menu.p2_char_select.character)
                            if numb_of_players == 2 and PP_menu.p1_char and PP_menu.p2_char:
                                PP_menu.menu_change()
                        if numb_of_players > 2:
                            PP_menu.p3_char_select.menu_update()
                            if PP_menu.p3_char:
                                player3 = Player(3, PP_menu.p3_char_select.character)
                                if numb_of_players == 3 and PP_menu.p1_char and PP_menu.p2_char and PP_menu.p3_char:
                                    PP_menu.menu_change()
                            if numb_of_players > 3:
                                PP_menu.p4_char_select.menu_update()
                                if PP_menu.p4_char:
                                    player4 = Player(4, PP_menu.p4_char_select.character)
                                    if numb_of_players == 4 and PP_menu.p1_char and PP_menu.p2_char and PP_menu.p3_char and PP_menu.p4_char:
                                        PP_menu.menu_change()
                elif PP_menu.which_menu == "control_mapping":
                    PP_menu.display_control_mapping()

            else:

                if PP_menu.score_music_played != True:
                    game_music.stop()
                    PP_menu.score_music.play(loops=-1)
                    PP_menu.score_music_played = True

                coins_message_surf_p1 = mario64_font.render("P1: " + str(player1.coins) + " coins", False, (25, 25, 25))
                coins_message_rect_p1 = coins_message_surf_p1.get_rect(center=(400, 60))
                if numb_of_players > 1:
                    coins_message_surf_p2 = mario64_font.render("P2: " + str(player2.coins) + " coins", False,
                                                                (25, 25, 25))
                    coins_message_rect_p2 = coins_message_surf_p2.get_rect(center=(400, 130))
                if numb_of_players > 2:
                    coins_message_surf_p3 = mario64_font.render("P3: " + str(player3.coins) + " coins", False,
                                                                (25, 25, 25))
                    coins_message_rect_p3 = coins_message_surf_p3.get_rect(center=(400, 200))
                if numb_of_players > 3:
                    coins_message_surf_p4 = mario64_font.render("P4: " + str(player4.coins) + " coins", False,
                                                                (25, 25, 25))
                    coins_message_rect_p4 = coins_message_surf_p4.get_rect(center=(400, 270))

                PP_menu.display_score_screen()

                screen.blit(coins_message_surf_p1, coins_message_rect_p1)
                if numb_of_players > 1:
                    screen.blit(coins_message_surf_p2, coins_message_rect_p2)
                if numb_of_players > 2:
                    screen.blit(coins_message_surf_p3, coins_message_rect_p3)
                if numb_of_players > 3:
                    screen.blit(coins_message_surf_p4, coins_message_rect_p4)


        pygame.display.update()
        clock.tick(fps)
