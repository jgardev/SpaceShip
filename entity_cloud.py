import random
from quick import qk, draw
from util import dbg

class Cloud:

    def __init__(self):
        self.time = 0
        self.position_op = [0, 0]
        self.sprites = [qk.get_image('./assets/backgrounds/clouds-transparent.png'),
                        qk.get_image('./assets/backgrounds/clouds.png')]
        self.active = False
        self.size = qk.percent_to_pixel((100, 40))
        self.margin = 0
        self.next_time = random.randint(1000, 2000)  # 10s , 20s

    def draw_background(self, deltatime):

        if not self.active:
            self.time += deltatime * 100
            if self.time >= self.next_time:
                self.next_time = random.randint(1000, 2000)
                dbg('New cloud, next spawn in {0} seconds'.format(
                    int(self.next_time/100)), 'GameInfo')
                self.time = 0
                self.active = True
                self.position_op = [0, -(qk.pc_y(5)+self.size[1])]
                self.margin = qk.pc_y(random.randint(6, 10))
        else:
            self.position_op[0] += deltatime * 80
            self.position_op[1] += deltatime * 100
            if self.position_op[0] >= qk.width:
                self.position_op[0] = 0

            if self.position_op[1] >= qk.height:
                self.active = False

            draw.effect(self.sprites[1], self.position_op[0],
                        self.position_op[1], self.size)
            draw.effect(self.sprites[1], self.position_op[0]-self.size[0]-1,
                        self.position_op[1], self.size, 0, 1, (True, False))
        pass

    def draw_opacity(self, deltatime):
        if self.active:
            draw.effect(self.sprites[0], self.position_op[0],
                        self.position_op[1]+self.margin, self.size)
            draw.effect(self.sprites[0], self.position_op[0]-self.size[0]-1,
                        self.position_op[1]+self.margin, self.size, 0, 1, (True, False))