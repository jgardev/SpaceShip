import random
import os
from quick import qk, draw



class Bullet:
    sprites_laser = []
    sprites_bolt = []
    LASER = 0
    BOLTS = 1

    def __init__(self, position, directionTop=True, type=0):
        self.position = position
        self.dir = directionTop
        self.size = qk.percent_to_pixel((4, 8))
        self.alive = True

        self.i = 0

        self.speed = 600
        self.bolts = []
        self.type = type
        if type == Bullet.BOLTS:
            self.size = qk.percent_to_pixel((4, 4))
            self.speed = 200

            maxl = random.randint(5, 10)
            for i in range(maxl):
                spaceX = qk.pc_x(random.randint(10, 20))
                spaceY = qk.pc_y(random.randint(0, 4))
                pos = [self.position[0] + spaceX, self.position[1] + spaceY]
                self.bolts.append(pos)

        if len(Bullet.sprites_laser) == 0 or len(Bullet.sprites_bolt) == 0:
            sprites = qk.split_image(
                './assets/spritesheets/laser-bolts.png', (16, 16))

            Bullet.sprites_laser = sprites[2:]
            Bullet.sprites_bolt = sprites[:2]

    def hit(self, position, size):
        if self.type == Bullet.LASER:
            if self.position[0] + self.size[0] >= position[0] and self.position[0] <= position[0] + size[0]:
                if self.position[1] + self.size[1] >= position[1] and self.position[1] <= position[1] + size[1]:
                    self.alive = False
                    return True
            return False
        else:
            hitb = False
            for bolt in self.bolts:
                if bolt[0] + self.size[0] >= position[0] and bolt[0] <= position[0] + size[0]:
                    if bolt[1] + self.size[1] >= position[1] and bolt[1] <= position[1] + size[1]:
                        self.bolts.remove(bolt)
                        hitb = True

            return hitb

    def draw(self, deltatime):
        self.i += deltatime * 10

        if self.type == Bullet.LASER:
            if self.dir:
                self.position[1] -= self.speed * deltatime
            else:
                self.position[1] += self.speed * deltatime

            if self.position[1] < 0 or self.position[1] > qk.height:
                self.alive = False

            image = Bullet.sprites_laser[int(
                self.i) % len(Bullet.sprites_laser)]
            draw.effect(
                image, self.position[0], self.position[1], self.size, 0, 1, (False, not self.dir))

            if os.environ['SPACESHIP_DEBUG'] == '1':
                draw.border(self.position[0], self.position[1],
                            self.size[0], self.size[1], (255, 0, 0))
        else:

            if self.position[1] < 0 or self.position[1] > qk.height:
                self.alive = False

            image = Bullet.sprites_bolt[int(
                self.i) % len(Bullet.sprites_bolt)]

            for b in self.bolts:

                if random.randint(0, 1):
                    b[0] += self.speed * 2 * deltatime
                else:
                    b[0] -= self.speed * 2 * deltatime

                b[1] += deltatime * self.speed

                draw.effect(
                    image, b[0], b[1], self.size, 0, 1, (False, not self.dir))

                if os.environ['SPACESHIP_DEBUG'] == '1':
                    draw.border(b[0], b[1],
                                self.size[0], self.size[1], (255, 0, 0))


