from quick import qk, draw, screen, data
from util import dbg
from screens import ScreenTypes
from entity_cloud import *
from entity_player import *
from gui_input import *
from gui_range import *
from pygame.constants import *

def screen_gameover(input, deltatime):
    draw.rectangle(0, 0, qk.width, qk.height, (20, 20, 20))

    if data.game_over == -1:
        draw.text('GameOver', qk.pc_x(
            50), qk.pc_y(35), 19, (220, 220, 220), True)
        spacetop = draw.text('Score {0}'.format(int(data.score)),
                             qk.pc_x(50), qk.pc_y(50), 8, (220, 220, 220), True)[1]

        draw.text('Time {0}s'.format(round(data.time_duration, 2)), qk.pc_x(
            50), qk.pc_y(50) + spacetop, 6, (220, 220, 220), True)

        if data.btn_back_home.draw(input, deltatime):
            dbg('Reset game data to restart', 'GameInfo')
            data.score_board.append([round(data.score), round(data.time_duration,2)])
            data.score_board = sorted(data.score_board, key=lambda x: x[0])[::-1]
            data_reset()
            screen.set_screen(ScreenTypes.HOME)
    else:
        data.game_over += deltatime * 18
        if data.game_over >= 20:
            data.game_over = -1

        draw.text('GameOver', qk.pc_x(50), qk.pc_y(50), int(
            data.game_over) % 20, (220, 220, 220), True)
    return 0


def data_reset():
    data.set_var('background', qk.get_image(
        './assets/backgrounds/desert-backgorund.png'))
    data.set_var('background_y', 0)
    data.set_var('cloud', Cloud())

    playerlife = 100
    data.set_var('player_life', Range(qk.percent_to_pixel(
        (20, 3.5)), [10, 10], (30, 200, 30), playerlife))
    data.set_var('score', 0)

    data.set_var('left_key', InputKeyBoard(K_q,
                                           (qk.pc_x(50), qk.pc_y(20)),
                                           qk.percent_to_pixel((10, 10)),
                                           (200, 200, 200), (50, 200, 50)))

    data.set_var('right_key', InputKeyBoard(K_d,
                                            (qk.pc_x(50), qk.pc_y(32)),
                                            qk.percent_to_pixel((10, 10)),
                                            (200, 200, 200), (50, 200, 50)))

    data.set_var('fire_key', InputKeyBoard(K_z,
                                           (qk.pc_x(50), qk.pc_y(44)),
                                           qk.percent_to_pixel((10, 10)),
                                           (200, 200, 200), (50, 200, 50)))

    data.set_var('debug_key', InputKeyBoard(K_i,
                                            (qk.pc_x(50), qk.pc_y(56)),
                                            qk.percent_to_pixel((10, 10)),
                                            (200, 200, 200), (50, 200, 50)))

    data.set_var('player', Player())
    data.set_var('enemy_time', 0)
    data.set_var('enemy_spawn_time', 100)
    data.set_var('background_speed', 100)
    data.set_var('enemies', [])
    data.set_var('bullet_list', [])
    data.set_var('explosions', [])
    data.set_var('player_kill', 0)
    data.set_var('start_time', 0)
    data.set_var('game_over', 1)