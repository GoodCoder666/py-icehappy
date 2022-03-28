# -*- encoding: utf-8 -*-
'''Pygame sprites.'''
from pygame.sprite import Sprite
from pygame.image import load

class Tree(Sprite):
    '''Tree sprite'''
    # Images
    tree = 'img/tree.png'
    fruit = 'img/fruit.png'
    energy_num = 'img/energy/num.png'
    money = 'img/money.png'
    energy_buy = 'img/energy/buy.png'

    # Positioning
    x, y = 340, 510
    h = 90
    position = ([x, y], [x+50, y-25], [x+105, y-45], [x-5, y-h-5],
                [x+55, y-25-h+10], [x+105, y-45-h],
                [x, y-h*2], [x+50+10, y-25-h*2-5],
                [x+105+25, y-45-h*2-14], [x+30, y-h*3-30]) # Fruit positions
    energy_num_position = (15, 70) # Energy position
    energy_buy_position = (250, 400) # "Buy energy" position

    def __init__(self, icon, position):
        super().__init__()
        self.image = load(icon).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = position

    def draw(self, screen):
        '''Display the tree on the given screen.'''
        screen.blit(self.image, self.rect)

class Board(Sprite):
    '''Wooden boards'''
    # Images
    step_board = 'img/board/step.png'
    num_format = 'img/text/%d.png'
    task_board = 'img/task.png'
    ok = 'img/ok.png'
    level_format = 'img/level/%d.png'
    success  = 'img/board/success.png'
    fail     = 'img/board/fail.png'
    step_add = 'img/button/step_add.png'
    next   = 'img/button/next.png'
    replay = 'img/button/replay.png'
    stars  = 'img/star.png'
    money  = 'img/money.png'
    energy = 'img/energ.png'

    # Positioning
    button_position = [[300, 465], [500, 465]]
    starts_position = [[330, 340], [413, 340], [495, 340]]

    def __init__(self, icon, position):
        super().__init__()
        self.image = load(icon).convert_alpha()
        self.speed = [0, 45]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = position

    def move(self):
        '''Move the board with its speed.'''
        self.rect = self.rect.move(self.speed)
        if self.rect.bottom >= 543:
            self.speed = [0, -45]
        if self.speed == [0, -45] and self.rect.bottom <= 450:
            self.speed = [0, 0]

    def draw(self, screen):
        '''Display the board on the given screen.'''
        screen.blit(self.image, self.rect)

class Element(Sprite):
    '''Element type'''
    # 6 Animals: (0) Fox, (1) bear, (2) chicken, (3) eagle, (4) frog, (5) cow
    animals = ('img/animal/fox.png', 'img/animal/bear.png',
               'img/animal/chick.png', 'img/animal/eagle.png',
               'img/animal/frog.png', 'img/animal/cow.png')
    ice = 'img/ice/normal.png'
    brick = 'img/brick.png'
    frame = 'img/frame.png' # Selection frame
    bling_format = 'img/bling/%d.png'
    ice_format = 'img/ice/%d.png'

    # Score images
    score_level = ('img/text/good.png', 'img/text/great.png',
                   'img/text/amazing.png', 'img/excellent.png',
                   'img/unbelievable.png')
    none_animal = 'img/noneanimal.png'
    stop = 'img/exit.png'
    stop_position = (20, 530)

    def __init__(self, icon, position):
        super().__init__()
        self.image = load(icon).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = position # Topleft positioning
        self.speed = [0, 0]
        self.init_position = position

    def move(self, speed):
        '''Move with given speed.'''
        self.speed = speed
        self.rect = self.rect.move(self.speed)
        if self.speed[0] != 0: # Moving horizontally
            if abs(self.rect.left - self.init_position[0]) == self.rect[2]:
                self.init_position = self.rect.topleft
                self.speed = [0, 0]
        else: # Moving vertically
            if abs(self.rect.top - self.init_position[1]) == self.rect[3]:
                self.init_position = self.rect.topleft
                self.speed = [0, 0]

    def draw(self, screen):
        '''Display the element on the given screen.'''
        screen.blit(self.image, self.rect)
