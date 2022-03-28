# -*- encoding: utf-8 -*-
'''Game sounds.'''
from enum import Enum
from pygame.mixer import Sound

class Sounds(Enum):
    '''Enum for the game's sounds.'''
    GAME_BGM = 'sound/GameSceneBGM.ogg'
    WORLD_BGM = 'sound/WorldSceneBGM.ogg'
    ELIMINATE_FORMAT = 'sound/eliminate/%d.ogg'
    SCORE_LEVEL = ('sound/good.ogg', 'sound/great.ogg', 'sound/amazing.ogg', 'sound/excellent.ogg',\
                   'sound/unbelievable.ogg')
    CLICK = 'sound/click.bubble.ogg'
    BOARD_SOUND = 'sound/board.ogg'
    CLICK_BUTTON = 'sound/click_common_button.ogg'
    MONEY = 'sound/money.ogg'
    ICE_BREAKING = 'sound/ice_break.ogg'

    @staticmethod
    def eliminate(idx):
        '''Plays the eliminate sound with given index.'''
        Sound(Sounds.ELIMINATE_FORMAT.value%idx).play()

    @staticmethod
    def score_level(idx):
        '''Plays the score level sound with given index.'''
        Sound(Sounds.SCORE_LEVEL.value[idx]).play()

def play_sound(sound: Enum):
    '''Play sound with given number of loops.'''
    Sound(sound.value).play()
