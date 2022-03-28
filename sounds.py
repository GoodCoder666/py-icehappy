from pygame.mixer import Sound

class Sounds:
    '''Game sounds.'''
    game_bgm = 'sound/GameSceneBGM.ogg'
    world_bgm = 'sound/WorldSceneBGM.ogg'
    eliminate_format = 'sound/eliminate/%d.ogg'
    score_level = ('sound/good.ogg', 'sound/great.ogg', 'sound/amazing.ogg', 'sound/excellent.ogg',\
                   'sound/unbelievable.ogg')
    click = 'sound/click.bubble.ogg'
    board_sound = 'sound/board.ogg'
    click_button = 'sound/click_common_button.ogg'
    money_sound = 'sound/money.ogg'
    ice_break = 'sound/ice_break.ogg'

def playSound(filename, loops=0):
    sound = Sound(filename)
    sound.play(loops)
