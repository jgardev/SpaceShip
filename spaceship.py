import os
import sys

from screen_game import *
from screen_home import *
from screen_setting import *
from screen_gameover import *

from gui_button import *



from quick import qk, draw, screen, data
from pygame.constants import *


os.environ['SPACESHIP_DEBUG'] = '0'


def game(input, deltatime):
    screen.game(input, deltatime)

    if deltatime:
        qk.set_title('SpaceShip | {0} FPS'.format(int(1/deltatime)))
    return 0


def main(args):
    qk.init(800, 600, 'SpaceShip', False, False)

    screen.add_screen(screen_home)
    screen.add_screen(screen_game)
    screen.add_screen(screen_settings)
    screen.add_screen(screen_gameover)
    screen.set_screen(ScreenTypes.HOME)

    add_btn('btn_play', 'Start Game', -qk.percent_to_pixel((5, 15))[1])
    add_btn('btn_settings', 'Settings', -qk.percent_to_pixel((5, 0))[1])
    add_btn('btn_quit', 'Exit', qk.percent_to_pixel((5, 15))[1])

    add_btn('btn_back_home', 'Back Home', qk.percent_to_pixel((0, 30))[1])

    data_reset()
    data.set_var('score_board', [])

    draw.set_font(draw.get_font('arial', 20, 4))

    qk.run(game)
    return 0




if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
