import random
import time
from entity_enemy import *
from screens import ScreenTypes
from util import dbg
from quick import qk, draw, screen, data
from pygame.constants import *


def screen_game(input, deltatime):
    size = qk.percent_to_pixel((100, 100))
    data.background_y += deltatime * data.background_speed
    if data.background_y >= qk.percent_to_pixel((0, 100))[1]:
        data.background_y = 0

    draw.effect(data.background, 0, data.background_y, size)
    draw.effect(data.background, 0, -qk.percent_to_pixel((0, 100))
                [1] + data.background_y, size)

    key_fire = data.fire_key.key
    key_left = data.left_key.key
    key_right = data.right_key.key

    data.enemy_time += deltatime * 100
    data.score += deltatime

    if data.enemy_time >= data.enemy_spawn_time:
        data.enemy_time = 0
        type = random.choice([Enemy.BIG, Enemy.MEDIUM, Enemy.SMALL])

        if type == Enemy.BIG:
            data.enemy_spawn_time = 300
        elif type == Enemy.MEDIUM:
            data.enemy_spawn_time = 400
        else:
            data.enemy_spawn_time = 500

        data.enemies.append(
            Enemy(type))

    data.cloud.draw_background(deltatime)

    for bullet in data.bullet_list:

        if bullet.dir:
            for enemy in data.enemies:
                if bullet.hit(enemy.position, enemy.size):
                    enemy.life -= 1
                    data.score += 5

        else:
            if bullet.hit([data.player.x, data.player.y], data.player.size):
                data.player_life.sub(5)
                dbg('Player hit by enemy bullet', 'GameInfo')

        if bullet.alive:
            bullet.draw(deltatime)
        else:
            data.bullet_list.remove(bullet)

    for enemy in data.enemies:
        if enemy.alive:
            if enemy.hit([data.player.x, data.player.y], data.player.size):
                data.player_life.sub(10)
                dbg('Player hit by enemy', 'GameInfo')
                data.player_kill += 1
                data.score += 10
            else:
                enemy.draw(deltatime)
        else:
            data.enemies.remove(enemy)

    for explosion in data.explosions:
        if explosion.alive:
            explosion.draw(deltatime)
        else:
            data.explosions.remove(explosion)

    if input.key_tap(key_fire) or input.key_tap(K_SPACE) or input.key_tap(K_UP) or input.click():
        data.player.fire()

    if input.key_down(key_left) or input.key_down(K_LEFT):
        data.player.move_left()

    if input.key_down(key_right) or input.key_down(K_RIGHT):
        data.player.move_right()

    if input.key_tap(data.debug_key.key):
        os.environ['SPACESHIP_DEBUG'] = '0' if os.environ['SPACESHIP_DEBUG'] == '1' else '1'
        dbg('Switch debug mode', 'UpdateDebug')

    data.player.draw(deltatime)
    data.cloud.draw_opacity(deltatime)

    if data.player_life.value <= 0:
        dbg('Player died game is over', 'GameInfo')
        data.set_var('time_duration', time.time()-data.start_time)
        screen.set_screen(ScreenTypes.GAME_OVER)

    draw.text('Score {0}'.format(int(data.score)),
              10, qk.pc_y(6), 5, (255, 255, 255))

    data.player_life.draw()

    return 0
