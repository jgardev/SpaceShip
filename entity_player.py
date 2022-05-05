import os
from entity_bullet import *
import time
from quick import qk, draw, data


class Player:

    def __init__(self):
        self.sprites = qk.split_image(
            './assets/spritesheets/ship.png', (16, 24))
        self.i = 0

        self.size = qk.percent_to_pixel((8, 12))
        self.y = qk.pc_y(70)
        self.x = qk.pc_x(50 - 8/2)

        self.velocity = 0
        self.shoot_time = 0
        self.shoot_time_max = 5

    def draw(self, deltatime):
        self.shoot_time -= deltatime * 100
        if self.shoot_time <= 0:
            self.shoot_time = 0

        self.i += deltatime * 10
        newVal = self.x + self.velocity * deltatime
        if newVal >= 0 and newVal <= qk.width - self.size[0]:
            self.x = newVal

        self.velocity *= 0.9
        if self.velocity < 0.1 and self.velocity > -0.1:
            self.velocity = 0

        image = self.sprites[int(self.i) % len(self.sprites)]
        draw.effect(image, self.x, self.y, self.size)

        if os.environ['SPACESHIP_DEBUG'] == '1':
            draw.border(self.x, self.y,
                        self.size[0], self.size[1], (255, 0, 0))
            draw.text('velocity: {0}'.format(
                self.velocity), 10, 100, 2, (0, 0, 0))
            draw.text('shoot delay: {0}'.format(
                self.shoot_time), 10, 120, 2, (0, 0, 0))
            draw.text('life: {0}'.format(
                data.player_life.value), 10, 140, 2, (0, 0, 0))
            draw.text('delta time: {0}'.format(
                deltatime), 10, 160, 2, (0, 0, 0))
            draw.text('enemies: {0}'.format(
                len(data.enemies)), 10, 180, 2, (0, 0, 0))
            draw.text('bullets: {0}'.format(
                len(data.bullet_list)), 10, 200, 2, (0, 0, 0))
            draw.text(
                'enemy spawn: {0}%'.format(int((data.enemy_time*100)/data.enemy_spawn_time)), 10, 220, 2, (0, 0, 0))
            draw.text(
                'kill enemies: {0}'.format(data.player_kill), 10, 240, 2, (0, 0, 0))
            draw.text(
                'play time: {0}s'.format(round(time.time()-data.start_time, 2)), 10, 260, 2, (0, 0, 0))
            draw.text(
                'cloud spawn: {0}%'.format(int((data.cloud.time*100)/data.cloud.next_time)), 10, 280, 2, (0, 0, 0))
            if self.shoot_time <= 0:
                draw.line(self.x+self.size[0]/2, self.y,
                          self.x+self.size[0]/2, 0, (0, 255, 0))
            else:
                draw.text('{0}%'.format(int(
                    self.shoot_time/self.shoot_time_max*100)), self.x, self.y - 20, 2, (255, 0, 0))

    def move_left(self):
        self.velocity -= 25

    def move_right(self):
        self.velocity += 25

    def fire(self):
        if self.shoot_time <= 0:

            self.shoot_time = self.shoot_time_max
            data.bullet_list.append(
                Bullet([self.x, self.y - self.size[1]], True))

