import random
import os
from entity_explosion import *
from entity_bullet import *
from quick import qk, draw, data


class Enemy:

    BIG = 0
    MEDIUM = 1
    SMALL = 2

    def __init__(self, type):
        self.min_x = random.randint(0, qk.pc_x(80))
        self.max_x = random.randint(0, qk.pc_x(80))
        if self.min_x > self.max_x:
            self.max_x, self.min_x = self.min_x, self.max_x
        self.max_x += random.randint(qk.pc_x(5), qk.pc_x(20))

        self.size = []

        self.i = 0
        self.dirLeft = False
        self.sprites = []
        self.alive = True
        self.life = 5
        self.shoot_time_max = 0
        self.shoot_time = 0
        self.bullet_type = Bullet.LASER

        self._load_type(type)

        self.position = [random.randint(self.min_x, self.max_x), -self.size[1]]

    def hit(self, postion, size):
        if self.position[0] + self.size[0] >= postion[0] and self.position[0] <= postion[0] + size[0]:
            if self.position[1] + self.size[1] >= postion[1] and self.position[1] <= postion[1] + size[1]:
                data.explosions.append(Explosion(self.position))
                self.alive = False
                return True
        return False

    def _load_type(self, type):
        if type == Enemy.BIG:
            self.shoot_time_max = 300
            self.sprites = qk.split_image(
                './assets/spritesheets/enemy-big.png', (32, 32))
            self.size = qk.percent_to_pixel((16, 16))
        elif type == Enemy.MEDIUM:
            self.bullet_type = Bullet.BOLTS
            self.shoot_time_max = 200
            self.sprites = qk.split_image(
                './assets/spritesheets/enemy-medium.png', (32, 16))
            self.size = qk.percent_to_pixel((16, 8))
        else:
            self.shoot_time_max = 100
            self.sprites = qk.split_image(
                './assets/spritesheets/enemy-small.png', (16, 16))
            self.size = qk.percent_to_pixel((8, 8))

        self.shoot_time = self.shoot_time_max

    def fire(self):
        data.bullet_list.append(
            Bullet([self.position[0], self.position[1] + self.size[1]], False, self.bullet_type))

    def draw(self, deltatime):
        if self.life <= 0:
            data.player_kill += 1
            data.explosions.append(Explosion(self.position))
            self.alive = False

        self.shoot_time += deltatime*100
        if self.shoot_time >= self.shoot_time_max:
            self.shoot_time = 0
            self.fire()

        self.position[1] += deltatime*100
        if self.position[1] > qk.pc_y(100) + self.size[1]:
            self.alive = False

        if self.dirLeft:
            self.position[0] -= deltatime*100
            if self.position[0] < self.min_x:
                self.dirLeft = False
        else:
            self.position[0] += deltatime*100
            if self.position[0] > self.max_x:
                self.dirLeft = True

        self.i += deltatime*100

        image = self.sprites[int(self.i) % len(self.sprites)]
        draw.effect(image, self.position[0], self.position[1], self.size)

        if os.environ['SPACESHIP_DEBUG'] == '1':
            draw.text('{0}% x: {1}'.format((int(self.life*100)/5), int(self.position[0])),
                      self.position[0], self.position[1] - 20, 2, (255, 0, 0))

            draw.text('min: {0} max: {1} '.format(self.min_x, self.max_x),
                      self.position[0], self.position[1] + self.size[1], 2, (255, 0, 0))

            draw.border(self.position[0], self.position[1],
                        self.size[0], self.size[1], (255, 0, 0))

            draw.line(
                self.min_x, self.position[1], self.position[0], self.position[1], (0, 0, 255))
            draw.line(
                self.max_x+self.size[0], self.position[1], self.position[0]+self.size[0], self.position[1], (0, 0, 255))