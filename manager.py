from random import randint
import pygame
from pygame.locals import *
from pygame.time import delay
from sprites import Tree, Board, Element
from sounds import Sounds, playSound

class TreeManager:
    '''Tree manager.'''
    __screen_size = (900, 600)
    screen = pygame.display.set_mode(__screen_size, DOUBLEBUF, 32)
    fruit_list = []
    fruit_image = pygame.image.load(Tree.fruit).convert_alpha()
    fruit_width = fruit_image.get_width()
    fruit_height = fruit_image.get_height()
    type = 0 # 0 Tree, 1 Energy
    energy_full = False # Energy full mark
    money_empty = False # Not any money left?

    def display_text(self, text, position, txt_size=25, txt_color=(255, 255, 255)):
        '''Display text with given position, size and color.'''
        my_font = pygame.font.SysFont(None, txt_size)
        text_screen = my_font.render(text, True, txt_color)
        self.screen.blit(text_screen, position)

    def draw_tree(self, energy_num, money_num):
        '''Draws the game tree.'''
        Tree(Tree.tree, (0, 600)).draw(self.screen) # Draw tree
        Tree(Tree.energy_num, Tree.energy_num_position).draw(self.screen) # Draw energy num
        if energy_num > 30:
            self.display_text(str(30) + '/30', (22, 55), 21)
        else:
            self.display_text(str(energy_num)+'/30', (22, 55), 21)
        Tree(Tree.money, (15, 135)).draw(self.screen) # Draw money
        self.display_text(str(money_num), (32, 124), 21)
        for i in range(0, 10): # Draw fruits
            Tree(Tree.fruit, Tree.position[i]).draw(self.screen)
            self.display_text(str(i+1), (Tree.position[i][0]+15, Tree.position[i][1]-47))
        if self.type == 1:
            Tree(Tree.energy_buy, Tree.energy_buy_position).draw(self.screen)
            if self.energy_full:
                self.display_text('energy is full!', (430, 310), 30, (255, 0, 0))
                pygame.display.flip()
                delay(500)
                self.energy_full = False
            if self.money_empty:
                self.display_text('money is not enough!', (410, 310), 30, (255, 0, 0))
                pygame.display.flip()
                delay(500)
                self.money_empty = False

    def mouse_select(self, mgr, mousex, mousey, level, energy_num, money_num):
        '''Handle mouse event.'''
        if self.type == 0: # Tree Scene
            for i in range(0, 10):
                if Tree.position[i][0] < mousex < Tree.position[i][0] + self.fruit_width \
                        and Tree.position[i][1] - self.fruit_height < mousey < Tree.position[i][1]:
                    if energy_num <= 0:
                        self.type = 1
                    else:
                        level = i + 1
            if Tree.energy_num_position[0] < mousex < Tree.energy_num_position[0] + 60 \
                    and Tree.energy_num_position[1] - 60 < mousey < Tree.energy_num_position[1]: # 精力60*60
                playSound(Sounds.click)
                self.type = 1
        else: # Energy Scene
            if 408 < mousex < 600 and 263 < mousey < 313: # "Buy Energy" button clicked
                playSound(Sounds.click_button)
                if money_num < 50:
                    self.money_empty = True
                if energy_num >= 30:
                    self.energy_full = True
                elif energy_num < 30 and money_num >= 50:
                    energy_num += 5
                    money_num -= 50
            elif 619 < mousex < 638 and 158 < mousey < 177: # "X" clicked
                self.type = 0
        mgr.level, mgr.energy_num, mgr.money = level, energy_num, money_num

class Manager:
    '''Game manager.'''
    __screen_size = (900, 600)
    screen = pygame.display.set_mode(__screen_size, DOUBLEBUF, 32)
    __brick_size = 50
    __bg = pygame.image.load('img/bg.png').convert()
    stop_width = 63
    selected = [-1, -1] # Current selected [row, col]
    swap_sign = -1 # Swap sign
    last_sel = [-1, -1] # Last selected [row, col]
    value_swapped = False # Swapped?
    death_sign = True # Death map sign
    boom_sel = [-1, -1] # Eliminate 4: [row, col]
    level = 0 # Current level, 0 for tree
    money = 100 # Money
    energy_num = 30 # Energy num
    num_sign = True
    type = 2 # (0) Playing, (1) Passed, (-1) Failed, (2) Tree
    reset_mode = True # Reset layout?
    init_step = 15 # Initial steps for each level
    step = init_step # Steps left of the game
    score = 0 # Score
    min = 20 # Medium score 1
    max = 50 # Medium score 2
    animal_num = [0, 0, 0, 0, 0, 0] # Number of eliminated animals
    ice_num = 0 # Number left of required ice
    success_board = Board(Board.success, [200, 0]) # Success board
    fail_board = Board(Board.fail, [200, 0]) # Failure board
    height, width = 9, 9
    row, col = 5, 5
    ice_list = [[-1 for _ in range(21)] for _ in range(21)] # (-1) None, (1) Ice
    animal = [[-1 for _ in range(21)] for _ in range(21)] # (-2) Elimated, (-1) None, (0-4) Animal
    list_x, list_y = (__screen_size[0] - 11 * __brick_size) / 2, (__screen_size[1] - 11 * __brick_size) / 2 # Position of the blocks

    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.list_x = (Manager.__screen_size[0] - self.width * Manager.__brick_size) / 2
        self.list_y = (Manager.__screen_size[1] - self.height * Manager.__brick_size) / 2
        self.row, self.col = Manager.xy_rc(self.list_x, self.list_y)
        self.list_x, self.list_y = Manager.rc_xy(self.row, self.col)
        self.ice_list = [[-1 for _ in range(21)] for _ in range(21)]
        self.animal = [[-1 for _ in range(21)] for _ in range(21)]
        self.reset_animal()

    def reset_animal(self):
        for row in range(self.row, self.row + self.height):
            for col in range(self.col, self.col + self.width):
                self.animal[row][col] = randint(0, 5)

    @staticmethod
    def rc_xy(row, col):
        '''(row, col) -> (x, y)'''
        return int(Manager.list_x + (col-Manager.col)*Manager.__brick_size), int\
            (Manager.list_y+(row-Manager.row)*Manager.__brick_size)

    @staticmethod
    def xy_rc(x, y):
        '''(x, y) -> (row, col)'''
        return int((y-Manager.list_y)/Manager.__brick_size+Manager.row), int\
            ((x-Manager.list_x)/Manager.__brick_size+Manager.col)

    @staticmethod
    def draw_brick(x, y):
        brick = Element(Element.brick, (x, y))
        Manager.screen.blit(brick.image, brick.rect)

    def draw_task(self, task_animal_num, which_animal, \
                  board_position=(400, 90), animal_position=(430, 35), txt_position=(455, 60)):
        '''Draw task board'''
        txt_size = 24
        txt_color = (0, 0, 0)
        Board(Board.task_board, board_position).draw(self.screen)
        if which_animal == 6:
            task_animal = Element(Element.ice, animal_position)
        else:
            task_animal = Element(Element.animals[which_animal], animal_position)
        task_animal.image = pygame.transform.smoothscale(task_animal.image, (40, 40))
        task_animal.draw(self.screen)
        if which_animal == 6:
            if task_animal_num-self.ice_num <= 0:
                Board(Board.ok, (txt_position[0], txt_position[1]+15)).draw(self.screen)
            else:
                self.load_text(str(task_animal_num-self.ice_num), txt_position, txt_size, txt_color)
        else:
            if task_animal_num - self.animal_num[which_animal] <= 0:
                Board(Board.ok, (txt_position[0], txt_position[1]+15)).draw(self.screen)
            else:
                self.load_text(str(task_animal_num - self.animal_num[which_animal]), txt_position, txt_size, txt_color)

    def draw(self):
        '''Draw background, animals, and so on.'''
        # Draw background
        self.screen.blit(Manager.__bg, (0, 0))
        # Display steps left
        Board(Board.step_board, (0, 142)).draw(self.screen)
        tens, single = divmod(self.step, 10)
        if tens == 0:
            Board(Board.num_format%single, (790, 110)).draw(self.screen)
        else:
            Board(Board.num_format%tens, (775, 110)).draw(self.screen)
            Board(Board.num_format%single, (805, 110)).draw(self.screen)
        # Display level & pause button
        Board(Board.level_format%self.level, (30, 105)).draw(self.screen)
        Element(Element.stop, Element.stop_position).draw(self.screen)

        # Draw bricks, ice and animals
        brick_group = pygame.sprite.Group()
        animal_group = pygame.sprite.Group()
        ice_group = pygame.sprite.Group()
        for i in range(0, 21):
            for j in range(0, 21):
                x, y = Manager.rc_xy(i, j)
                if self.animal[i][j] != -1:
                    brick_group.add(Element(Element.brick, (x, y)))
                    animal_group.add(Element(Element.animals[self.animal[i][j]], (x, y)))
                if self.ice_list[i][j] != -1:
                    ice_group.add(Element(Element.ice, (x, y)))
        brick_group.draw(self.screen)
        ice_group.draw(self.screen)
        for animallist in animal_group:
            self.screen.blit(animallist.image, animallist.rect)
        if self.level == 1:
            self.draw_task(10, 4)
        elif self.level == 2:
            self.draw_task(21, 1)
        elif self.level == 3:
            self.draw_task(16, 4, (300, 90), (330, 35), (360, 60))
            self.draw_task(16, 5, (500, 90), (530, 35), (560, 60))
        elif self.level == 4:
            self.draw_task(18, 5, (300, 90), (330, 35), (360, 60))
            self.draw_task(18, 2, (500, 90), (530, 35), (560, 60))
        elif self.level == 5:
            self.draw_task(28, 2, (300, 90), (330, 35), (360, 60))
            self.draw_task(28, 0, (500, 90), (530, 35), (560, 60))
        elif self.level == 6:
            self.draw_task(70, 4)
        elif self.level == 7:
            self.draw_task(36, 1)
            self.draw_task(36, 2, (300, 90), (330, 35), (360, 60))
            self.draw_task(36, 0, (500, 90), (530, 35), (560, 60))
        elif self.level == 8:
            self.draw_task(15, 6)
        elif self.level == 9:
            self.draw_task(49, 6)
        else:
            self.draw_task(39, 6)

        # Display selected animal
        if self.selected != [-1, -1]:
            frame_sprite = Element(Element.frame, Manager.rc_xy(self.selected[0], self.selected[1]))
            self.screen.blit(frame_sprite.image, frame_sprite.rect)

        # Show score
        self.load_text('Score:' + str(self.score), (300, 550), 30)
        pygame.draw.rect(self.screen, (50, 150, 50, 180), Rect(300, 570, self.score * 2, 25))
        pygame.draw.rect(self.screen, (100, 200, 100, 180), Rect(300, 570, 200, 25), 2)
        return animal_group

    def mouse_image(self):
        '''Replace the mouse image with img/mouse.png'''
        mouse_cursor = pygame.image.load('img/mouse.png').convert_alpha()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Find the topleft position of the mouse
        mouse_x -= mouse_cursor.get_width() / 2
        mouse_y -= mouse_cursor.get_height() / 2
        self.screen.blit(mouse_cursor, (mouse_x, mouse_y))

    def mouse_select(self, mousex, mousey):
        '''Handle mouse click event.'''
        if self.type == 1: # Passed
            if Board.button_position[0][0] < mousex < Board.button_position[0][0]+100 \
                    and Board.button_position[0][1] - 50 < mousey < Board.button_position[0][1]: # Clicked replay button
                if self.energy_num < 5:
                    self.level = 0
                self.reset_mode = True
            elif Board.button_position[1][0] < mousex < Board.button_position[1][0]+100 \
                    and Board.button_position[1][1]-50 < mousey < Board.button_position[1][1]: # Clicked next level button
                if self.level < 10:
                    if self.energy_num < 5:
                        self.level = 0
                    else:
                        self.level += 1
                    self.reset_mode = True
            elif 610 < mousex < 610 + 55 and 205 - 55 < mousey < 205: # x
                self.level = 0
                self.reset_mode = True

        elif self.type == -1: # Failed
            if Board.button_position[1][0] < mousex < Board.button_position[1][0]+100 \
                    and Board.button_position[1][1]-50 < mousey < Board.button_position[1][1]: # Clicked replay button
                if self.energy_num < 5:
                    self.level = 0
                self.reset_mode = True
            elif Board.button_position[0][0] < mousex < Board.button_position[0][0]+100 \
                    and Board.button_position[0][1]-50 < mousey < Board.button_position[0][1]: # Clicked 5 more steps button
                if self.money < 5:
                    self.level = 0
                else:
                    self.money -= 5
                    self.step += 5
                    self.type = 0 # Playing game
                    self.fail_board = Board(Board.fail, [200, 0])
            elif 610 < mousex < 610 + 55 and 205 - 55 < mousey < 205:
                self.level = 0
                self.reset_mode = True

        elif self.type == 0:
            if self.list_x < mousex < self.list_x + Manager.__brick_size * self.width \
                    and self.list_y < mousey < self.list_y + Manager.__brick_size * self.height:
                mouse_selected = Manager.xy_rc(mousex, mousey)
                if self.animal[mouse_selected[0]][mouse_selected[1]] != -1:
                    playSound(Sounds.click)
                    self.selected = mouse_selected
                    if (self.last_sel[0] == self.selected[0] and abs(self.last_sel[1] - self.selected[1]) == 1) \
                            or (self.last_sel[1] == self.selected[1] and abs(self.last_sel[0] - self.selected[0]) == 1):
                        self.swap_sign = 1 # Valid move, swap
            elif Element.stop_position[0] < mousex < Element.stop_position[0]+self.stop_width\
                    and Element.stop_position[1] < mousey < Element.stop_position[1]+self.stop_width: # Exit button clicked
                playSound(Sounds.click_button)
                self.level = 0
                self.reset_mode = True
            else:
                self.selected = [-1, -1]

    def swap(self, spritegroup):
        '''Swap two selected animals on the board.'''
        if self.swap_sign == -1: # Not swapped
            self.last_sel = self.selected
        if self.swap_sign == 1:
            last_x, last_y = Manager.rc_xy(self.last_sel[0], self.last_sel[1])
            sel_x, sel_y = Manager.rc_xy(self.selected[0], self.selected[1])
            if self.last_sel[0] == self.selected[0]: # Swap vertically
                for animallist in spritegroup:
                    if animallist.rect.topleft == (last_x, last_y):
                        last_sprite = animallist
                        last_sprite.speed = [self.selected[1]-self.last_sel[1], 0]
                    elif animallist.rect.topleft == (sel_x, sel_y):
                        selected_sprite = animallist
                        selected_sprite.speed = [self.last_sel[1]-self.selected[1], 0]
            else: # Swap horizontally
                for animallist in spritegroup:
                    if animallist.rect.topleft == (last_x, last_y):
                        last_sprite = animallist
                        last_sprite.speed = [0, self.selected[0]-self.last_sel[0]]
                    elif animallist.rect.topleft == (sel_x, sel_y):
                        selected_sprite = animallist
                        selected_sprite.speed = [0, self.last_sel[0]-self.selected[0]]
            while last_sprite.speed != [0, 0]:
                delay(5)
                self.draw_brick(last_x, last_y)
                self.draw_brick(sel_x, sel_y)
                last_sprite.move(last_sprite.speed)
                selected_sprite.move(selected_sprite.speed)
                self.screen.blit(last_sprite.image, last_sprite.rect)
                self.screen.blit(selected_sprite.image, selected_sprite.rect)
                pygame.display.flip()

            self.swap_values()
            if self.eliminate_animal():
                self.step -= 1
            else:
                self.swap_values()
            self.value_swapped = False
            self.boom_sel = self.selected
            self.swap_sign = -1
            self.selected = [-1, -1]

    def swap_values(self):
        '''Swap values.'''
        (xl, yl), (xc, yc) = self.last_sel, self.selected
        self.animal[xl][yl], self.animal[xc][yc] = self.animal[xc][yc], self.animal[xl][yl]

    def load_text(self, text, position, txt_size, txt_color=(255, 255, 255)):
        my_font = pygame.font.SysFont(None, txt_size)
        text_screen = my_font.render(text, True, txt_color)
        self.screen.blit(text_screen, position)

    def death_map(self):
        '''Checks if there is not a valid move.'''
        for i in range(self.row, self.row + self.height):
            for j in range(self.col, self.col + self.width):
                if self.animal[i][j] != -1:
                    if self.animal[i][j] == self.animal[i][j+1]:
                        if (self.animal[i][j] in [self.animal[i-1][j-1], self.animal[i+1][j-1]] \
                                    and self.animal[i][j-1] != -1) or \
                                (self.animal[i][j] in [self.animal[i-1][j+2], self.animal[i+1][j+2]] \
                                         and self.animal[i][j+2] != -1):
                            '''a     b
                                 a a
                               c     d'''
                            self.death_sign = False
                            break
                    if self.animal[i][j] == self.animal[i+1][j]:
                        if (self.animal[i][j] in [self.animal[i-1][j-1], self.animal[i-1][j+1]] \
                                    and self.animal[i-1][j] != -1) or \
                                (self.animal[i][j] in [self.animal[i+2][j - 1], self.animal[i+2][j + 1]] \
                                         and self.animal[i+2][j] != -1):
                            '''a   b
                                 a
                                 a
                               c   d'''
                            self.death_sign = False
                            break
                    else:
                        if self.animal[i-1][j-1] == self.animal[i][j]:
                            if (self.animal[i][j] == self.animal[i-1][j+1] and self.animal[i-1][j] != -1)\
                                    or (self.animal[i][j] == self.animal[i+1][j-1] and self.animal[i][j-1] != -1):
                                '''a   a      a   b
                                     a          a
                                   c          a    '''
                                self.death_sign = False
                                break
                        if self.animal[i][j] == self.animal[i+1][j+1]:
                            if (self.animal[i][j] == self.animal[i-1][j+1] and self.animal[i][j+1] != -1)\
                                    or (self.animal[i][j] == self.animal[i+1][j-1] and self.animal[i+1][j] != -1):
                                '''    a          b
                                     a          a
                                   b   a      a   a'''
                                self.death_sign = False
                                break
        if self.death_sign:
            delay(500)
            Element(Element.none_animal, (230, 150)).draw(self.screen)
            pygame.display.flip()
            delay(500)
            temp = [self.step, self.score, self.animal_num, self.ice_num, self.energy_num]
            self.reset_mode = True
            self.set_level_mode(self.level)
            self.step = temp[0]
            self.score = temp[1]
            self.animal_num = temp[2]
            self.ice_num = temp[3]
            self.energy_num = temp[4]
        else:
            self.death_sign = True

    # TODO: Merge 4 functions below
    def exists_left(self, i, j, num):
        '''Checks there are at least {num} continous same animals on the left side of (i, j).'''
        for t in range(0, num):
            if self.animal[i][j] != self.animal[i][j - t] or self.animal[i][j] < 0:
                return False
        return True

    def exists_right(self, i, j, num):
        '''Checks there are at least {num} continous same animals on the right side of (i, j).'''
        for t in range(0, num):
            if self.animal[i][j] != self.animal[i][j + t] or self.animal[i][j] < 0:
                return False
        return True

    def exists_up(self, i, j, num):
        '''Checks there are at least {num} continous same animals above (i, j).'''
        for t in range(0, num):
            if self.animal[i][j] != self.animal[i - t][j] or self.animal[i][j] < 0:
                return False
        return True

    def exists_down(self, i, j, num):
        '''Checks there are at least {num} continous same animals below (i, j).'''
        for t in range(0, num):
            if self.animal[i][j] != self.animal[i + t][j] or self.animal[i][j] < 0:
                return False
        return True

    # TODO: Merge 4 functions below
    def change_left(self, i, j, num):
        '''Change the left side of the animal.'''
        self.value_swapped = True
        self.score += num
        for k in range(0, int(num)):
            self.animal[i][j - k] = -2

    def change_right(self, i, j, num):
        '''Change the right side of the animal.'''
        self.value_swapped = True
        self.score += num
        for k in range(0, num):
            self.animal[i][j + k] = -2

    def change_up(self, i, j, num):
        '''Change above the animal.'''
        self.value_swapped = True
        self.score += num
        for k in range(0, num):
            self.animal[i-k][j] = -2

    def change_down(self, i, j, num):
        '''Change below the animal.'''
        self.value_swapped = True
        self.score += num
        for k in range(0, num):
            self.animal[i+k][j] = -2

    def eliminate_animal(self):
        score_level = self.score
        self.value_swapped = False
        for i in range(self.row, self.row + self.height):
            for j in range(self.col, self.col + self.width):
                # TODO: Simplify the if statement below
                if self.exists_right(i, j, 5):
                    self.value_swapped = True
                    if self.exists_down(i, j+2, 3):
                        self.animal_num[self.animal[i][j]] += 7
                        playSound(Sounds.eliminate_format%5) # Elimination sound 5
                        self.change_right(i, j, 5)
                        self.change_down(i, j+2, 3)
                    else:
                        self.animal_num[self.animal[i][j]] += 5
                        playSound(Sounds.eliminate_format%3) # Elimination sound 3
                        self.change_right(i, j, 5)
                elif self.exists_right(i, j, 4):
                    self.value_swapped = True
                    if self.exists_down(i, j+1, 3):
                        self.animal_num[self.animal[i][j]] += 6
                        playSound(Sounds.eliminate_format%4) # Elimination sound 4
                        self.change_right(i, j, 4)
                        self.change_down(i, j+1, 3)
                    elif self.exists_down(i, j+2, 3):
                        self.animal_num[self.animal[i][j]] += 6
                        playSound(Sounds.eliminate_format%4) # Elimination sound 4
                        self.change_right(i, j, 4)
                        self.change_down(i, j+2, 3)
                    else:
                        self.animal_num[self.animal[i][j]] += 4
                        playSound(Sounds.eliminate_format%2) # Elimination sound 2
                        self.change_right(i, j, 4)
                elif self.exists_right(i, j, 3):
                    self.value_swapped = True
                    if self.exists_down(i, j, 3):
                        self.animal_num[self.animal[i][j]] += 5
                        playSound(Sounds.eliminate_format%3) # Elimination sound 3
                        self.change_right(i, j, 3)
                        self.change_down(i, j, 3)
                    elif self.exists_down(i, j+1, 3):
                        self.animal_num[self.animal[i][j]] += 5
                        playSound(Sounds.eliminate_format%3) # Elimination sound 3
                        self.change_right(i, j, 3)
                        self.change_down(i, j+1, 3)
                    elif self.exists_down(i, j+2, 3):
                        self.animal_num[self.animal[i][j]] += 5
                        playSound(Sounds.eliminate_format%3) # Elimination sound 3
                        self.change_right(i, j, 3)
                        self.change_down(i, j + 2, 3)
                    else:
                        self.animal_num[self.animal[i][j]] += 3
                        playSound(Sounds.eliminate_format%1) # Elimination sound 1
                        self.change_right(i, j, 3)
                elif self.exists_down(i, j, 5):
                    self.value_swapped = True
                    if self.exists_right(i+2, j, 3):
                        self.animal_num[self.animal[i][j]] += 7
                        playSound(Sounds.eliminate_format%5) # Elimination sound 5
                        self.change_down(i, j, 5)
                        self.change_right(i+2, j, 3)
                    elif self.exists_left(i+2, j, 3):
                        self.animal_num[self.animal[i][j]] += 7
                        playSound(Sounds.eliminate_format%5) # Elimination sound 5
                        self.change_down(i, j, 5)
                        self.change_left(i+2, j, 3)
                    else:
                        self.animal_num[self.animal[i][j]] += 5
                        playSound(Sounds.eliminate_format%3) # Elimination sound 3
                        self.change_down(i, j, 5)
                elif self.exists_down(i, j, 4):
                    self.value_swapped = True
                    if self.exists_left(i+1, j, 3):
                        self.animal_num[self.animal[i][j]] += 6
                        playSound(Sounds.eliminate_format%4) # Elimination sound 4
                        self.change_down(i, j, 4)
                        self.change_left(i+1, j, 3)
                    elif self.exists_right(i+1, j, 3):
                        self.animal_num[self.animal[i][j]] += 6
                        playSound(Sounds.eliminate_format%4) # Elimination sound 4
                        self.change_down(i, j, 4)
                        self.change_right(i+1, j, 3)
                    elif self.exists_left(i+2, j, 3):
                        self.animal_num[self.animal[i][j]] += 6
                        playSound(Sounds.eliminate_format%4) # Elimination sound 4
                        self.change_down(i, j, 4)
                        self.change_left(i+2, j, 3)
                    elif self.exists_right(i+2, j, 3):
                        self.animal_num[self.animal[i][j]] += 6
                        playSound(Sounds.eliminate_format%4) # Elimination sound 4
                        self.change_down(i, j, 4)
                        self.change_right(i+2, j, 3)
                    else:
                        self.animal_num[self.animal[i][j]] += 4
                        playSound(Sounds.eliminate_format%2) # Elimination sound 2
                        self.change_down(i, j, 4)
                elif self.exists_down(i, j, 3):
                    self.value_swapped = True
                    if self.exists_left(i+1, j, 3):
                        self.animal_num[self.animal[i][j]] += 5
                        playSound(Sounds.eliminate_format%3) # Elimination sound 3
                        self.change_down(i, j, 3)
                        self.change_left(i+1, j, 3)
                    elif self.exists_right(i+1, j, 3):
                        self.animal_num[self.animal[i][j]] += 5
                        playSound(Sounds.eliminate_format%3) # Elimination sound 3
                        self.change_down(i, j, 3)
                        self.change_right(i+1, j, 3)
                    elif self.exists_left(i+2, j, 3):
                        self.animal_num[self.animal[i][j]] += 5
                        playSound(Sounds.eliminate_format%3) # Elimination sound 3
                        self.change_down(i, j, 3)
                        self.change_left(i+2, j, 3)
                    elif self.exists_right(i+2, j, 3):
                        self.animal_num[self.animal[i][j]] += 5
                        playSound(Sounds.eliminate_format%3) # Elimination sound 3
                        self.change_down(i, j, 3)
                        self.change_right(i+2, j, 3)
                    elif self.exists_left(i+2, j, 2) and self.exists_right(i+2, j, 2):
                        self.animal_num[self.animal[i][j]] += 5
                        playSound(Sounds.eliminate_format%3) # Elimination sound 3
                        self.change_down(i, j, 3)
                        self.change_left(i+2, j, 2)
                        self.change_right(i+2, j, 2)
                    elif self.exists_left(i+2, j, 2) and self.exists_right(i+2, j, 3):
                        self.animal_num[self.animal[i][j]] += 6
                        playSound(Sounds.eliminate_format%4) # Elimination sound 4
                        self.change_down(i, j, 3)
                        self.change_left(i+2, j, 2)
                        self.change_right(i+2, j, 3)
                    elif self.exists_left(i+2, j, 3) and self.exists_right(i+2, j, 2):
                        self.animal_num[self.animal[i][j]] += 6
                        playSound(Sounds.eliminate_format%4) # Elimination sound 4
                        self.change_down(i, j, 3)
                        self.change_left(i+2, j, 3)
                        self.change_right(i+2, j, 2)
                    elif self.exists_left(i+2, j, 3) and self.exists_right(i+2, j, 3):
                        self.animal_num[self.animal[i][j]] += 7
                        playSound(Sounds.eliminate_format%5) # Elimination sound 5
                        self.change_down(i, j, 3)
                        self.change_left(i+2, j, 3)
                        self.change_right(i+2, j, 3)
                    else:
                        self.animal_num[self.animal[i][j]] += 3
                        playSound(Sounds.eliminate_format%1) # Elimination sound 1
                        self.change_down(i, j, 3)

        self.fall_animal()
        score_level = self.score - score_level # Score level

        # Display & speak: good, great, amazing, excellent, unbelievable
        if score_level < 5: return self.value_swapped
        if score_level < 8: # 5 good
            playSound(Sounds.score_level[0])
            Element(Element.score_level[0], (350, 250)).draw(self.screen)
            pygame.display.flip()
            delay(500)
        elif score_level < 10: # 8 great
            playSound(Sounds.score_level[1])
            Element(Element.score_level[1], (350, 250)).draw(self.screen)
            pygame.display.flip()
            delay(500)
        elif score_level < 15: # 10 amazing
            playSound(Sounds.score_level[2])
            Element(Element.score_level[2], (350, 250)).draw(self.screen)
            pygame.display.flip()
            delay(500)
        elif score_level < 20: # 15 excellent
            playSound(Sounds.score_level[3])
            Element(Element.score_level[3], (350, 250)).draw(self.screen)
            pygame.display.flip()
            delay(500)
        elif score_level >= 20: # 20 unbelievable
            playSound(Sounds.score_level[4])
            Element(Element.score_level[4], (350, 250)).draw(self.screen)
            pygame.display.flip()
            delay(500)

        return self.value_swapped # Return the swap value sign

    def fall_animal(self):
        '''Animation of falling animals'''
        clock = pygame.time.Clock()
        position = []
        ice_position = []
        for i in range(self.row, self.row + self.height):
            for j in range(self.col, self.col + self.width):
                if self.animal[i][j] == -2:
                    x, y = self.rc_xy(i, j)
                    position.append((x, y))
                    if self.ice_list[i][j] == 1:
                        ice_position.append((x, y))
        if position:
            for index in range(0, 9):
                clock.tick(20)
                for pos in position:
                    self.draw_brick(pos[0], pos[1])
                    if pos in ice_position:
                        Element(Element.ice_format%index, (pos[0], pos[1])).draw(self.screen)
                    Element(Element.bling_format%index, (pos[0], pos[1])).draw(self.screen)
                    pygame.display.flip()
        for i in range(self.row, self.row + self.height):
            brick_position = []
            fall_animal_list = []
            speed = [0, 1]
            for j in range(self.col, self.col + self.width):
                if self.animal[i][j] == -2:
                    x, y = self.rc_xy(i, j)
                    if self.ice_list[i][j] == 1:
                        playSound(Sounds.ice_break)
                        self.ice_num += 1
                        self.ice_list[i][j] = -1

                    brick_position.append((x, y))

                    for m in range(i, self.row - 1, -1):
                        if self.animal[m - 1][j] != -1:
                            x, y = self.rc_xy(m - 1, j)
                            brick_position.append((x, y))
                            animal = Element(Element.animals[self.animal[m - 1][j]], (x, y))
                            fall_animal_list.append(animal)
                            self.animal[m][j] = self.animal[m - 1][j]
                        else:
                            self.animal[m][j] = randint(0, 5)
                            break
            while speed != [0, 0] and fall_animal_list:
                for position in brick_position:
                    self.draw_brick(position[0], position[1])
                for animal_sprite in fall_animal_list:
                    animal_sprite.move(speed)
                    animal_sprite.draw(self.screen)
                    speed = animal_sprite.speed
                pygame.display.flip()

    def judge_next(self, type, score):
        '''Check whether the next level is reached or not'''
        if type == 1: # Passed
            self.load_fns_window(score)
        elif type == -1: # Failed
            self.load_fail_window()

    def load_fail_window(self):
        '''Display the failure board and buttons'''
        sound_sign = 0
        step_add = Board(Board.step_add, Board.button_position[0]) # L: 5 more steps
        retry = Board(Board.replay, Board.button_position[1]) # R: Replay
        self.screen.blit(self.fail_board.image, self.fail_board.rect) # Failure board
        self.screen.blit(step_add.image, step_add.rect)
        self.screen.blit(retry.image, retry.rect)
        while self.fail_board.speed != [0, 0]:
            self.draw()
            self.screen.blit(self.fail_board.image, self.fail_board.rect)
            self.fail_board.move()
            pygame.display.flip()
            if sound_sign == 0:
                playSound(Sounds.board_sound)
                sound_sign = 1

    def load_fns_window(self, score):
        '''Display the success board, score and buttons'''
        sound_sign = 0
        replay = Board(Board.replay, Board.button_position[0]) # L: Replay
        self.screen.blit(self.success_board.image, self.success_board.rect) # Successful board
        if self.level < 10: # If not the last level
            next_level = Board(Board.next, Board.button_position[1]) # R: Next level
            self.screen.blit(next_level.image, next_level.rect)
        self.screen.blit(replay.image, replay.rect)
        while self.success_board.speed != [0, 0]:
            self.draw()
            self.screen.blit(self.success_board.image, self.success_board.rect)
            self.success_board.move()
            pygame.display.flip()
            if sound_sign == 0:
                playSound(Sounds.board_sound)
                sound_sign = 1
        self.displayStars(score) # Display the stars
        # Money
        self.load_text(str(self.score*2), (Board.starts_position[0][0]+75, Board.starts_position[0][0]+46), 20, (0, 0, 0))

    def displayStars(self, score):
        '''Display the stars according to the score.'''
        star1 = Board(Board.stars, Board.starts_position[0])
        star2 = Board(Board.stars, Board.starts_position[1])
        star3 = Board(Board.stars, Board.starts_position[2])
        if 0 <= score < self.min:
            self.load_text('1', (Board.starts_position[1][0]+48, Board.starts_position[1][1]+35), 20, (0, 0, 0))
            self.screen.blit(star1.image, star1.rect)
        elif self.min <= score <= self.max:
            self.load_text('2', (Board.starts_position[1][0] + 48, Board.starts_position[1][1] + 35), 20, (0, 0, 0))
            self.screen.blit(star1.image, star1.rect)
            self.screen.blit(star2.image, star2.rect)
        elif score > self.max:
            self.load_text('5', (Board.starts_position[1][0] + 48, Board.starts_position[1][1] + 35), 20, (0, 0, 0))
            self.screen.blit(star1.image, star1.rect)
            self.screen.blit(star2.image, star2.rect)
            self.screen.blit(star3.image, star3.rect)
        pygame.display.flip()

    def set_level_mode(self, level):
        '''Set the level mode and its steps.'''
        self.level = level
        if self.reset_mode: # If it is required to reset the mode
            self.num_sign = True
            if level == 1:
                self.__init__(7, 7)
                self.animal[7][9] = self.animal[7][10] = self.animal[7][11] = self.animal[8][10] = self.animal[11][7] = \
                    self.animal[11][13] = self.animal[12][7] = self.animal[12][8] = self.animal[12][12] = self.animal[12][13] = \
                    self.animal[13][7] = self.animal[13][8] = self.animal[13][9] = self.animal[13][11] = self.animal[13][12] = \
                    self.animal[13][13] = -1
                self.init_step = 17 # 17 initial steps
            elif level == 2:
                self.__init__(4, 8)
                self.init_step = 16 # 16 initial steps
            elif level == 3:
                self.__init__(7, 7)
                self.init_step = 18 # 18 initial steps
            elif level == 4:
                self.__init__(9, 7)
                row, col = self.row, self.col
                self.animal[row][col] = self.animal[row][col+7] = self.animal[row][col+8] = self.animal[row+1][col+8] = \
                    self.animal[row+5][col] = self.animal[row+6][col] = self.animal[row+6][col+1] = self.animal[row+6][col+8] = -1
                self.init_step = 20
            elif level == 5:
                self.__init__(8, 9)
                row, col = self.row, self.col
                self.animal[row][col+7] = self.animal[row+2][col] = self.animal[row+5][col] = self.animal[row+3][col+7] = \
                    self.animal[row+6][col+7] = self.animal[row+8][col] = -1
                self.init_step = 20
            elif level == 6:
                self.__init__(9, 9)
                row, col = self.row, self.col
                self.animal[row][col] = self.animal[row][col+8] = self.animal[row+2][col+4] = self.animal[row+3][col+2] = \
                    self.animal[row+3][col+6] = self.animal[row+8][col] = self.animal[row+8][col+8] = -1
                for i in range(row+4, row+6):
                    for j in range(col+3, col+6):
                        self.animal[i][j] = -1
                self.init_step = 28
            elif level == 7:
                self.__init__(9, 9)
                row, col = self.row, self.col
                for i in range(row, row + 9):
                    self.animal[i][col+4] = -1
                for j in range(col, col+4):
                    self.animal[row+3][j] = -1
                for j in range(col+5, col+9):
                    self.animal[row+5][j] = -1
                self.init_step = 25
            elif level == 8:
                self.__init__(7, 8)
                row, col = self.row, self.col
                for i in range(row+2, row+5):
                    for j in range(col+1, col+6):
                        self.ice_list[i][j] = 1
                self.init_step = 21
            elif level == 9:
                self.__init__(9, 9)
                row, col = self.row, self.col
                self.animal[row][col+4] = self.animal[row+4][col] = self.animal[row+4][col+8] = self.animal[row+8][col+4] = -1
                for i in range(row+1, row+8):
                    for j in range(col+1, col+8):
                        self.ice_list[i][j] = 1
                self.init_step = 35
            else:
                self.__init__(9, 9)
                row, col = self.row, self.col
                for i in range(row, row+2):
                    for j in range(col, col+9):
                        self.animal[i][j] = -1
                self.animal[row][col+4] = randint(0, 5)
                self.animal[row+1][col+2] = randint(0, 5)
                self.animal[row+1][col+4] = randint(0, 5)
                self.animal[row+1][col+6] = randint(0, 5)
                self.animal[row+2][col+1] = self.animal[row+3][col+1] = self.animal[row+2][col+3] = self.animal[row+3][col+3] =\
                    self.animal[row+2][col+5] = self.animal[row+3][col+5] = self.animal[row+2][col+7] = \
                    self.animal[row+3][col+7] = self.animal[row+8][col] = self.animal[row+8][col+8] = -1
                for i in range(row+4, row+8):
                    for j in range(col, col+9):
                        self.ice_list[i][j] = 1
                self.ice_list[row+2][col+4] = self.ice_list[row+3][col+2] = self.ice_list[row+3][col+4] = \
                    self.ice_list[row+3][col+6] = 1
                self.init_step = 40
            self.type = 0
            self.energy_num -= 5
            self.success_board = Board(Board.success, [200, 0]) # Success board
            self.fail_board = Board(Board.fail, [200, 0]) # Failure board
            self.step = self.init_step
            self.score = 0
            self.animal_num = [0, 0, 0, 0, 0, 0]
            self.ice_num = 0
            self.reset_mode = False

    def num_add(self):
        '''Add to score'''
        if self.num_sign:
            self.money += self.score * 2
            if self.score < self.min:
                self.energy_num += 1
            elif self.score < self.max:
                self.energy_num += 2
            else:
                self.energy_num += 5
            self.num_sign = False

    def judge_level(self):
        '''Check whether the level was passed'''
        if self.step <= 0:
            self.type = -1 # Game over
        if self.level == 1:
            if self.animal_num[4] >= 10: # L1: 10 frogs
                self.type = 1 # Level 1 passed
                self.num_add()
        elif self.level == 2:
            if self.animal_num[1] >= 21: # L2: 21 bears
                self.type = 1 # Level 2 passed
                self.num_add()
        elif self.level == 3:
            if self.animal_num[4] >= 16 and self.animal_num[5] >= 16: # L3: 16 frogs and 16 cows
                self.type = 1 # Level 3 passed
                self.num_add()
        elif self.level == 4:
            if self.animal_num[5] >= 18 and self.animal_num[2] >= 18: # L4: 18 cows and 18 chicks
                self.type = 1 # Level 4 passed
                self.num_add()
        elif self.level == 5:
            if self.animal_num[2] >= 28 and self.animal_num[0] >= 28: # L5: 28 chicks and 28 foxes
                self.type = 1 # Level 5 passed
                self.num_add()
        elif self.level == 6:
            if self.animal_num[4] >= 70: # L6: 70 frogs
                self.type = 1 # Level 6 passed
                self.num_add()
        elif self.level == 7:
            if self.animal_num[2] >= 36 and self.animal_num[1] >= 36 and self.animal_num[0] >= 36: # L7: 36 chickens, 36 bears and 36 foxes
                self.type = 1 # Level 7 passed
                self.num_add()
        elif self.level == 8:
            if self.ice_num >= 15: # L8: 15 ice
                self.type = 1 # Level 8 passed
                self.num_add()
        elif self.level == 9:
            if self.ice_num >= 49: # L9: 49 ice
                self.type = 1 # Level 9 passed
                self.num_add()
        else:
            if self.ice_num >= 39: # L10: 39 ice
                self.type = 1 # Level 10 passed
                self.num_add()

        self.judge_next(self.type, self.score)
