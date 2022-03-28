import sys
import pygame
from pygame.locals import KEYDOWN, QUIT, K_q, K_ESCAPE, MOUSEBUTTONDOWN
from manager import Manager, TreeManager
from sounds import Sounds

# Initialize game
pygame.init()
pygame.mixer.init()
pygame.display.set_caption('开心消消乐')
pygame.mouse.set_visible(False)

tree = TreeManager()
m = Manager(0, 0)
sound_sign = 0
world_bgm = pygame.mixer.Sound(Sounds.world_bgm)
game_bgm = pygame.mixer.Sound(Sounds.game_bgm)

# This improves the performance of the game
get_events, update_window = pygame.event.get, pygame.display.flip

while True:
    if m.level == 0:
        if sound_sign == 0:
            game_bgm.stop()
            world_bgm.play(-1)
            sound_sign = 1
    else:
        if sound_sign == 1:
            world_bgm.stop()
            game_bgm.play(-1)
            sound_sign = 0
    if m.level == 0:
        tree.draw_tree(m.energy_num, m.money)
    else:
        m.set_level_mode(m.level)
        sprite_group = m.draw()
        if m.type == 0:
            m.eliminate_animal()
            m.death_map()
            m.swap(sprite_group)
        m.judge_level()

    for event in get_events():
        if event.type == KEYDOWN:
            if event.key == K_q or event.key == K_ESCAPE:
                sys.exit()
        elif event.type == QUIT:
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            if m.level == 0:
                tree.mouse_select(m, mousex, mousey, m.level, m.energy_num, m.money)
            m.mouse_select(mousex, mousey)

    m.mouse_image()
    update_window()
